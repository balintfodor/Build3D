#include "BackendOutput.h"

#include <tuple>
#include <string>

using namespace core::compute_platform;
using namespace std;

// TODO: move to separate file
VolumeTexture* ImageOutputValue::texture() const
{
    return m_texture;
}

QVector3D ImageOutputValue::size() const
{
    return m_texture ? m_texture->size() : QVector3D(0, 0, 0);
}

QColor ImageOutputValue::color() const
{
    return m_color;
}

bool ImageOutputValue::visible() const
{
    return m_visible;
}

QVector2D ImageOutputValue::lutParams() const
{
    return m_lutParams;
}

QColor details::waveLengthToQColor(double w, double gamma)
{
    // NOTE: from https://gist.github.com/friendly/67a7df339aa999e2bcfcfec88311abfc
    // all credits to the original author

    double R, G, B;
    if (w >= 380.0 && w <= 440.0) {
        double a = 0.3 + 0.7 * (w - 380.0) / (440.0 - 380.0);
        R = pow((-(w - 440.0) / (440.0 - 380.0)) * a, gamma);
        G = 0.0;
        B = pow(a, gamma);
    } else if (w >= 440.0 & w <= 490.0) {
        R = 0.0;
        G = pow((w - 440.0) / (490.0 - 440.0), gamma);
        B = 1.0;
    } else if (w >= 490.0 & w <= 510.0) {
        R = 0.0;
        G = 1.0;
        B = pow(-(w - 510.0) / (510.0 - 490.0), gamma);
    } else if (w >= 510.0 & w <= 580.0) {
        R = pow((w - 510.0) / (580.0 - 510.0), gamma);
        G = 1.0;
        B = 0.0;
    } else if (w >= 580.0 & w <= 645.0) {
        R = 1.0;
        G = pow(-(w - 645.0) / (645.0 - 580.0), gamma);
        B = 0.0;
    } else if (w >= 645.0 & w <= 750.0) {
        double a = 0.3 + 0.7 * (750.0 - w) / (750.0 - 645.0);
        R = pow(a, gamma);
        G = 0.0;
        B = 0.0;
    } else {
        R = 0.0;
        G = 0.0;
        B = 0.0;
    }
    R = R * 255;
    G = G * 255;
    B = B * 255;
    return QColor::fromRgb(floor(R), floor(G), floor(B));
}

void ImageOutputValue::setTextureFromImage(std::shared_ptr<MultiDimImage<float>> image)
{
    if (image.get() != m_image.get()) {
        m_image = image;
        if (m_image) {
            if (!m_texture) {
                m_texture = new VolumeTexture();
            }
            m_texture->init(*m_image);
            QObject::connect(m_texture, &QObject::destroyed,
                this, &ImageOutputValue::textureDeleted);
            if (m_image->meta.has("wavelength")) {
                setColor(details::waveLengthToQColor(stod(m_image->meta.get("wavelength"))));
            }

        }
        Q_EMIT textureChanged();
        Q_EMIT sizeChanged();
    }
}

void ImageOutputValue::textureDeleted()
{
    m_texture = nullptr;
}

void ImageOutputValue::setColor(QColor color)
{
    if (m_color != color) {
        m_color = color;
        Q_EMIT colorChanged();
    }
}

void ImageOutputValue::setVisible(bool visible)
{
    if (m_visible != visible) {
        m_visible = visible;
        Q_EMIT visibleChanged();
    }
}

void ImageOutputValue::setLutParams(QVector2D lutParams)
{
    if (!qFuzzyCompare(m_lutParams, lutParams)) {
        m_lutParams = lutParams;
        Q_EMIT lutParamsChanged();
    }
}

ImageOutputValue::~ImageOutputValue()
{
    if (m_texture && m_texture->parentNode() == nullptr) {
        delete m_texture;
    }
}

