from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt


class HistoryView(QWidget):
    """View for displaying operation history (undo/redo stacks)"""

    def __init__(self, history_controller):
        super().__init__()
        self.history_controller = history_controller
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Refresh button
        btn_layout = QHBoxLayout()
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.load_data)
        btn_layout.addStretch()
        btn_layout.addWidget(refresh_btn)
        layout.addLayout(btn_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["#", "Operation", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.table)

    def load_data(self):
        try:
            history = self.history_controller.get_history()
            self.table.setRowCount(0)

            if history:
                for row_idx, record in enumerate(history):
                    self.table.insertRow(row_idx)
                    self.table.setItem(row_idx, 0, QTableWidgetItem(str(row_idx + 1)))
                    self.table.setItem(row_idx, 1, QTableWidgetItem(record['operation']))
                    self.table.setItem(row_idx, 2, QTableWidgetItem(record['status']))
        except Exception as e:
            print(f"Failed to load history: {str(e)}")
