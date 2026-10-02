#ifndef MYQLABEL_H
#define MYQLABEL_H

#include <QLabel>

class MyQLabel : public QLabel
{
    Q_OBJECT
private:
    int value = 0;
    const int banLimit = 10;

public:
    MyQLabel(QWidget *parent = 0);
public slots:
    void incValue();
signals:
    void banUser();
};

#endif // MYQLABEL_H
