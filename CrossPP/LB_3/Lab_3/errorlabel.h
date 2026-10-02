#ifndef ERRORLABEL_H
#define ERRORLABEL_H

#include <QLabel>

class ErrorLabel : public QLabel
{
    Q_OBJECT

public:
    explicit ErrorLabel(QWidget *parrent = nullptr);

private:
    QString errorText;

signals:
    void hasErr();

public slots:
    void addErr(QString err);
};

#endif // ERRORLABEL_H
