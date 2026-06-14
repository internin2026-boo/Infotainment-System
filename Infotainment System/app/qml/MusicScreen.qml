import QtQuick
import QtQuick.Controls
import "controls"

Item {
    id: root

    property bool userIsMovingProgress: false

    Rectangle {
        anchors.fill: parent
        color: "#06090E"
    }

    Column {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 14

        // -------------------------------------------------
        // Header
        // -------------------------------------------------

        Row {
            width: parent.width
            height: 42
            spacing: 12

            Column {
                width: parent.width * 0.70
                spacing: 2

                Text {
                    text: appName
                    color: "#3DB8FF"
                    font.pixelSize: 25
                    font.bold: true
                }

                Text {
                    text: "Touchscreen Music Player"
                    color: "#7F96AD"
                    font.pixelSize: 13
                }
            }

            Column {
                width: parent.width * 0.30 - 12
                spacing: 2

                Text {
                    id: clockText

                    width: parent.width
                    text: Qt.formatTime(new Date(), "hh:mm AP")
                    color: "#FFFFFF"
                    font.pixelSize: 20
                    font.bold: true
                    horizontalAlignment: Text.AlignRight
                }

                Text {
                    width: parent.width
                    text: Qt.formatDate(new Date(), "dd MMM yyyy")
                    color: "#7F96AD"
                    font.pixelSize: 12
                    horizontalAlignment: Text.AlignRight
                }
            }
        }

        Timer {
            interval: 1000
            running: true
            repeat: true

            onTriggered: {
                clockText.text = Qt.formatTime(
                    new Date(),
                    "hh:mm AP"
                )
            }
        }

        // -------------------------------------------------
        // Song information card
        // -------------------------------------------------

        Rectangle {
            width: parent.width
            height: 108
            radius: 20
            color: "#101923"
            border.width: 1
            border.color: "#22354A"

            Row {
                anchors.fill: parent
                anchors.margins: 16
                spacing: 18

                Rectangle {
                    width: 72
                    height: 72
                    radius: 16
                    color: "#173B5C"

                    Text {
                        anchors.centerIn: parent
                        text: "♫"
                        color: "#51C3FF"
                        font.pixelSize: 38
                        font.bold: true
                    }
                }

                Column {
                    width: parent.width - 190
                    anchors.verticalCenter: parent.verticalCenter
                    spacing: 6

                    Text {
                        width: parent.width
                        text: musicController.currentTitle
                        color: "#FFFFFF"
                        font.pixelSize: 25
                        font.bold: true
                        elide: Text.ElideRight
                    }

                    Text {
                        width: parent.width

                        text: musicController.hasSongs
                              ? "Song "
                                + (musicController.currentIndex + 1)
                                + " of "
                                + musicController.songCount
                              : "Add music files to app/assets/songs"

                        color: "#8EA4B9"
                        font.pixelSize: 14
                        elide: Text.ElideRight
                    }

                    Text {
                        width: parent.width
                        text: musicController.status
                        color: musicController.errorMessage.length > 0
                               ? "#FF6B6B"
                               : "#45D49B"
                        font.pixelSize: 14
                        font.bold: true
                    }
                }

                ControlButton {
                    width: 82
                    height: 50
                    anchors.verticalCenter: parent.verticalCenter
                    text: "Scan"

                    onClicked: {
                        musicController.scan_songs()
                    }
                }
            }
        }

        // -------------------------------------------------
        // Song progress
        // -------------------------------------------------

        Rectangle {
            width: parent.width
            height: 70
            radius: 17
            color: "#0D151E"
            border.width: 1
            border.color: "#1D2E40"

            Column {
                anchors.fill: parent
                anchors.margins: 10
                spacing: 4

                Slider {
                    id: progressSlider

                    width: parent.width
                    from: 0
                    to: Math.max(musicController.duration, 1)

                    value: root.userIsMovingProgress
                           ? value
                           : musicController.position

                    enabled: musicController.hasSongs
                             && musicController.duration > 0

                    onPressedChanged: {
                        root.userIsMovingProgress = pressed

                        if (!pressed) {
                            musicController.set_position(
                                Math.round(value)
                            )
                        }
                    }
                }

                Row {
                    width: parent.width

                    Text {
                        width: parent.width / 2
                        text: musicController.formattedPosition
                        color: "#8EA4B9"
                        font.pixelSize: 13
                    }

                    Text {
                        width: parent.width / 2
                        text: musicController.formattedDuration
                        color: "#8EA4B9"
                        font.pixelSize: 13
                        horizontalAlignment: Text.AlignRight
                    }
                }
            }
        }

        // -------------------------------------------------
        // Playback controls
        // -------------------------------------------------

        Row {
            width: parent.width
            height: 68
            spacing: 12

            ControlButton {
                width: (parent.width - 48) / 5
                height: parent.height
                text: "Previous"
                enabled: musicController.hasSongs

                onClicked: {
                    musicController.previous_song()
                }
            }

            ControlButton {
                width: (parent.width - 48) / 5
                height: parent.height

                text: musicController.isPlaying
                      ? "Pause"
                      : "Play"

                normalColor: "#0D4F7D"
                hoverColor: "#12679F"
                pressedColor: "#168BD4"
                enabled: musicController.hasSongs

                onClicked: {
                    musicController.toggle_play_pause()
                }
            }

            ControlButton {
                width: (parent.width - 48) / 5
                height: parent.height
                text: "Next"
                enabled: musicController.hasSongs

                onClicked: {
                    musicController.next_song()
                }
            }

            ControlButton {
                width: (parent.width - 48) / 5
                height: parent.height
                text: "Stop"
                enabled: musicController.hasSongs

                onClicked: {
                    musicController.stop()
                }
            }

            ComboBox {
                id: songSelector

                width: (parent.width - 48) / 5
                height: parent.height

                enabled: musicController.hasSongs
                model: musicController.songTitles
                currentIndex: musicController.currentIndex

                displayText: musicController.hasSongs
                             ? "Songs"
                             : "No Songs"

                onActivated: function(index) {
                    musicController.select_song(index)
                }
            }
        }

        // -------------------------------------------------
        // Volume section
        // -------------------------------------------------

        Rectangle {
            width: parent.width
            height: 64
            radius: 17
            color: "#101923"
            border.width: 1
            border.color: "#22354A"

            Row {
                anchors.fill: parent
                anchors.margins: 12
                spacing: 14

                Text {
                    width: 75
                    anchors.verticalCenter: parent.verticalCenter
                    text: "Volume"
                    color: "#FFFFFF"
                    font.pixelSize: 17
                    font.bold: true
                }

                Slider {
                    id: volumeSlider

                    width: parent.width - 165
                    anchors.verticalCenter: parent.verticalCenter

                    from: 0
                    to: 100
                    stepSize: 1
                    value: musicController.volume

                    onMoved: {
                        musicController.set_volume(
                            Math.round(value)
                        )
                    }
                }

                Text {
                    width: 48
                    anchors.verticalCenter: parent.verticalCenter

                    text: Math.round(volumeSlider.value) + "%"
                    color: "#8EA4B9"
                    font.pixelSize: 15
                    horizontalAlignment: Text.AlignRight
                }
            }
        }

        // -------------------------------------------------
        // Error and footer
        // -------------------------------------------------

        Text {
            width: parent.width
            height: 18

            text: musicController.errorMessage
            visible: text.length > 0

            color: "#FF6B6B"
            font.pixelSize: 13
            horizontalAlignment: Text.AlignHCenter
            elide: Text.ElideRight
        }

        Text {
            width: parent.width

            text: "Version "
                  + appVersion
                  + " | Python + PySide6 + QML"

            color: "#53677B"
            font.pixelSize: 12
            horizontalAlignment: Text.AlignHCenter
        }
    }
}