#ifndef FIELDCONTROLLER_H
#define FIELDCONTROLLER_H

#include <QObject>
#include <QVariantList>
#include <QString>
#include "field.h"

class FieldController : public QObject
{
    Q_OBJECT

    Q_PROPERTY(int fieldWidth  READ fieldWidth  WRITE setFieldWidth  NOTIFY fieldChanged)
    Q_PROPERTY(int fieldHeight READ fieldHeight WRITE setFieldHeight NOTIFY fieldChanged)

    Q_PROPERTY(int width  READ width  NOTIFY fieldChanged)
    Q_PROPERTY(int height READ height NOTIFY fieldChanged)
    Q_PROPERTY(QVariantList cells READ cells NOTIFY fieldChanged)

public:
    explicit FieldController(QObject *parent = nullptr);

    int fieldWidth()  const { return m_field.width();  }
    int fieldHeight() const { return m_field.height(); }

    void setFieldWidth(int w);
    void setFieldHeight(int h);

    int width()  const { return m_field.width();  }
    int height() const { return m_field.height(); }
    QVariantList cells() const;

    Q_INVOKABLE void createField(int width, int height, int defaultValue = 0);
    Q_INVOKABLE int  getCell(int x, int y) const;
    Q_INVOKABLE void setCell(int x, int y, int value);
    Q_INVOKABLE void fill(int value);
    Q_INVOKABLE bool save(const QString &fileName = QString());
    Q_INVOKABLE bool load(const QString &fileName = QString());
    Q_INVOKABLE void setCells(const QVariantList &cells);

signals:
    void fieldChanged();
    void cellChanged(int x, int y, int value);

private:
    QString defaultFileName() const;

    Field m_field;
    QString m_fileName;
};

#endif // FIELDCONTROLLER_H