import QtQuick
import QtQuick.Layouts
import QtQuick.Controls.Basic
import "core"

Window {
    width: 303
    height: 423
    visible: true
    title: "Lab_4"

    property int btnHeight: 51;

    property int gap: 20;
    property int rowEntry: btnHeight + gap

    property int firstRow: rowEntry;
    property int secondRow: firstRow + rowEntry;
    property int thirdRow: secondRow + rowEntry;
    property int fourthRow: thirdRow + rowEntry;

    Button {
        id: oneButton
        x: 40; y: firstRow; width: 57; height: btnHeight
        buttonColor: "red"; altColor: "lightblue";

        buttonWidth: 100; buttonHeight: 100
        onButtonClick: { tmpColor = buttonColor; buttonColor = altColor; altColor = tmpColor }
    }

    Button {
        id: twoButton
        x: 121; y: firstRow; width: 57; height: btnHeight

        buttonWidth: 100; buttonHeight: 100
        onButtonClick: { tmpColor = buttonColor; buttonColor = altColor; altColor = tmpColor }
    }

    Button {
        id: threeButton
        x: 201; y: firstRow; width: 57; height: btnHeight

        buttonWidth: 100; buttonHeight: 100
        onButtonClick: { tmpColor = buttonColor; buttonColor = altColor; altColor = tmpColor }
    }

    Button {
        id: fourButton
        x: 40; y: secondRow; width: 57; height: btnHeight

        buttonWidth: 100; buttonHeight: 100
        onButtonClick: { tmpColor = buttonColor; buttonColor = altColor; altColor = tmpColor }
    }

    Button {
        id: fiveButton
        x: 121; y: secondRow; width: 57; height: btnHeight

        buttonWidth: 100; buttonHeight: 100
        onButtonClick: { tmpColor = buttonColor; buttonColor = altColor; altColor = tmpColor }
    }

    Button {
        id: sixButton
        x: 201; y: secondRow; width: 57; height: btnHeight

        buttonWidth: 100; buttonHeight: 100
        onButtonClick: { tmpColor = buttonColor; buttonColor = altColor; altColor = tmpColor }
    }

    Button {
        id: sevenButton
        x: 40; y: thirdRow; width: 57; height: btnHeight

        buttonWidth: 100; buttonHeight: 100
        onButtonClick: { tmpColor = buttonColor; buttonColor = altColor; altColor = tmpColor }
    }

    Button {
        id: eightButton
        x: 121; y: thirdRow; width: 57; height: btnHeight

        buttonWidth: 100; buttonHeight: 100
        onButtonClick: { tmpColor = buttonColor; buttonColor = altColor; altColor = tmpColor }
    }

    Button {
        id: nineButton
        x: 201; y: thirdRow; width: 57; height: btnHeight

        buttonWidth: 100; buttonHeight: 100
        onButtonClick: { tmpColor = buttonColor; buttonColor = altColor; altColor = tmpColor }
    }

    Button {
        id: tenButton
        x: 40; y: fourthRow; width: 57; height: btnHeight

        buttonWidth: 100; buttonHeight: 100
        onButtonClick: { tmpColor = buttonColor; buttonColor = altColor; altColor = tmpColor }
    }

    Button {
        id: elevenButton
        x: 121; y: fourthRow; width: 57; height: btnHeight

        buttonWidth: 100; buttonHeight: 100
        onButtonClick: { tmpColor = buttonColor; buttonColor = altColor; altColor = tmpColor }
    }

    Button {
        id: twelveButton
        x: 201; y: fourthRow; width: 57; height: btnHeight

        buttonWidth: 100; buttonHeight: 100
        onButtonClick: { tmpColor = buttonColor; buttonColor = altColor; altColor = tmpColor }
    }
}