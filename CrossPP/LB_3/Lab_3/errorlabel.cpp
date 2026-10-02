#include "errorlabel.h"

ErrorLabel::ErrorLabel(QWidget *parrent) : QLabel(parrent) {}

void ErrorLabel::addErr(QString err) {
    this->errorText.append(err);
    emit hasErr();
}

// void ErrorLabel::hasErr() {}