"""Thin PySide6 wrapper around the existing non-interactive CLI flow."""

import sys
from pathlib import Path

from PySide6.QtCore import QProcess, Qt
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QCheckBox,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from src.core.config import PROJECT_ROOT, get_services_config
from src.core.domain.choices import OPERATION_CHOICES, PLATFORM_CHOICES


def get_venv_python() -> Path:
    """Resolve the local project virtualenv interpreter."""
    return PROJECT_ROOT / ".venv" / "bin" / "python"


class MainWindow(QMainWindow):
    """Main GUI window for launching CLI operations."""

    def __init__(self) -> None:
        super().__init__()
        self.process: QProcess | None = None
        self.service_items: list[QListWidgetItem] = []

        self.setWindowTitle("Bazarrify Deployment Tool")
        self.resize(980, 720)

        root = QWidget()
        self.setCentralWidget(root)

        layout = QVBoxLayout(root)
        layout.addWidget(self._build_form_group())
        layout.addWidget(self._build_actions_row())
        layout.addWidget(self._build_output_group(), stretch=1)

        self._refresh_services()
        self._update_command_preview()

    def _build_form_group(self) -> QGroupBox:
        group = QGroupBox("Execution")
        layout = QFormLayout(group)

        self.mode_combo = QComboBox()
        for choice in OPERATION_CHOICES:
            self.mode_combo.addItem(choice.label, choice.value)
        self.mode_combo.currentIndexChanged.connect(self._update_command_preview)

        self.arch_combo = QComboBox()
        for choice in PLATFORM_CHOICES:
            self.arch_combo.addItem(choice.label, choice.value)
        self.arch_combo.currentIndexChanged.connect(self._update_command_preview)

        self.service_list = QListWidget()
        self.service_list.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.service_list.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        self.service_list.itemChanged.connect(self._update_command_preview)

        self.select_all_checkbox = QCheckBox("Select all services")
        self.select_all_checkbox.toggled.connect(self._toggle_all_services)

        services_layout = QVBoxLayout()
        services_layout.addWidget(self.select_all_checkbox)
        services_layout.addWidget(self.service_list)

        services_container = QWidget()
        services_container.setLayout(services_layout)

        layout.addRow("Mode", self.mode_combo)
        layout.addRow("Architecture", self.arch_combo)
        layout.addRow("Services", services_container)
        return group

    def _build_actions_row(self) -> QWidget:
        row = QWidget()
        layout = QHBoxLayout(row)

        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self._run_command)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self._stop_command)

        self.refresh_button = QPushButton("Reload Services")
        self.refresh_button.clicked.connect(self._refresh_services)

        self.command_preview = QLabel()
        self.command_preview.setTextInteractionFlags(self.command_preview.textInteractionFlags())

        layout.addWidget(self.run_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.command_preview, stretch=1)
        return row

    def _build_output_group(self) -> QGroupBox:
        group = QGroupBox("Output")
        layout = QVBoxLayout(group)

        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        layout.addWidget(self.output)
        return group

    def _refresh_services(self) -> None:
        self.service_list.clear()
        self.service_items.clear()

        services = list(get_services_config().get("services", {}).keys())
        for service in services:
            item = QListWidgetItem(service)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.service_list.addItem(item)
            self.service_items.append(item)

        self.select_all_checkbox.setChecked(False)
        self._update_command_preview()

    def _toggle_all_services(self, checked: bool) -> None:
        state = Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
        for item in self.service_items:
            item.setCheckState(state)
        self._update_command_preview()

    def _selected_services(self) -> list[str]:
        selected: list[str] = []
        for item in self.service_items:
            if item.checkState() == Qt.CheckState.Checked:
                selected.append(item.text())
        return selected

    def _command_args(self) -> list[str]:
        return [
            "-m",
            "main",
            self.mode_combo.currentData(),
            self.arch_combo.currentData(),
            *self._selected_services(),
        ]

    def _update_command_preview(self) -> None:
        python_path = get_venv_python()
        args = self._command_args()
        self.command_preview.setText(
            f"Command: {python_path} {' '.join(args)}"
        )

    def _append_output(self, text: str) -> None:
        if not text:
            return
        self.output.moveCursor(QTextCursor.MoveOperation.End)
        self.output.insertPlainText(text)
        self.output.moveCursor(QTextCursor.MoveOperation.End)

    def _run_command(self) -> None:
        python_path = get_venv_python()
        if not python_path.exists():
            QMessageBox.critical(
                self,
                "Missing Interpreter",
                f"Expected interpreter not found at:\n{python_path}",
            )
            return

        services = self._selected_services()
        if not services:
            QMessageBox.warning(self, "No Services", "Select at least one service.")
            return

        self._update_command_preview()
        self.output.clear()
        self._append_output("Starting process...\n\n")

        self.process = QProcess(self)
        self.process.setProgram(str(python_path))
        self.process.setArguments(self._command_args())
        self.process.setWorkingDirectory(str(PROJECT_ROOT))
        self.process.readyReadStandardOutput.connect(self._read_stdout)
        self.process.readyReadStandardError.connect(self._read_stderr)
        self.process.finished.connect(self._process_finished)

        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.process.start()

    def _stop_command(self) -> None:
        if self.process is not None:
            self.process.kill()

    def _read_stdout(self) -> None:
        if self.process is None:
            return
        text = bytes(self.process.readAllStandardOutput().data()).decode(
            "utf-8",
            errors="replace",
        )
        self._append_output(text)

    def _read_stderr(self) -> None:
        if self.process is None:
            return
        text = bytes(self.process.readAllStandardError().data()).decode(
            "utf-8",
            errors="replace",
        )
        self._append_output(text)

    def _process_finished(self, exit_code: int, _exit_status: QProcess.ExitStatus) -> None:
        self._append_output(f"\n\nProcess finished with exit code {exit_code}.\n")
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.process = None


def main() -> int:
    """Launch the GUI application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
