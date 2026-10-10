#include "gamefield.h"

#include <QFile>
#include <QTextStream>

GameField::GameField(QObject *parent)
    : QObject(parent) {
    m_filename = QStringLiteral("gamefield.txt");
}

GameField::~GameField() {}

QString GameField::field() const {
    return m_field;
}

void GameField::setField(const QString &value) {
    m_field = value;
    emit fieldChanged();
}

bool GameField::saveToFile() {
    QFile file(m_filename);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Truncate | QIODevice::Text)) {
        return false;
    }

    QTextStream out(&file);
    out << m_field;

    file.close();
    return true;
}

bool GameField::loadFromFile() {
    QFile file(m_filename);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        return false;
    }

    QTextStream in(&file);
    setField(in.readAll());

    file.close();
    return true;
}