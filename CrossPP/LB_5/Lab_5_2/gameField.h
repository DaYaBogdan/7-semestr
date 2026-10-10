#ifndef GAMEFIELD_H
#define GAMEFIELD_H

#include <QObject>
#include <QString>

class GameField : public QObject
{
    Q_OBJECT

public:
    explicit GameField(QObject *parent = nullptr);
    ~GameField();

    Q_PROPERTY(QString field READ field WRITE setField NOTIFY fieldChanged)

    Q_INVOKABLE bool saveToFile();
    Q_INVOKABLE bool loadFromFile();

    QString field() const;
    void setField(const QString &value);

signals:
    void fieldChanged();

private:
    QString m_filename;
    QString m_field;
};

#endif // GAMEFIELD_H