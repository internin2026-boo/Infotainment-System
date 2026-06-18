from PyQt6.QtWidgets import *

from screens.splash_screen import SplashScreen
from screens.home_screen import HomeScreen
from screens.music_screen import MusicScreen  # 1. Import the music screen


class MainWindow(QWidget):

    def __init__(
            self,
            configuration,
            music_controller
    ):
        super().__init__()
        self.configuration = configuration
        self.music_controller = music_controller

        self.setWindowTitle("AI Car Infotainment")
        self.resize(800, 480)

        ################################################
        self.stack = QStackedWidget(self)

        ################################################
        self.splash = SplashScreen()
        self.home = HomeScreen()
        
        # 2. Instantiate the MusicScreen and pass the music controller
        self.music_page = MusicScreen(self.music_controller)

        ################################################
        self.stack.addWidget(self.splash)  # Index 0
        self.stack.addWidget(self.home)    # Index 1
        self.stack.addWidget(self.music_page) # Index 2

        ################################################
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stack)
        self.setLayout(layout)

        ################################################
        # 3. Connect screen navigation signals
        
        # Splash finishes -> Show Home
        self.splash.finished.connect(self.showHome)
        
        # Home Screen "Music" clicked -> Show Music Screen
        self.home.musicClicked.connect(self.showMusicPlayer)
        
        # Music Screen "Back" clicked -> Go back to Home Screen
        self.music_page.backClicked.connect(self.showHome)

    ################################################
    def showHome(self):
        self.stack.setCurrentIndex(1)

    def showMusicPlayer(self):
        self.stack.setCurrentIndex(2)