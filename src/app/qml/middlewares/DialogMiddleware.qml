import QtQuick 2.8
import QtQuick.Dialogs 1.2

import "../actions"

Middleware {
    id: middleware

    property url folder: "."
    property int tmpUid: -1;

    function dispatch(actionType, args) {
        var handlers = {};
        handlers[ActionTypes.ics_file_import] = function(args) {
            openDialog.open();
        };

        handlers[ActionTypes.module_remove_request] = function(args) {
            middleware.tmpUid = args.uid;
            moduleRemoveDialog.open();
        };

        var notHandled = function(args) {
            next(actionType, args);
        };
        (handlers[actionType] || notHandled)(args);
    }

    FileDialog {
        id: openDialog
        title: "Import"
        folder: middleware.folder
        selectMultiple: false
        nameFilters: [ "Image Cytometry Standard (*.ics)" ]
        onAccepted: {
            console.debug(openDialog.fileUrl);
            next(ActionTypes.ics_file_import, {url: openDialog.fileUrl});
        }
    }

    Dialog {
        id: moduleRemoveDialog
        visible: false
        title: "Removal Confirmation"
        standardButtons: StandardButton.Yes | StandardButton.No

        Text {
            text: "Remove?" // TODO: proper message
        }

        onYes: {
            next(ActionTypes.module_remove_request, {uid: middleware.tmpUid});
            middleware.tmpUid = -1;
        }
    }
}
