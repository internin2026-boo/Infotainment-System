import QtQuick
import QtQuick.Controls

Button {
    id: control

    property color normalColor: "#18263A"
    property color hoverColor: "#213550"
    property color pressedColor: "#1976D2"
    property color disabledColor: "#111923"
    property color outlineColor: "#304560"

    implicitWidth: 150
    implicitHeight: 64

    font.pixelSize: 18
    font.bold: true

    hoverEnabled: true

    background: Rectangle {
        radius: 16

        color: {
            if (!control.enabled) {
                return control.disabledColor
            }

            if (control.down) {
                return control.pressedColor
            }

            if (control.hovered) {
                return control.hoverColor
            }

            return control.normalColor
        }

        border.width: 1
        border.color: control.enabled
                      ? control.outlineColor
                      : "#1D2835"

        Behavior on color {
            ColorAnimation {
                duration: 100
            }
        }
    }

    contentItem: Text {
        text: control.text
        color: control.enabled ? "#F7FAFC" : "#667789"
        font: control.font
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }
}