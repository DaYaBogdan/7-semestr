#include "fieldcontroller.h"
#include <QFile>
#include <QTextStream>
#include <QStandardPaths>
#include <QDir>
#include <QDebug>

FieldController::FieldController(QObject *parent)
    : QObject{parent}
{}

void FieldController::setFieldWidth(int w)
{
    if (w <= 0 || w == m_field.width()) return;
    m_field.resize(w, m_field.height() > 0 ? m_field.height() : 1, 0);
    emit fieldChanged();
}

void FieldController::setFieldHeight(int h)
{
    if (h <= 0 || h == m_field.height()) return;
    m_field.resize(m_field.width() > 0 ? m_field.width() : 1, h, 0);
    emit fieldChanged();
}

QString FieldController::defaultFileName() const
{
    const QString dir = QStandardPaths::writableLocation(QStandardPaths::AppDataLocation);
    QDir().mkpath(dir);
    return dir + "/playfield.txt";
}

QVariantList FieldController::cells() const
{
    QVariantList list;
    list.reserve(static_cast<int>(m_field.cells().size()));
    for (int v : m_field.cells())
        list.append(v);
    return list;
}

void FieldController::createField(int width, int height, int defaultValue)
{
    if (width <= 0 || height <= 0) return;
    m_field.resize(width, height, defaultValue);
    emit fieldChanged();
}

int FieldController::getCell(int x, int y) const
{
    return m_field.cell(x, y);
}

void FieldController::setCell(int x, int y, int value)
{
    if (m_field.cell(x, y) == value) return;
    m_field.setCell(x, y, value);
    emit cellChanged(x, y, value);
    emit fieldChanged();
}

void FieldController::fill(int value)
{
    m_field.clear(value);
    emit fieldChanged();
}

void FieldController::setCells(const QVariantList &cells)
{
    const int expected = m_field.width() * m_field.height();
    if (cells.size() != expected) return;

    auto &vec = m_field.cells();
    for (int i = 0; i < cells.size(); ++i)
        vec[static_cast<size_t>(i)] = cells[i].toInt();
    emit fieldChanged();
}

// ---------------------- Сохранение ----------------------

bool FieldController::save(const QString &fileName)
{
    if (m_field.isEmpty()) {
        qWarning() << "Поле пустое — нечего сохранять";
        return false;
    }

    const QString path = fileName.isEmpty()
                             ? (m_fileName.isEmpty() ? defaultFileName() : m_fileName)
                             : fileName;

    QFile file(path);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Truncate | QIODevice::Text))
        return false;

    QTextStream out(&file);
    out << m_field.width() << ' ' << m_field.height() << '\n';
    for (int y = 0; y < m_field.height(); ++y) {
        for (int x = 0; x < m_field.width(); ++x) {
            if (x) out << ' ';
            out << m_field.cell(x, y);
        }
        out << '\n';
    }

    m_fileName = path;
    return true;
}

// ---------------------- Загрузка ----------------------

bool FieldController::load(const QString &fileName)
{
    const QString path = fileName.isEmpty()
    ? (m_fileName.isEmpty() ? defaultFileName() : m_fileName)
    : fileName;

    QFile file(path);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) return false;

    QTextStream in(&file);

    int w = 0, h = 0;
    in >> w >> h;
    if (w <= 0 || h <= 0) {
        qWarning() << "Некорректные размеры в файле:" << w << h;
        return false;
    }

    m_field.resize(w, h, 0);

    for (int y = 0; y < h; ++y)
        for (int x = 0; x < w; ++x) {
            int v = 0;
            in >> v;
            m_field.setCell(x, y, v);
        }

    m_fileName = path;
    emit fieldChanged();
    return true;
}