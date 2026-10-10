import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts

ApplicationWindow {
    id: window
    width: 640
    height: 480
    minimumWidth: 200
    minimumHeight: 250
    visible: true
    title: qsTr("Lab_5")

    ColumnLayout {
        anchors.fill: parent
        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
        }

        TextField {
            id: stateField
            x: 20
            y: 20
            Layout.fillWidth: true
            height: 40
            placeholderText: "Состояние игрового поля"
            text: gameField.field
            onTextEdited: gameField.field = text
        }

        Connections {
            target: gameField
            function onFieldChanged() {
                stateField.text = gameField.field
            }
        }

        RowLayout {
            Button {
                id: saveButton
                Layout.fillWidth: true
                y: 93
                width: 100
                height: 51
                text: "Save"
                onClicked: gameField.saveToFile()
            }

            Button {
                id: loadButton
                Layout.fillWidth: true
                y: 163
                width: 100
                height: 51
                text: "Load"
                onClicked: gameField.loadFromFile()
            }
        }
        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }

}