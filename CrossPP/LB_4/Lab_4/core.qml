import QtQuick 2.0

Rectangle {
 id: button
 property int buttonHeight: 75
 property int buttonWidth: 150

 property string label
 property color textColor: buttonLabel.color

 property color onHoverColor: "lightsteelblue"
 property color borderColor: "transparent"

 property color buttonColor: "lightblue"

 property real labelSize: 14

 radius: 6
 antialiasing: true
 border { width: 2; color: borderColor }
 width: buttonWidth; height: buttonHeight

 Text {
 id: buttonLabel
 anchors.centerIn: parent
 text: label
 color: "#000000"
 font.pointSize: labelSize
 }

 signal buttonClick()

 MouseArea {
 id: buttonMouseArea
 anchors.fill: parent
 onClicked: buttonClick()

 hoverEnabled: true

 onEntered: parent.border.color = onHoverColor
 onExited: parent.border.color = borderColor
 }

 color: buttonMouseArea.pressed ? Qt.darker(buttonColor, 1.5) : buttonColor
 Behavior on color { ColorAnimation{ duration: 55 } }

 scale: buttonMouseArea.pressed ? 1.1 : 1.00
 Behavior on scale { NumberAnimation{ duration: 55 }}
}