BackendOutput::BackendOutput(std::weak_ptr<OutputPort> source,
    ComputePlatform& platform, int portId, int parentUid)
    : m_source(source), m_portId(portId), m_parentUid(parentUid)
{
    static vector<Qt::GlobalColor> colorNames = {Qt::red, Qt::green, Qt::blue, Qt::cyan, Qt::magenta, Qt::yellow};
    m_internalValue.setColor(QColor(colorNames[(parentUid + portId - 4) % colorNames.size()]));
    m_internalValue.setVisible(false);
    m_internalValue.setLutParams(QVector2D(0, 1));

    QObject::connect(&m_internalValue,
                     &ImageOutputValue::textureChanged,
                     this, &BackendStoreItem::valueChanged);
    QObject::connect(&m_internalValue,
                     &ImageOutputValue::sizeChanged,
                     this, &BackendStoreItem::valueChanged);
    QObject::connect(&m_internalValue,
                     &ImageOutputValue::colorChanged,
                     this, &BackendStoreItem::valueChanged);
    QObject::connect(&m_internalValue,
                     &ImageOutputValue::visibleChanged,
                     this, &BackendStoreItem::valueChanged);
    QObject::connect(&m_internalValue,
                     &ImageOutputValue::lutParamsChanged,
                     this, &BackendStoreItem::valueChanged);

    if (m_source.lock() == nullptr) {
        throw std::runtime_error("invalid source port");
    }

    using namespace details;

    m_hints = propertyMapToQVariantMap(m_source.lock()->properties());

    static BuildOutputFunction empty;
    static vector<tuple<string, BuildOutputFunction, string>> types = {
        make_tuple("uint8_t", empty, "int"),
        make_tuple("uint16_t", empty, "int"),
        make_tuple("uint32_t", empty, "int"),
        make_tuple("uint64_t", empty, "int"),
        make_tuple("int8_t", empty, "int"),
        make_tuple("int16_t", empty, "int"),
        make_tuple("int32_t", empty, "int"),
        make_tuple("int64_t", empty, "int"),
        make_tuple("float", empty, "float"),
        make_tuple("double", empty, "float"),
        make_tuple("bool", empty, "bool"),
        make_tuple("string", empty, "string"),
        make_tuple("url", empty, "url"),
        make_tuple("float-image", buildImageOutput<float>, "float-image"),
        make_tuple("uint32-image", buildImageOutput<uint32_t>, "int-image"),
        make_tuple("py-object", empty, "py-object")
    };

    const auto& t = m_source.lock()->traits();
    for (auto& tri: types) {
        if (t.hasTrait(get<0>(tri))) {
            if (get<1>(tri)) {
                m_interfaceModule = get<1>(tri)(platform);
                m_interfaceModule->setOnExecuted([this]() { this->onExecuted(); });
                m_source.lock()->bind(m_interfaceModule->inputPort(0));
            }
            m_type = QString::fromStdString(get<2>(tri));
            return;
        }
    }

    string errorMsg = "unknown output type for port '"
        + m_source.lock()->name() + "' (info:["
        + portTypeTraitsToString(m_source.lock()->traits()) + "])";
    throw std::runtime_error(errorMsg);
}

int BackendOutput::uid() const
{
    return m_portId;
}

int BackendOutput::parentUid() const
{
    return m_parentUid;
}

QString BackendOutput::category() const
{
    return QString("output");
}

QString BackendOutput::name() const
{
    // TODO: check for nullptr
    return QString::fromStdString(m_source.lock()->name());
}

QString BackendOutput::type() const
{
    return m_type;
}

int BackendOutput::status() const
{
    return m_ready;
}

QVariant BackendOutput::value() const
{
    return QVariant::fromValue((ImageOutputValue*)&m_internalValue);
}

QVariant BackendOutput::hints() const
{
    return m_hints;
}

void BackendOutput::setName(const QString&)
{}

void BackendOutput::setStatus(int)
{}

bool BackendOutput::setValue(QVariant)
{
    return true;
}

std::weak_ptr<OutputPort> BackendOutput::source()
{
    return m_source;
}

void BackendOutput::onExecuted()
{
    if (m_interfaceModule) {
        auto im = m_interfaceModule->getImage();
        m_internalValue.setTextureFromImage(im);
        if (m_internalValue.texture()) {
            m_ready = true;
            Q_EMIT statusChanged();
        }
    }
}
