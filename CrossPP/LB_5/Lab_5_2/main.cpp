#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>

#include "gamefield.h"

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    GameField gameField;

    QQmlApplicationEngine engine;

    engine.rootContext()->setContextProperty("gameField", &gameField);

    QObject::connect(
        &engine,
        &QQmlApplicationEngine::objectCreationFailed,
        &app,
        []() { QCoreApplication::exit(-1); },
        Qt::QueuedConnection);
    engine.loadFromModule("Lab_5_2", "Main");

    return QGuiApplication::exec();
}
