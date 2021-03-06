#ifndef _app_BackendOutput_h_
#define _app_BackendOutput_h_

#include "BackendStoreItem.h"
#include <QObject>
#include <core/compute_platform/ComputeModule.h>
#include <core/multidim_image_platform/MultiDimImage.hpp>
#include "OutputInterfaceModules.hpp"
#include <QColor>
#include <QVector2D>
#include <QVector3D>
#include "VolumeTexture.h"
#include <QJsonValue>

// Helper class to enable handing over std::shared_ptr<MultiDimImage<float>>
// through signal/slots.
class ImageWrapper {
    template <typename T> using MultiDimImage = core::multidim_image_platform::MultiDimImage<T>;
public:
    std::shared_ptr<MultiDimImage<float>> m_image;
};
Q_DECLARE_METATYPE(ImageWrapper);

class ImageOutputValue: public QObject {
    Q_OBJECT
    Q_PROPERTY(VolumeTexture* texture READ texture NOTIFY textureChanged)
    Q_PROPERTY(bool textureReady READ textureReady NOTIFY textureReadyChanged)
    Q_PROPERTY(QVector3D size READ size NOTIFY sizeChanged)
    Q_PROPERTY(QColor color READ color WRITE setColor NOTIFY colorChanged)
    Q_PROPERTY(bool visible READ visible WRITE setVisible NOTIFY visibleChanged)
    Q_PROPERTY(QVector2D lutParams READ lutParams WRITE setLutParams NOTIFY lutParamsChanged)
    Q_PROPERTY(QVector2D lutLimits READ lutLimits NOTIFY lutLimitsChanged)
    template <typename T> using MultiDimImage = core::multidim_image_platform::MultiDimImage<T>;
public:
    ImageOutputValue(QObject* parent = nullptr);
    VolumeTexture* texture() const;
    bool textureReady() const;
    QVector3D size() const;
    QColor color() const;
    bool visible() const;
    QVector2D lutParams() const;
    QVector2D lutLimits() const;
    void setColor(QColor color);
    void setVisible(bool visible);
    void setLutParams(QVector2D lutParams);
    virtual ~ImageOutputValue();
    static QVariantMap convertToVariantMap(ImageOutputValue* x);
    QVariantMap toVariantMap() const;
    void fromVariantMap(QVariantMap vmap);
public Q_SLOTS:
    void setTextureFromImage(const ImageWrapper& wrapper);
    void setLutLimits(QVector2D lutLimits);
Q_SIGNALS:
    void textureChanged();
    void textureReadyChanged();
    void sizeChanged();
    void colorChanged();
    void visibleChanged();
    void lutParamsChanged();
    void lutLimitsChanged();
    void requestSetTextureFromImage(const ImageWrapper& wrapper);
    void requestSetLutLimits(QVector2D);
protected:
    std::shared_ptr<MultiDimImage<float>> m_image;
    VolumeTexture* m_texture = nullptr;
    bool m_textureReady = false;
    QColor m_color;
    bool m_visible = false;
    QVector2D m_lutParams = QVector2D(0, 0);
    QVector2D m_lutLimits = QVector2D(0, 0);
    void textureDeleted();
};

namespace details {
    QVector2D calculateLutLimits(std::shared_ptr<core::multidim_image_platform::MultiDimImage<float>> im);
}

class BackendOutput : public BackendStoreItem {
    typedef core::compute_platform::ComputePlatform ComputePlatform;
    typedef core::compute_platform::OutputPort OutputPort;
public:
    BackendOutput(std::weak_ptr<OutputPort> source, ComputePlatform& platform,
        int portId, int parentUid);
    int uid() const override;
    int parentUid() const override;
    QString category() const override;
    QString name() const override;
    QString type() const override;
    int status() const override;
    QVariant value() const override;
    QVariant hints() const override;
    void invalidate() override;

    void setName(const QString& name) override;
    void setStatus(int status) override;
    bool setValue(QVariant value) override;

    std::weak_ptr<OutputPort> source();
protected:
    std::weak_ptr<OutputPort> m_source;
    int m_portId = -1;
    int m_parentUid = -1;
    QVariantMap m_hints;
    QString m_type;
    bool m_ready = false;
    std::shared_ptr<ImageOutputInterfaceModule> m_interfaceModule;
    ImageOutputValue m_internalValue;
    void onExecuted();
};

namespace details {

    template <typename T>
    std::shared_ptr<ImageOutputInterfaceModule> buildImageOutput(
        core::compute_platform::ComputePlatform& platform)
    {
        return std::make_shared<TypedImageOutputInterfaceModule<T>>(platform);
    }

    typedef std::function<
        std::shared_ptr<ImageOutputInterfaceModule>
        (core::compute_platform::ComputePlatform&)> BuildOutputFunction;

    QColor waveLengthToQColor(double w, double gamma = 0.8);
}

#endif
