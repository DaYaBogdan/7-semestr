import QtQuick 2.15

Rectangle {
 id: button
 property int buttonHeight: 75
 property int buttonWidth: 150

 property color onHoverColor: "lightsteelblue"
 property color borderColor: "transparent"

 property color buttonColor: "lightblue"
 property color altColor: "red"
 property color tmpColor: "lightblue";

 radius: 6
 antialiasing: true
 border { width: 2; color: borderColor }
 width: buttonWidth; height: buttonHeight

 signal buttonClick()

 MouseArea {
 id: buttonMouseArea
 anchors.fill: parent
 onClicked: buttonClick()

 hoverEnabled: true

 onEntered: parent.border.color = onHoverColor
 onExited: parent.border.color = borderColor
 }

 color: buttonMouseArea.pressed ? altColor : buttonColor
 Behavior on color { ColorAnimation { duration: 55 } }

 scale: buttonMouseArea.pressed ? 1.1 : 1.00
 Behavior on scale { NumberAnimation{ duration: 55 }}
}
