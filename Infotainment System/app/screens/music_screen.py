from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class MusicScreen(QWidget):
    backClicked = pyqtSignal()

    def __init__(self, music_controller, parent=None):
        super().__init__(parent)
        self.music_controller = music_controller

        self.setStyleSheet("""
            QWidget {
                background: #06090E;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(15)

        ################################################
        # HEADER (Back Button + Title)
        ################################################
        header_layout = QHBoxLayout()
        
        back_btn = QPushButton("⬅ Dashboard")
        back_btn.setFixedSize(130, 40)
        back_btn.setStyleSheet("""
            QPushButton {
                background: #101923; color: white; border: 1px solid #22354A;
                border-radius: 10px; font-size: 14px; font-weight: bold;
            }
            QPushButton:hover { background: #173B5C; }
            QPushButton:pressed { background: #3DB8FF; }
        """)
        back_btn.clicked.connect(self.backClicked.emit)
        header_layout.addWidget(back_btn)
        header_layout.addStretch()
        
        main_layout.addLayout(header_layout)

        ################################################
        # NOW PLAYING INFO
        ################################################
        main_layout.addStretch()
        
        self.track_icon = QLabel("🎵")
        self.track_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.track_icon.setStyleSheet("font-size: 70px;")
        main_layout.addWidget(self.track_icon)

        self.title_label = QLabel("No song playing")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            color: white; font-size: 22px; font-weight: bold;
        """)
        main_layout.addWidget(self.title_label)

        main_layout.addSpacing(10)

        ################################################
        # PROGRESS SLIDER & TIMESTAMPS
        ################################################
        progress_layout = QVBoxLayout()
        
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px; background: #101923; border-radius: 3px;
            }
            QSlider::sub-page:horizontal {
                background: #3DB8FF; border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: white; width: 14px; margin-top: -4px; margin-bottom: -4px; border-radius: 7px;
            }
        """)
        # Allow clicking and dragging the slider to skip sections of the song
        self.slider.sliderMoved.connect(self.music_controller.set_position)
        progress_layout.addWidget(self.slider)

        # Time labels
        time_label_layout = QHBoxLayout()
        self.time_current = QLabel("00:00")
        self.time_current.setStyleSheet("color: #7F96AD; font-size: 12px;")
        
        self.time_total = QLabel("00:00")
        self.time_total.setStyleSheet("color: #7F96AD; font-size: 12px;")
        self.time_total.setAlignment(Qt.AlignmentFlag.AlignRight)

        time_label_layout.addWidget(self.time_current)
        time_label_layout.addWidget(self.time_total)
        progress_layout.addLayout(time_label_layout)

        main_layout.addLayout(progress_layout)
        main_layout.addStretch()

        ################################################
        # CONTROLS (Prev, Play/Pause, Next)
        ################################################
        controls_layout = QHBoxLayout()
        controls_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        controls_layout.setSpacing(25)

        self.prev_btn = self.create_media_button("⏮", 60)
        self.play_btn = self.create_media_button("▶", 75)
        self.next_btn = self.create_media_button("⏭", 60)

        self.prev_btn.clicked.connect(self.music_controller.previous_song)
        self.play_btn.clicked.connect(self.music_controller.toggle_play_pause)
        self.next_btn.clicked.connect(self.music_controller.next_song)

        controls_layout.addWidget(self.prev_btn)
        controls_layout.addWidget(self.play_btn)
        controls_layout.addWidget(self.next_btn)
        
        main_layout.addLayout(controls_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

        ################################################
        # STATUS TIMER (Sync UI components with backend changes)
        ################################################
        self.ui_timer = QTimer(self)
        self.ui_timer.timeout.connect(self.sync_player_ui)
        self.ui_timer.start(500) # Check every half-second

        # Connect core signal changes to keep ui responsive
        self.music_controller.songChanged.connect(self.sync_player_ui)
        self.music_controller.playbackChanged.connect(self.update_play_button_text)

    def create_media_button(self, text, size):
        btn = QPushButton(text)
        btn.setFixedSize(size, size)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: #101923; color: white; border: 1px solid #22354A;
                border-radius: {size // 2}px; font-size: {size // 3}px;
            }}
            QPushButton:hover {{ background: #173B5C; border-color: #3DB8FF; }}
            QPushButton:pressed {{ background: #3DB8FF; color: black; }}
        """)
        return btn

    def update_play_button_text(self):
        if self.music_controller.isPlaying:
            self.play_btn.setText("⏸")
        else:
            self.play_btn.setText("▶")

    def sync_player_ui(self):
        # Update Track Title
        self.title_label.setText(self.music_controller.currentTitle)
        
        # Sync Playback state display icon toggle
        self.update_play_button_text()

        # Update Timeline Progress and Duration Labels
        duration = self.music_controller.duration
        position = self.music_controller.position

        if duration > 0:
            self.slider.setMaximum(duration)
            self.slider.setValue(position)
            self.time_current.setText(self.music_controller.formattedPosition)
            self.time_total.setText(self.music_controller.formattedDuration)
        else:
            self.slider.setValue(0)
            self.time_current.setText("00:00")
            self.time_total.setText("00:00")