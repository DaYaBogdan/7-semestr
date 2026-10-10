import QtQuick
import QtQuick.Controls
import Game 1.0
import QtQuick.Dialogs
import QtQuick.Layouts

ApplicationWindow {
    visible: true
    width: 640
    height: 480
    title: "Игровое поле"

    FieldController {
            id: field

            fieldWidth:  10
            fieldHeight: 10
        }

    function buildModel() {
        let m = []
        for (let y = 0; y < field.height; ++y)
            for (let x = 0; x < field.width; ++x)
                m.push({ x: x, y: y, v: field.getCell(x, y) })
        return m
    }

    Grid {
        id: grid
        anchors.centerIn: parent
        columns: field.width
        spacing: 2

        Repeater {
            model: field.cells.length

            Rectangle {
                id: cellRect
                required property int index
                property int cx: index % field.width
                property int cy: Math.floor(index / field.width)

                width: 30; height: 30
                border.color: "#888"
                border.width: 1


                color: {
                    let dummy = field.cells
                    return field.getCell(cx, cy) === 1 ? "#4a90d9" : "#eeeeee"
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        let v = field.getCell(cellRect.cx, cellRect.cy)
                        field.setCell(cellRect.cx, cellRect.cy, v === 1 ? 0 : 1)
                    }
                }
            }
        }
    }

    footer: ToolBar {
        RowLayout {
            anchors.fill: parent
            spacing: 6

            Label {
                text: "Ширина:"
                Layout.leftMargin: 12}
            SpinBox {
                from: 1; to: 50
                value: field.fieldWidth
                onValueModified: field.fieldWidth = value
            }

            Label {
                text: "Высота:"
                Layout.leftMargin: 12}
            SpinBox {
                from: 1; to: 50
                value: field.fieldHeight
                onValueModified: field.fieldHeight = value
            }

            Button { text: "Сохранить"; onClicked: saveDialog.open() }
            Button { text: "Загрузить"; onClicked: loadDialog.open() }
            Button { text: "Очистить";  onClicked: field.fill(0) }
        }
    }

    FileDialog {
        id: saveDialog
        title: "Куда сохранить"
        fileMode: FileDialog.SaveFile
        nameFilters: ["Текстовые файлы (*.txt)"]
        onAccepted: field.save(selectedFile.toString().replace("file:///", ""))
    }

    FileDialog {
        id: loadDialog
        title: "Откуда загрузить"
        fileMode: FileDialog.OpenFile
        nameFilters: ["Текстовые файлы (*.txt)"]
        onAccepted: field.load(selectedFile.toString().replace("file:///", ""))
    }
}

