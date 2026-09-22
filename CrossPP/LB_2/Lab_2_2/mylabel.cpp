#include "mylabel.h"

MyLabel::MyLabel(QWidget *parent)
    : QLabel(parent) {
}

void MyLabel::check()
{
    if (this->text().toInt() > limit){
        emit disable();
    }
}


