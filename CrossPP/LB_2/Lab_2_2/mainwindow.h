#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <mylabel.h>

QT_BEGIN_NAMESPACE
namespace Ui {
class MainWindow;
}
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow() override;

private:
    char toChange = 'a';
    char changeTo = '*';
    char countThis = '*';

    Ui::MainWindow *ui;

private slots:
    void setTitle();
    void copyText();
    void counter();
    void disableEditText();
};

#endif // MAINWINDOW_H
