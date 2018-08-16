import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQml 2.2
import QtQml.Models 2.2
import QtQuick.Controls.Material 2.2
import koki.katonalab.a3dc 1.0

import "../../actions"
import "../../stores"

Pane {
    id: root
    property var supportedModules
    property var baseModel
    property bool configurationUpToDate: true

    padding: 12

    BackendStoreFilter {
        id: moduleList
        source: baseModel
        includeCategory: ["module"]
    }

    ListView {
        id: listView

        anchors.fill: parent
        spacing: 8

        model: moduleList
        delegate: Card {
            moduleDetails: model

            BackendStoreFilter {
                id: inputsModel
                source: baseModel
                includeCategory: ["input"]
                includeParentUid: [model.uid]
            }

            BackendStoreFilter {
                id: parametersModel
                source: baseModel
                includeCategory: ["parameter"]
                includeParentUid: [model.uid]
            }

            BackendStoreFilter {
                id: outputsModel
                source: baseModel
                includeCategory: ["output"]
                includeParentUid: [model.uid]
            }

            inputs: inputsModel
            parameters: parametersModel
            outputs: outputsModel
            width: parent.width
            expanded: true
            font.pointSize: 11
        }

        header: Column {
            anchors.horizontalCenter: parent.horizontalCenter
            RoundButton {
                text: "run"
                onClicked: {
                    MainStore.moduleStore.model.evaluate(-1);
                }
                Material.background: configurationUpToDate ? Material.LightGreen : Material.Amber
            }

            Rectangle { color: "transparent"; height: 16; width: 1 }
        }

        footer: Column {
            anchors.horizontalCenter: parent.horizontalCenter

            Rectangle { color: "transparent"; height: 16; width: 1 }

            RoundButton {
                text: "+"
                onClicked: {
                    menu.open();
                }

                Menu {
                    id: menu
                    width: 300
                    Menu {
                        id: defaultToolsMenu
                        title: "general"
                        MenuItem {
                            text: "import ics"
                            onTriggered: {
                                AppActions.importIcsFile({});
                            }
                        }
                    }
                    MenuSeparator {}

                    Instantiator {
                        model: supportedModules
                        Menu {
                            id: subMenu
                            title: displayName
                            width: 300
                            Component.onCompleted: {
                                // TODO: find an off-the-shelf solution, this is bad
                                for (var i = 0; i < files.count; ++i) {
                                    for(var j = 0; j < i; ++j) {
                                        if(files.get(i).displayName < files.get(j).displayName) {
                                            files.move(i, j, 1)
                                        }
                                    }
                                }

                                // TODO: find a nicer QML-way to generate the submenu items
                                for (var i = 0; i < files.count; ++i) {
                                    insertItem(-1, Qt.createQmlObject('\
                                        import QtQuick 2.9; \
                                        import QtQuick.Controls 2.2; \
                                        import "../../actions"; \
                                        MenuItem { \
                                            text: "' + files.get(i).displayName + '"; \
                                            onTriggered: {AppActions.requestAddModule("' + files.get(i).path + '");} \
                                        }', subMenu));
                                }
                            }
                        }
                        onObjectAdded: menu.insertMenu(2, object)
                        onObjectRemoved: menu.removeMenu(object)
                    }

                    MenuSeparator {}
                    MenuItem {
                        text: "refresh module list"
                        onTriggered: {
                            AppActions.refreshModuleList();
                        }
                    }
                }
            }
        }
    }
}
