#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    QString DBpath = QDir::toNativeSeparators("students.db");
    sdb = QSqlDatabase::addDatabase("QSQLITE");
    sdb.setDatabaseName(DBpath);

    if(!sdb.open()) {
        QMessageBox::critical(this, tr("SQLite connection"),
            tr("Unable connect to DB, check file permission."));
        exit(1);
    }

    QSqlTableModel *model = new QSqlTableModel(ui->studentsView);
    model->setTable("Student");

    model->setEditStrategy(QSqlTableModel::OnFieldChange);
    model->select();

    ui->studentsView->setModel(model);
    connect(ui->deleteButton, SIGNAL(clicked()), SLOT(deleteSelected()));
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::deleteSelected()
{
    QModelIndexList indexes = ui->studentsView->selectionModel()->selection().indexes();
    QSet<int> *rowsToDelete = new QSet<int>();

    for (int i = 0; i < indexes.count(); ++i) {
        QModelIndex index = indexes.at(i);
        rowsToDelete->insert(index.row());
    }

    QAbstractItemModel *model = ui->studentsView->model();
    QSet<int>::iterator i;
    for (i = rowsToDelete->begin(); i != rowsToDelete->end(); ++i)
    {
        model->removeRow(*i);
    }
}