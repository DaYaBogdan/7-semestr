#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    // слоты для "валидации на лету"
    void validateEmail();
    void validateName();
    void validateTitle();
    void validateMessage();

    // слот кнопки
    void on_sendMessage_clicked();

private:
    // функции-проверки: true = ok, false = ошибка
    // (setHint = true — обновлять ли подсказку/метку)
    bool checkEmail(bool setHint = true);
    bool checkName(bool setHint = true);
    bool checkTitle(bool setHint = true);
    bool checkMessage(bool setHint = true);

    // сохранение в файл
    bool saveToFile(const QString &path);

    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H