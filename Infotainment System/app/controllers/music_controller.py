from __future__ import annotations

from pathlib import Path
from typing import Final

from PyQt6.QtCore import QObject, pyqtProperty, QUrl, pyqtSignal, pyqtSlot
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer


class MusicController(QObject):
    """
    Controls song discovery, playback, volume and playback progress.

    QML calls the public slots and reads the exposed properties.
    """

    songChanged = pyqtSignal()
    playlistChanged = pyqtSignal()
    playbackChanged = pyqtSignal()
    statusChanged = pyqtSignal()
    volumeChanged = pyqtSignal()
    positionChanged = pyqtSignal()
    durationChanged = pyqtSignal()
    errorChanged = pyqtSignal()

    DEFAULT_VOLUME: Final[float] = 0.70

    def __init__(
        self,
        songs_directory: Path,
        supported_extensions: list[str],
        default_volume: int = 70,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)

        self._songs_directory = songs_directory
        self._supported_extensions = {
            extension.lower() for extension in supported_extensions
        }

        self._song_paths: list[Path] = []
        self._current_index = -1
        self._status = "Starting"
        self._error_message = ""

        self._audio_output = QAudioOutput(self)
        self._player = QMediaPlayer(self)
        self._player.setAudioOutput(self._audio_output)

        volume_percentage = max(0, min(default_volume, 100))
        self._audio_output.setVolume(volume_percentage / 100.0)

        self._player.playbackStateChanged.connect(
            self._handle_playback_state_changed
        )
        self._player.mediaStatusChanged.connect(
            self._handle_media_status_changed
        )
        self._player.positionChanged.connect(
            self._handle_position_changed
        )
        self._player.durationChanged.connect(
            self._handle_duration_changed
        )
        self._player.errorOccurred.connect(
            self._handle_error
        )

        self.scan_songs()

    # ---------------------------------------------------------
    # Properties exposed to QML
    # ---------------------------------------------------------

    @pyqtProperty(str, notify=songChanged)
    def currentTitle(self) -> str:
        if not self._has_current_song():
            return "No song selected"

        return self._song_paths[self._current_index].stem

    @pyqtProperty(str, notify=songChanged)
    def currentFileName(self) -> str:
        if not self._has_current_song():
            return ""

        return self._song_paths[self._current_index].name

    @pyqtProperty(int, notify=songChanged)
    def currentIndex(self) -> int:
        return self._current_index

    @pyqtProperty(int, notify=playlistChanged)
    def songCount(self) -> int:
        return len(self._song_paths)

    @pyqtProperty("QStringList", notify=playlistChanged)
    def songTitles(self) -> list[str]:
        return [song.stem for song in self._song_paths]

    @pyqtProperty(bool, notify=playbackChanged)
    def isPlaying(self) -> bool:
        return (
            self._player.playbackState()
            == QMediaPlayer.PlaybackState.PlayingState
        )

    @pyqtProperty(bool, notify=playbackChanged)
    def isPaused(self) -> bool:
        return (
            self._player.playbackState()
            == QMediaPlayer.PlaybackState.PausedState
        )

    @pyqtProperty(bool, notify=playlistChanged)
    def hasSongs(self) -> bool:
        return bool(self._song_paths)

    @pyqtProperty(str, notify=statusChanged)
    def status(self) -> str:
        return self._status

    @pyqtProperty(str, notify=errorChanged)
    def errorMessage(self) -> str:
        return self._error_message

    @pyqtProperty(int, notify=volumeChanged)
    def volume(self) -> int:
        return round(self._audio_output.volume() * 100)

    @pyqtProperty(int, notify=positionChanged)
    def position(self) -> int:
        return int(self._player.position())

    @pyqtProperty(int, notify=durationChanged)
    def duration(self) -> int:
        return int(self._player.duration())

    @pyqtProperty(str, notify=positionChanged)
    def formattedPosition(self) -> str:
        return self._format_milliseconds(self._player.position())

    @pyqtProperty(str, notify=durationChanged)
    def formattedDuration(self) -> str:
        return self._format_milliseconds(self._player.duration())

    # ---------------------------------------------------------
    # Slots called from QML
    # ---------------------------------------------------------

    @pyqtSlot()
    def scan_songs(self) -> None:
        """
        Scan the assets/songs directory and rebuild the playlist.
        """

        self._songs_directory.mkdir(parents=True, exist_ok=True)

        previously_selected_path: Path | None = None

        if self._has_current_song():
            previously_selected_path = self._song_paths[self._current_index]

        discovered_songs = [
            file_path
            for file_path in self._songs_directory.iterdir()
            if file_path.is_file()
            and file_path.suffix.lower() in self._supported_extensions
        ]

        self._song_paths = sorted(
            discovered_songs,
            key=lambda path: path.name.lower(),
        )

        if not self._song_paths:
            self._current_index = -1
            self._player.stop()
            self._player.setSource(QUrl())
            self._set_status("No songs found")
            self._clear_error()
        elif (
            previously_selected_path is not None
            and previously_selected_path in self._song_paths
        ):
            self._current_index = self._song_paths.index(
                previously_selected_path
            )
            self._load_current_song()
            self._set_status("Ready")
            self._clear_error()
        else:
            self._current_index = 0
            self._load_current_song()
            self._set_status("Ready")
            self._clear_error()

        self.playlistChanged.emit()
        self.songChanged.emit()
        self.playbackChanged.emit()

    @pyqtSlot()
    def play(self) -> None:
        if not self._ensure_song_available():
            return

        if self.isPaused:
            self._player.play()
            return

        if self._player.source().isEmpty():
            self._load_current_song()

        self._player.play()

    @pyqtSlot()
    def pause(self) -> None:
        if not self._ensure_song_available():
            return

        if self.isPlaying:
            self._player.pause()

    @pyqtSlot()
    def toggle_play_pause(self) -> None:
        if self.isPlaying:
            self.pause()
        else:
            self.play()

    @pyqtSlot()
    def stop(self) -> None:
        self._player.stop()

        if self.hasSongs:
            self._set_status("Stopped")
        else:
            self._set_status("No songs found")

        self.playbackChanged.emit()

    @pyqtSlot()
    def next_song(self) -> None:
        if not self._ensure_song_available():
            return

        self._current_index = (
            self._current_index + 1
        ) % len(self._song_paths)

        self._load_current_song()
        self.songChanged.emit()
        self._player.play()

    @pyqtSlot()
    def previous_song(self) -> None:
        if not self._ensure_song_available():
            return

        self._current_index = (
            self._current_index - 1
        ) % len(self._song_paths)

        self._load_current_song()
        self.songChanged.emit()
        self._player.play()

    @pyqtSlot(int)
    def select_song(self, index: int) -> None:
        if index < 0 or index >= len(self._song_paths):
            self._set_error("The selected song number is invalid.")
            return

        self._current_index = index
        self._load_current_song()
        self.songChanged.emit()
        self._player.play()

    @pyqtSlot(int)
    def set_volume(self, volume_percentage: int) -> None:
        safe_volume = max(0, min(volume_percentage, 100))
        self._audio_output.setVolume(safe_volume / 100.0)
        self.volumeChanged.emit()

    @pyqtSlot(int)
    def set_position(self, position_milliseconds: int) -> None:
        safe_position = max(
            0,
            min(position_milliseconds, self._player.duration()),
        )
        self._player.setPosition(safe_position)

    # ---------------------------------------------------------
    # Internal player handlers
    # ---------------------------------------------------------

    def _handle_playback_state_changed(
        self,
        state: QMediaPlayer.PlaybackState,
    ) -> None:
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self._set_status("Playing")
        elif state == QMediaPlayer.PlaybackState.PausedState:
            self._set_status("Paused")
        elif state == QMediaPlayer.PlaybackState.StoppedState:
            if self.hasSongs and self._status not in {
                "Loading",
                "Playback error",
            }:
                self._set_status("Stopped")

        self.playbackChanged.emit()

    def _handle_media_status_changed(
        self,
        media_status: QMediaPlayer.MediaStatus,
    ) -> None:
        if media_status == QMediaPlayer.MediaStatus.LoadingMedia:
            self._set_status("Loading")
        elif media_status == QMediaPlayer.MediaStatus.LoadedMedia:
            if not self.isPlaying:
                self._set_status("Ready")
        elif media_status == QMediaPlayer.MediaStatus.InvalidMedia:
            self._set_status("Playback error")
        elif media_status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.next_song()

    def _handle_position_changed(
        self,
        _position,
    ) -> None:

        self.positionChanged.emit()


    def _handle_duration_changed(
        self,
        _duration,
    ) -> None:

        self.durationChanged.emit()

    def _handle_error(
        self,
        error
    ):

        error_string = self._player.errorString()

        if error == QMediaPlayer.Error.NoError:
            self._clear_error()
            return

        readable_error = error_string.strip()

        if not readable_error:
            readable_error = "Unknown media error"

        self._set_error(
            readable_error
        )

        self._set_status(
            "Playback error"
        )

    # ---------------------------------------------------------
    # Internal helper methods
    # ---------------------------------------------------------

    def _load_current_song(self) -> None:
        if not self._has_current_song():
            self._player.setSource(QUrl())
            return

        song_path = self._song_paths[self._current_index]
        self._player.setSource(QUrl.fromLocalFile(str(song_path)))
        self._clear_error()

    def _ensure_song_available(self) -> bool:
        if not self._song_paths:
            self._set_error(
                "No supported songs were found in app/assets/songs."
            )
            self._set_status("No songs found")
            return False

        if not self._has_current_song():
            self._current_index = 0
            self._load_current_song()
            self.songChanged.emit()

        return True

    def _has_current_song(self) -> bool:
        return (
            bool(self._song_paths)
            and 0 <= self._current_index < len(self._song_paths)
        )

    def _set_status(self, status: str) -> None:
        if self._status == status:
            return

        self._status = status
        self.statusChanged.emit()

    def _set_error(self, message: str) -> None:
        if self._error_message == message:
            return

        self._error_message = message
        self.errorChanged.emit()

    def _clear_error(self) -> None:
        if not self._error_message:
            return

        self._error_message = ""
        self.errorChanged.emit()

    @staticmethod
    def _format_milliseconds(milliseconds: int) -> str:
        total_seconds = max(0, int(milliseconds // 1000))
        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)

        if hours:
            return f"{hours}:{minutes:02d}:{seconds:02d}"

        return f"{minutes:02d}:{seconds:02d}"