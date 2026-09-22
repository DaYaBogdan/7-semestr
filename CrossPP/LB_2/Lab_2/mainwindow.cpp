#include "mainwindow.h"
#include "./ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    connect(ui->pushButton, SIGNAL(clicked()), this,
            SLOT(addWord()));
    connect(ui->label, SIGNAL(banUser()), ui->pushButton,
            SLOT(hide()));
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::addWord()
{
    QString newWord = ui->lineEdit->text();
    if (!newWord.compare(bannedWord, Qt::CaseInsensitive))
    {
        QMessageBox msgBox;
        msgBox.setText("И не стыдно?");
        msgBox.setStandardButtons(QMessageBox::Ok);
        msgBox.exec();
        ui->label->incValue();
    }
    else
    {
        ui->textEdit->append(newWord + '\n')
    }
}