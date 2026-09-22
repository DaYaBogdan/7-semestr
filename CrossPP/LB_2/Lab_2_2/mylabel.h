#ifndef MYLABEL_H
#define MYLABEL_H

#include <QLabel>

class MyLabel : public QLabel
{
    Q_OBJECT
public:
    MyLabel(QWidget *parent = 0);
private:
    int value = 0;
    const int limit = 10;
public slots:
    void check();
signals:
    void disable();
};

#endif // MYLABEL_H
