#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include "fieldcontroller.h"

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    qmlRegisterType<FieldController>("Game", 1, 0, "FieldController");

    QQmlApplicationEngine engine;
    QObject::connect(
        &engine,
        &QQmlApplicationEngine::objectCreationFailed,
        &app,
        []() { QCoreApplication::exit(-1); },
        Qt::QueuedConnection);
    engine.loadFromModule("Lab_5", "Main");

    return QGuiApplication::exec();
}
