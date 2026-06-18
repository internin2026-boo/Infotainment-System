from PyQt6.QtCore import (
    Qt,
    pyqtSignal,
)

from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)


class AppTile(QFrame):

    # Signal
    clicked = pyqtSignal()

    def __init__(self, title=""):

        super().__init__()

        self.title = title

        self.setupUI()

    def setupUI(self):

        # Fixed Size
        self.setFixedSize(150, 100)

        # Styling
        self.setStyleSheet("""

        QFrame{

            background:#303030;

            border-radius:15px;

        }

        QFrame:hover{

            background:#404040;

        }

        """)

        # Layout
        layout = QVBoxLayout()

        layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # Text
        self.label = QLabel(self.title)

        self.label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.label.setStyleSheet("""

        color:white;

        font-size:24px;

        font-weight:bold;

        background:transparent;

        """)

        layout.addWidget(self.label)

        self.setLayout(layout)

    # Mouse Click

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:

            self.clicked.emit()

        super().mousePressEvent(event)

    # Change Title

    def setTitle(self, title):

        self.title = title

        self.label.setText(title)