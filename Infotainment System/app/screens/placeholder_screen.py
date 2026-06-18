from PyQt6.QtCore import Qt, pyqtSignal

from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class PlaceholderScreen(QWidget):

    # Custom signal
    homeClicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):

        self.setStyleSheet("""

        QWidget{
            background:#202020;
            color:white;
        }

        QLabel{
            color:white;
        }

        QPushButton{
            background:#303030;
            color:white;
            border:none;
            border-radius:8px;
            font-size:18px;
            padding:10px;
        }

        QPushButton:hover{
            background:#505050;
        }

        """)

        layout = QVBoxLayout()

        layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.setSpacing(20)

        # -------------------------
        # Screen Title
        # -------------------------

        self.title = QLabel()

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.title.setStyleSheet("""

        font-size:40px;
        font-weight:bold;

        """)

        layout.addWidget(self.title)

        # -------------------------
        # Coming Soon
        # -------------------------

        comingSoon = QLabel("Coming Soon")

        comingSoon.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        comingSoon.setStyleSheet("""

        color:gray;
        font-size:25px;

        """)

        layout.addWidget(comingSoon)

        # -------------------------
        # Home Button
        # -------------------------

        homeButton = QPushButton("Home")

        homeButton.setFixedWidth(150)

        homeButton.clicked.connect(
            self.homeClicked.emit
        )

        layout.addWidget(
            homeButton,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.setLayout(layout)

    # -------------------------

    def setTitle(self, title):
        self.title.setText(title)