import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class SplashScreen(QWidget):

    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setFixedSize(800, 480)
        
        # Optional: Makes it look like a real splash screen by removing borders
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.setStyleSheet("""
        background-color:#06090E;
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ################################################
        # LOGO
        ################################################

        self.logo = QLabel("AI")
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo.setStyleSheet("""
        color:#3DB8FF;
        font-size:90px;
        font-weight:bold;
        """)

        ################################################
        # TITLE (Fixed alignment flag)
        ################################################

        title = QLabel("CAR INFOTAINMENT")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
        color:white;
        font-size:30px;
        font-weight:bold;
        """)

        ################################################
        # PROGRESS BAR
        ################################################

        self.progress = QProgressBar()
        self.progress.setFixedWidth(400)
        self.progress.setValue(0)
        self.progress.setStyleSheet("""
        QProgressBar{
            border:2px solid #3DB8FF;
            border-radius:10px;
            text-align:center;
            color:white;
            background:#101923;
        }
        QProgressBar::chunk{
            background:#3DB8FF;
            border-radius:8px;
        }
        """)

        ################################################
        # LAYOUT ASSEMBLY
        ################################################

        layout.addWidget(self.logo)
        layout.addSpacing(10)
        layout.addWidget(title)
        layout.addSpacing(30)
        layout.addWidget(self.progress)
        self.setLayout(layout)

        ################################################
        # TIMER
        ################################################

        self.value = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateProgress)
        self.timer.start(30)

    def updateProgress(self):
        self.value += 1
        self.progress.setValue(self.value)

        if self.value >= 100:
            self.timer.stop()
            self.finished.emit()


# Execution block to test the screen
if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    # Connect to app exit just for testing closing behavior
    splash.finished.connect(app.quit) 
    sys.exit(app.exec())
