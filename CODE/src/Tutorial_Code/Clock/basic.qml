import QtQuick 2.5
import QtQuick.Controls 1.4
import Qt 5.7

ApplicationWindow {

    width: 300
    height: 200
    title: "Simple"

    Text {

        text: "Qt Quick"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        font.pointSize: 24; font.bold: true
    }
}