import QtQuick 2.8
import Qt3D.Core 2.0
import Qt3D.Render 2.0
import Qt3D.Extras 2.0
import Qt3D.Input 2.0
import koki.katonalab.a3dc 1.0

import "../../stores"

Entity {
    id: root
    property size viewPortSize: Qt.size(1, 1);
    property var baseModel

    components: [
        SceneRenderSettings {
            id: renderSettings
            camera: sceneCamera
            clearColor: Qt.rgba(0.2, 0.2, 0.2, 1.0)
            renderSize: Qt.size(width, height)
            sceneLayer: sceneLayer
            screenQuadLayer: screenQuadLayer
        },
        InputSettings {}
    ]

    Camera {
        id: sceneCamera
        projectionType: CameraLens.PerspectiveProjection
        fieldOfView: 45
        aspectRatio: 3/4
        nearPlane : 0.1
        farPlane : 100.0
        position: Qt.vector3d(0.0, 0.0, -2.0)
        upVector: Qt.vector3d(0.0, 1.0, 0.0)
        viewCenter: Qt.vector3d(0.0, 0.0, 0.0)
    }

    TurnTableCameraController {
        camera: sceneCamera
        viewPortSize: root.viewPortSize
        rollBallRadius: viewPortSize.width * 0.4
        lookSpeed: 180
        linearSpeed: 1
        zoomMax: 10
    }

    // TODO: find a way to do the rendering like this:
    // 
    // for 3d_objects:
    //   do_backface_render -> backfacebuffer
    //   do_frontface_render(backfacebuffer) -> accum buffer
    // render_accum_buffer
    // 
    // so we need a per object volume rendering and then merging the results

    NodeInstantiator {
        model: BackendStoreFilter {
            source: baseModel
            includeCategory: ["output"]
            includeType: ["float-image"]
            includeStatus: [1]
        }

        delegate: VolumeEntity {
            uid: model.uid

            // arbitrary size scaling
            property real scale: 1.0/512.0

            width: model.value.size.x * scale
            height: model.value.size.y * scale
            depth: model.value.size.z * scale
            volumeTexture: model.value.texture

            Binding {
                target: model.value.texture
                property: "smooth"
                value: baseModel.smoothTextures
            }

            Connections {
                target: model
                // onStatusChanged: console.log("status changed", model.status)
            }

            Component.onCompleted: {
                lutDataMax = 1.;
            }

            backFaceMap: renderSettings.backFaceMap
            // TODO: count only the visible channels
            // accumDivisor: 1.0 / MainStore.moduleStore.model.count
            accumDivisor: 1.0
            layer: sceneLayer

            // note: JSValue to QColor conversion
            volumeColor: Qt.rgba(model.value.color.r, model.value.color.g, model.value.color.b, model.value.color.a);
            visible: model.value.visible && model.status == 1
            labeled: false

            lutLowCut: model.value.lutParams.x
            lutHighCut: model.value.lutParams.y
        }
    }

    Layer {
        id: screenQuadLayer
    }

    Layer {
        id: sceneLayer
    }

    ScreenQuadEntity {
        layer: screenQuadLayer
        frontFaceAccumulatorMap: renderSettings.frontFaceAccumulatorMap
    }
}
