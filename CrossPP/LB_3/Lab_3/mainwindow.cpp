#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QFile>
#include <QTextStream>
#include <QSaveFile>
#include <QFileDialog>
#include <QMessageBox>
#include <QDir>
#include <QStandardPaths>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    connect(ui->sendMessage, SIGNAL(clicked()), this,
            SLOT(sendMessage()));
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::sendMessage()
{

    const QString defaultPath = QDir::homePath() + "/message.txt";
    const QString path = QFileDialog::getSaveFileName(
        this,
        "Сохранить сообщение",
        defaultPath,
        "Текстовые файлы (*.txt);;Все файлы (*)"
        );

    if (path.isEmpty())
        return;

    if (!saveToFile(path)) {
        QMessageBox::warning(this, "Ошибка", "Не удалось сохранить файл: " + path);
        return;
    }

    QMessageBox::information(this, "Готово", "Сообщение сохранено: " + path);
}

bool MainWindow::saveToFile(const QString &path)
{
    QSaveFile file(path);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Text))
        return false;

    QTextStream out(&file);
    out.setEncoding(QStringConverter::Utf8);

    out << "E-mail: "     << ui->emailEdit->text().trimmed()   << '\n';
    out << "Имя: "        << ui->nameEdit->text().trimmed()    << '\n';
    out << "Тема: "       << ui->titleEdit->text().trimmed()   << '\n';
    out << "\nСообщение ниже:\n"   << ui->messageEdit->toPlainText()  << '\n';

    return file.commit();
}