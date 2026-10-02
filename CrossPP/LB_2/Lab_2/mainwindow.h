#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QMessageBox>
#include "myqlabel.h"

QT_BEGIN_NAMESPACE
namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow() override;

private:
    const QString bannedWord = "Помидор";

    Ui::MainWindow *ui;

private slots:
    void addWord();
};
#endif // MAINWINDOW_H
