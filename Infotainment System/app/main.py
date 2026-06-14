from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

from PySide6.QtCore import QCoreApplication, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from controllers.music_controller import MusicController


APP_DIRECTORY = Path(__file__).resolve().parent
CONFIG_FILE = APP_DIRECTORY / "config" / "app_config.json"
QML_FILE = APP_DIRECTORY / "qml" / "Main.qml"
SONGS_DIRECTORY = APP_DIRECTORY / "assets" / "songs"


def load_configuration() -> dict[str, Any]:
    """
    Load application configuration from app_config.json.
    """

    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Configuration file was not found: {CONFIG_FILE}"
        )

    try:
        with CONFIG_FILE.open(
            "r",
            encoding="utf-8",
        ) as config_handle:
            configuration = json.load(config_handle)
    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"Configuration JSON is invalid: {error}"
        ) from error

    required_keys = {
        "application_name",
        "version",
        "window_width",
        "window_height",
        "default_volume",
        "supported_audio_extensions",
    }

    missing_keys = required_keys.difference(configuration.keys())

    if missing_keys:
        missing_names = ", ".join(sorted(missing_keys))
        raise RuntimeError(
            f"Configuration is missing these values: {missing_names}"
        )

    return configuration


def configure_graphics_environment() -> None:
    """
    Configure a stable graphics API for the desktop prototype.

    Later, the Raspberry Pi version will use Wayland/OpenGL ES settings.
    """

    os.environ.setdefault("QSG_RHI_BACKEND", "opengl")


def main() -> int:
    configure_graphics_environment()

    try:
        configuration = load_configuration()
    except (FileNotFoundError, RuntimeError) as error:
        print(f"Startup error: {error}", file=sys.stderr)
        return 1

    app = QGuiApplication(sys.argv)

    application_name = str(configuration["application_name"])
    application_version = str(configuration["version"])

    QCoreApplication.setOrganizationName("AICarProject")
    QCoreApplication.setApplicationName(application_name)
    QCoreApplication.setApplicationVersion(application_version)

    engine = QQmlApplicationEngine()

    music_controller = MusicController(
        songs_directory=SONGS_DIRECTORY,
        supported_extensions=list(
            configuration["supported_audio_extensions"]
        ),
        default_volume=int(configuration["default_volume"]),
    )

    context = engine.rootContext()
    context.setContextProperty(
        "musicController",
        music_controller,
    )
    context.setContextProperty(
        "appName",
        application_name,
    )
    context.setContextProperty(
        "appVersion",
        application_version,
    )
    context.setContextProperty(
        "configuredWindowWidth",
        int(configuration["window_width"]),
    )
    context.setContextProperty(
        "configuredWindowHeight",
        int(configuration["window_height"]),
    )

    engine.load(QUrl.fromLocalFile(str(QML_FILE)))

    if not engine.rootObjects():
        print(
            f"QML interface could not be loaded: {QML_FILE}",
            file=sys.stderr,
        )
        return 1

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())