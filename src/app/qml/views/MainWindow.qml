import QtQuick 2.9
import QtQuick.Window 2.3
import QtQuick.Controls 2.3
import QtQuick.Controls.Material 2.2
import QtQuick.Layouts 1.3
import QtQuick.Scene3D 2.0
import Qt.labs.settings 1.0
import Qt.labs.platform 1.0
import koki.katonalab.a3dc 1.0

import "../actions"
import "../stores"
import "sidebar"
import "display"
import "components"

ApplicationWindow {
    id: appWindow

    width: 480
    height: 480
    title: "A3DC - KatonaLab KOKI MTA (" + A3DCVersion.version() + ")"

    Material.theme: Material.Light
    Material.accent: Material.Teal

    Component.onCompleted: visible = true

    MenuBar {
        Menu {
            title: "File"
            MenuItem {
                text: importAction.text
                onTriggered: importAction.onTriggered();
            }
        }
    }

    // header: ToolBar {
    //     RowLayout {
    //         anchors.fill: parent
    //         Button {
    //             text: "\uE807"
    //             action: importAction
    //         }
    //     }
    // }

    footer: Rectangle {
        // TODO
        height: 16
    }

    Settings {
        property alias x: appWindow.x
        property alias y: appWindow.y
        property alias width: appWindow.width
        property alias height: appWindow.height
    }

    Action {
        id: importAction
        text: "Import"
        onTriggered: {
            AppActions.importIcsFile({});
        }
    }

    RowLayout {
        anchors.fill: parent
        spacing: 0

        CardPanel {
            Layout.preferredWidth: 300
            Layout.fillHeight: true
            model: MainStore.cardStore.model
            supportedModules: MainStore.moduleStore.supportedModules
        }

        Scene3D {
            Layout.fillWidth: true
            Layout.fillHeight: true
            // prevent errors when shrinked size 0
            Layout.minimumWidth: 128
            Layout.minimumHeight: 128

            aspects: ["input", "logic"]
            cameraAspectRatioMode: Scene3D.AutomaticAspectRatio

            SceneRootEntity {}
        }
    }

}