import QtQuick
import QtQuick.Controls
import QtQuick.Window

ApplicationWindow {
    id: applicationWindow

    width: configuredWindowWidth
    height: configuredWindowHeight

    minimumWidth: 800
    minimumHeight: 480

    visible: true
    title: appName
    color: "#06090E"

    MusicScreen {
        anchors.fill: parent
    }
}