#ifndef MYLABEL_H
#define MYLABEL_H

#include <QLabel>

class MyLabel : public QLabel {
    Q_OBJECT
public:
    explicit MyLabel(QWidget *parent = nullptr);

    void setText(const QString &text);

signals:
    void disable();

public slots:
    void check();

private:
    int limit = 10;
};

#endif // MYLABEL_H
