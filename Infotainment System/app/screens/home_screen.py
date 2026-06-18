from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from datetime import datetime


class HomeScreen(QWidget):

    musicClicked = pyqtSignal()
    navigationClicked = pyqtSignal()
    phoneClicked = pyqtSignal()
    radioClicked = pyqtSignal()
    bluetoothClicked = pyqtSignal()
    vehicleClicked = pyqtSignal()
    aiClicked = pyqtSignal()
    settingsClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("""
        QWidget{
            background:#06090E;
        }
        """)

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(20, 20, 20, 20)
        mainLayout.setSpacing(15)

        ################################################
        # HEADER
        ################################################
        header = QHBoxLayout()
        left = QVBoxLayout()

        title = QLabel("AI Car Infotainment")
        title.setStyleSheet("""
        color:#3DB8FF;
        font-size:25px;
        font-weight:bold;
        """)

        subtitle = QLabel("Smart Dashboard")
        subtitle.setStyleSheet("""
        color:#7F96AD;
        font-size:13px;
        """)

        left.addWidget(title)
        left.addWidget(subtitle)
        header.addLayout(left)
        header.addStretch()

        right = QVBoxLayout()
        self.clock = QLabel()
        self.clock.setAlignment(Qt.AlignmentFlag.AlignRight) # PyQt6 explicit namespace
        self.clock.setStyleSheet("""
        color:white;
        font-size:20px;
        font-weight:bold;
        """)

        self.date = QLabel()
        self.date.setAlignment(Qt.AlignmentFlag.AlignRight) # PyQt6 explicit namespace
        self.date.setStyleSheet("""
        color:gray;
        font-size:12px;
        """)

        right.addWidget(self.clock)
        right.addWidget(self.date)
        header.addLayout(right)

        mainLayout.addLayout(header)

        ################################################
        # ICON GRID
        ################################################
        grid = QGridLayout()
        grid.setSpacing(15)

        grid.addWidget(self.makeButton("🎵\nMusic", self.musicClicked), 0, 0)
        grid.addWidget(self.makeButton("🗺\nNavigation", self.navigationClicked), 0, 1)
        grid.addWidget(self.makeButton("📞\nPhone", self.phoneClicked), 1, 0)
        grid.addWidget(self.makeButton("📻\nRadio", self.radioClicked), 1, 1)
        grid.addWidget(self.makeButton("🔵\nBluetooth", self.bluetoothClicked), 2, 0)
        grid.addWidget(self.makeButton("🚗\nVehicle", self.vehicleClicked), 2, 1)
        grid.addWidget(self.makeButton("🤖\nAI", self.aiClicked), 3, 0)
        grid.addWidget(self.makeButton("⚙\nSettings", self.settingsClicked), 3, 1)

        mainLayout.addLayout(grid)
        mainLayout.addStretch()

        ################################################
        # FOOTER
        ################################################
        footer = QLabel("🏠 Home     🎵 Music     📞 Phone     ⚙ Settings")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter) # PyQt6 explicit namespace
        footer.setStyleSheet("""
        color:gray;
        font-size:16px;
        """)

        mainLayout.addWidget(footer)
        self.setLayout(mainLayout)

        ################################################
        # TIMER
        ################################################
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateClock)
        self.timer.start(1000)
        self.updateClock()

    def updateClock(self):
        now = datetime.now()
        self.clock.setText(now.strftime("%I:%M %p"))
        self.date.setText(now.strftime("%d %b %Y"))

    def makeButton(self, text, signal):
        button = QPushButton(text)
        button.setFixedSize(180, 80)
        button.setStyleSheet("""
        QPushButton{
            background:#101923;
            color:white;
            font-size:18px;
            font-weight:bold;
            border:1px solid #22354A;
            border-radius:15px;
        }
        QPushButton:hover{
            background:#173B5C;
        }
        QPushButton:pressed{
            background:#3DB8FF;
        }
        """)
        button.clicked.connect(signal.emit)
        return button