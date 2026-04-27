MAIN_STYLESHEET = """
    /* Main Window */
    QMainWindow {
        background-color: #1e293b;
    }

    QWidget {
        background-color: #1e293b;
        color: #e2e8f0;
    }
    
    /* Tabs */
    QTabWidget::pane {
        border: 1px solid #334155;
        background-color: #1e293b;
    }

    QTabBar::tab {
        background-color: #334155;
        color: #94a3b8;
        padding: 10px 25px;
        border: 1px solid #475569;
        border-bottom: none;
        font-weight: 500;
        margin-right: 2px;
    }
    
    QTabBar::tab:selected {
        background-color: #1e293b;
        border-bottom: 3px solid #3b82f6;
        color: #f1f5f9;
    }
    
    QTabBar::tab:hover:!selected {
        background-color: #475569;
        color: #e2e8f0;
    }
    
    /* Buttons */
    QPushButton {
        background-color: #3b82f6;
        color: white;
        border: none;
        padding: 10px 18px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 12px;
    }
    
    QPushButton:hover {
        background-color: #60a5fa;
    }
    
    QPushButton:pressed {
        background-color: #2563eb;
    }
    
    QPushButton:disabled {
        background-color: #475569;
        color: #64748b;
    }
    
    /* Tables */
    QTableWidget {
        background-color: #0f172a;
        alternate-background-color: #1e293b;
        border: 1px solid #334155;
        gridline-color: #334155;
        color: #e2e8f0;
    }
    
    QTableWidget::item {
        padding: 5px;
        border: none;
    }
    
    QTableWidget::item:selected {
        background-color: #1e3a5f;
        color: #f1f5f9;
    }
    
    QHeaderView::section {
        background-color: #334155;
        color: #f1f5f9;
        padding: 8px;
        border: none;
        font-weight: 600;
    }
    
    /* Input Fields */
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
        border: 1px solid #475569;
        border-radius: 4px;
        padding: 8px;
        background-color: #0f172a;
        color: #e2e8f0;
        selection-background-color: #1e3a5f;
    }
    
    QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
        border: 2px solid #3b82f6;
    }

    QComboBox::drop-down {
        border: none;
        background-color: #334155;
    }

    QComboBox QAbstractItemView {
        background-color: #0f172a;
        color: #e2e8f0;
        selection-background-color: #1e3a5f;
        border: 1px solid #475569;
    }
    
    /* Status Bar */
    QStatusBar {
        background-color: #0f172a;
        color: #94a3b8;
        border-top: 1px solid #334155;
    }
    
    /* Dialog */
    QDialog {
        background-color: #1e293b;
    }
    
    /* Message Box */
    QMessageBox {
        background-color: #1e293b;
    }

    QMessageBox QLabel {
        color: #e2e8f0;
    }
    
    /* Scrollbars */
    QScrollBar:vertical {
        background-color: #1e293b;
        width: 12px;
    }
    
    QScrollBar::handle:vertical {
        background-color: #475569;
        border-radius: 6px;
        min-height: 20px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #64748b;
    }
    
    QScrollBar:horizontal {
        background-color: #1e293b;
        height: 12px;
    }
    
    QScrollBar::handle:horizontal {
        background-color: #475569;
        border-radius: 6px;
        min-width: 20px;
    }
    
    QScrollBar::handle:horizontal:hover {
        background-color: #64748b;
    }

    QScrollBar::add-line, QScrollBar::sub-line {
        background: none;
        border: none;
    }

    QScrollBar::add-page, QScrollBar::sub-page {
        background: none;
    }
    
    /* Labels */
    QLabel {
        color: #e2e8f0;
        font-size: 12px;
    }
"""
