import QtQuick 2.8
import QtQuick.Window 2.0
import QtQuick.Controls 1.5
import QtQuick.Layouts 1.1

import "../actions"
import "../stores"
import "controls"

GroupBox {

    Action {
        id: addSegmentationNode
        text: "Add Segmentation"
        onTriggered: AppActions.addSegmentNode(AppActions.generateUid())
    }

    Action {
        id: addAnalysisNode
        text: "Add Analysis"
        onTriggered: AppActions.addAnalysisNode(AppActions.generateUid())
    }

    Action {
        id: addFakeAnalysisNode
        text: "Add Analysis 2"
        onTriggered: AppActions.addFakeAnalysisNode(AppActions.generateUid())
    }

    ScrollView {
        anchors.fill: parent

        ColumnLayout {
            width: parent.parent.width
            //width: 150
            ColumnLayout {
                anchors.fill: parent
                spacing: 4

                Repeater {
                    model: MainStore.nodeStore.model
                    delegate: Loader {
                        Layout.fillWidth: true
                        onLoaded: {
                            item.uid = model.uid;
                            item.nodeName = model.nodeName;
                            item.nodeViewParams = model.nodeViewParams;
                            item.nodeApplied = Qt.binding(function(){return model.nodeApplied});
                        }
                        source: model.nodeViewPath
                    }
                }
            }

            FontelloButton {
                text: "\uE827"
                Layout.fillWidth: true
                onClicked: {
                    menu.popup();
                }

                Menu {
                    id: menu
                    MenuItem { action: addSegmentationNode }
                    MenuItem { action: addAnalysisNode }
                    MenuItem { action: addFakeAnalysisNode }
                }
            }
        }
    }
}
