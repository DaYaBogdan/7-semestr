#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    connect(ui->label_2, SIGNAL(disable()),
            this, SLOT(disableEditText()));
    connect(ui->btn_changeTitle, SIGNAL(clicked()), this,
            SLOT(setTitle()));
    connect(ui->editText, SIGNAL(textChanged()), this,
            SLOT(copyText()));
    connect(ui->editText_copy, SIGNAL(textChanged()), this,
            SLOT(counter()));
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::disableEditText()
{
    ui->editText->setDisabled(true);
}

void MainWindow::setTitle()
{
    QString text = ui->lineEdit->text();

    if (text.isEmpty())
        return;

    this->setWindowTitle(text);
}

void MainWindow::copyText()
{
    QString text = ui->editText->toPlainText();
    text.replace(toChange, changeTo);
    ui->editText_copy->setPlainText(text);
}

void MainWindow::counter()
{
    ui->label_2->setText(QString::number(ui->editText_copy->toPlainText().count(countThis)));
}