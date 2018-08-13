#include "BackendStore.h"

BackendStore::BackendStore(QObject* parent)
    : QAbstractItemModel(parent)
{
    m_root = new BackendStoreRootItem;
    addModule("a", "typeA");
    addModule("b", "typeB");
    addModule("c", "typeC");
}

void BackendStore::addModule(QString name, QString type)
{
    BackendStoreDummyItem* newItem = new BackendStoreDummyItem(42, name, type);
    BackendStoreDummyItem* subItem = new BackendStoreDummyItem(42, "sub", "sub " + type);

    // beginInsertRows(QModelIndex(), m_root->numChildren(), m_root->numChildren());
    m_root->add(newItem);
    newItem->add(subItem);
    // endInsertRows();
}

BackendStore::~BackendStore()
{
    delete m_root;
}

QHash<int, QByteArray> BackendStore::roleNames() const
{
    static QHash<int, QByteArray> roles = {
        {UidRole, "uid"},
        {CategoryRole, "category"},
        {NameRole, "name"},
        {TypeRole, "type"},
        {StatusRole, "status"},
        {ValueRole, "value"}
    };
    return roles;
}

Qt::ItemFlags BackendStore::flags(const QModelIndex& index) const
{
    if (!index.isValid())
        return 0;

    return QAbstractItemModel::flags(index);
}

QVariant BackendStore::data(const QModelIndex& index, int role) const
{
    if (!index.isValid()) {
        return QVariant();
    }

    BackendStoreItem* item = static_cast<BackendStoreItem*>(index.internalPointer());

    if (!item) {
        return QVariant();
    }

    switch (role) {
        case UidRole: return item->uid();
        case CategoryRole: return item->category();
        case NameRole: return item->name();
        case TypeRole: return item->type();
        case StatusRole: return item->status();
        case ValueRole: return item->value();
        default: return QVariant();
    }
}

QModelIndex BackendStore::index(int row, int column, const QModelIndex& parent) const
{
    if (!hasIndex(row, column, parent)) {
        return QModelIndex();
    }

    BackendStoreItem* r;
    if (parent.isValid()) {
        r = static_cast<BackendStoreItem*>(parent.internalPointer());
    } else {
        r = m_root;
    }

    BackendStoreItem* c = r->child(row);
    if (c) {
        return createIndex(row, column, c);
    } else {
        return QModelIndex();
    }
}

QModelIndex BackendStore::parent(const QModelIndex& index) const
{
    if (!index.isValid()) {
        return QModelIndex();
    }

    BackendStoreItem* c = static_cast<BackendStoreItem*>(index.internalPointer());
    BackendStoreItem* r = c->parent();

    if (r == m_root) {
        return QModelIndex();
    }

    return createIndex(r->row(), 0, r);
}

int BackendStore::rowCount(const QModelIndex& parent) const
{
    if (parent.column() > 0) {
        return 0;
    }

    if (parent.isValid()) {
        return static_cast<BackendStoreItem*>(parent.internalPointer())->numChildren();
    } else {
        return m_root->numChildren();
    }
}

int BackendStore::columnCount(const QModelIndex& parent) const
{
    if (parent.isValid()) {
        return static_cast<BackendStoreItem*>(parent.internalPointer())->columnCount();
    } else {
        m_root->columnCount();
    }
}

BackendStoreProxy::BackendStoreProxy(QObject* parent)
    :  QSortFilterProxyModel(parent)
{}

bool BackendStoreProxy::filterAcceptsRow(int sourceRow, const QModelIndex& sourceParent) const
{
    QModelIndex index = sourceModel()->index(sourceRow, 0, sourceParent);
    return sourceModel()->data(index, BackendStore::TypeRole).toString() == QString("sub");
}