from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt


class ControlButton(QPushButton):

    def __init__(self, text=""):

        super().__init__(text)

        # Default Colors
        self.normalColor = "#18263A"
        self.hoverColor = "#213550"
        self.pressedColor = "#1976D2"
        self.disabledColor = "#111923"
        self.outlineColor = "#304560"

        self.setupUI()

    def setupUI(self):

        self.setMinimumSize(150, 64)

        # PyQt6 Cursor
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setStyleSheet(self.getStyle())

    def getStyle(self):

        return f"""

        QPushButton{{

            background-color:{self.normalColor};

            color:#F7FAFC;

            border:1px solid {self.outlineColor};

            border-radius:16px;

            font-size:18px;

            font-weight:bold;

        }}

        QPushButton:hover{{

            background-color:{self.hoverColor};

        }}

        QPushButton:pressed{{

            background-color:{self.pressedColor};

        }}

        QPushButton:disabled{{

            background-color:{self.disabledColor};

            color:#667789;

            border:1px solid #1D2835;

        }}

        """