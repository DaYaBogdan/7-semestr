#include "mylabel.h"

MyLabel::MyLabel(QWidget *parent)
    : QLabel(parent) {
}

void MyLabel::setText(const QString &text)
{
    QLabel::setText(text);
    check();
}

void MyLabel::check()
{
    int value = this->text().toInt();
    if (value > limit - 1) {
        emit disable();
    }
}


