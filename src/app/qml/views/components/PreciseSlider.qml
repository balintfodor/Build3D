import QtQuick 2.0
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

RowLayout {
    property int decimals: 4
    property alias from: slider.from
    property alias to: slider.to
    property alias value: slider.value
    property alias editWidth: field.implicitWidth
    property alias stepSize: slider.stepSize
    property alias snapMode: slider.snapMode
    property alias text: label.text

    Label {
        id: label
    }

    RowLayout {
        Layout.fillWidth: true

        Slider {
            id: slider
            Layout.fillWidth: true
            onValueChanged: {
                field.text = Number(value.toFixed(decimals)).toLocaleString();
            }
        }

        TextField {
            id: field
            horizontalAlignment: TextInput.AlignRight
            Layout.alignment: Qt.AlignRight
            validator: DoubleValidator {}
            onEditingFinished: {
                slider.value = Number.fromLocaleString(text);
            }
        }
    }
}

