from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from PyQt6.QtCore import QCoreApplication
from PyQt6.QtWidgets import QApplication

# -------------------------------------------------
# Project Paths
# -------------------------------------------------
APP_DIRECTORY = Path(__file__).resolve().parent
CONFIG_FILE = APP_DIRECTORY / "config" / "app_config.json"
SONGS_DIRECTORY = APP_DIRECTORY / "assets" / "songs"


def load_configuration() -> dict[str, Any]:
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Configuration file not found:\n{CONFIG_FILE}")

    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as file:
            configuration = json.load(file)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Invalid JSON:\n{error}")

    required_keys = {
        "application_name",
        "version",
        "window_width",
        "window_height",
        "default_volume",
        "supported_audio_extensions",
    }

    missing = required_keys.difference(configuration.keys())
    if missing:
        raise RuntimeError(f"Missing configuration values:\n{missing}")

    return configuration


def main():
    # 1. CRITICAL: Initialize QApplication before doing ANYTHING else
    app = QApplication(sys.argv)

    # 2. Defer module imports until after QApplication is safely alive in memory.
    # This prevents hidden global widgets in UI files from causing core dumps.
    from controllers.music_controller import MusicController
    from screens.main_window import MainWindow
    from screens.splash_screen import SplashScreen

    try:
        configuration = load_configuration()
    except (FileNotFoundError, RuntimeError) as error:
        print(error)
        return 1

    application_name = str(configuration["application_name"])
    application_version = str(configuration["version"])

    QCoreApplication.setOrganizationName("AICarProject")
    QCoreApplication.setApplicationName(application_name)
    QCoreApplication.setApplicationVersion(application_version)

    # 3. Initialize the audio controller safely
    music_controller = MusicController(
        songs_directory=SONGS_DIRECTORY,
        supported_extensions=list(configuration["supported_audio_extensions"]),
        default_volume=int(configuration["default_volume"]),
    )

    # 4. Spin up and display your main window
    window = MainWindow(configuration, music_controller)
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())