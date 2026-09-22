#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QRegularExpression>
#include <QToolTip>
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

    connect(ui->emailEdit,   &QTextEdit::textChanged, this, &MainWindow::validateEmail);
    connect(ui->nameEdit,    &QTextEdit::textChanged, this, &MainWindow::validateName);
    connect(ui->titleEdit,   &QTextEdit::textChanged, this, &MainWindow::validateTitle);
    connect(ui->messageEdit, &QTextEdit::textChanged, this, &MainWindow::validateMessage);

    // первичная проверка (пустые поля -> подсказки)
    validateEmail();
    validateName();
    validateTitle();
    validateMessage();
}

MainWindow::~MainWindow()
{
    delete ui;
}

// ОТКРЫВАЮ ПОДСКАЗКУ

static void showHint(QWidget *field, const QString &hint)
{
    field->setToolTip(hint);

    if (hint.isEmpty()) {
        QToolTip::hideText();
        return;
    }

    const QPoint p = field->mapToGlobal(QPoint(0, field->height()));
    QToolTip::showText(p, hint, field, QRect(), 2000);
}

// ------------------------------------------------------------------------------

// ПРОВЕРКИ ДЛЯ ПОЛЕЙ

bool MainWindow::checkEmail(bool setHint)
{
    static const QRegularExpression re(
        R"(^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$)"
        );

    const QString text = ui->emailEdit->toPlainText().trimmed();
    QString hint;

    if (text.isEmpty())
        hint = "E-mail не может быть пустым";
    else if (!re.match(text).hasMatch())
        hint = "Неверный формат e-mail. Пример: user@mail.ru";

    if (setHint)
        showHint(ui->emailEdit, hint);

    return hint.isEmpty();
}

bool MainWindow::checkName(bool setHint)
{
    const QString text = ui->nameEdit->toPlainText().trimmed();
    QString hint;

    if (text.isEmpty())
        hint = "Поле имени должно содержать хотя бы один символ";

    if (setHint)
        showHint(ui->nameEdit, hint);

    return hint.isEmpty();
}

bool MainWindow::checkTitle(bool setHint)
{
    const QString text = ui->titleEdit->toPlainText().trimmed();
    QString hint;

    if (text.isEmpty())
        hint = "Поле темы должно содержать хотя бы один символ";

    if (setHint)
        showHint(ui->titleEdit, hint);

    return hint.isEmpty();
}

bool MainWindow::checkMessage(bool setHint)
{
    const QString text = ui->messageEdit->toPlainText().trimmed();
    QString hint;

    if (text.isEmpty())
        hint = "Поле сообщения должно содержать хотя бы один символ";

    if (setHint)
        showHint(ui->messageEdit, hint);

    return hint.isEmpty();
}

// ------------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// Слоты «на лету»
// ---------------------------------------------------------------------------
void MainWindow::validateEmail()   { checkEmail(true);   }
void MainWindow::validateName()    { checkName(true);    }
void MainWindow::validateTitle()   { checkTitle(true);   }
void MainWindow::validateMessage() { checkMessage(true); }

// ------------------------------------------------------------------------------

// ВАЛИДАЦИЯ НА КНОПКЕ

void MainWindow::on_sendMessage_clicked()
{
    // 1. Проверяем все поля. setHint = true, чтобы пользователь увидел ошибки.
    const bool emailOk   = checkEmail(true);
    const bool nameOk    = checkName(true);
    const bool titleOk   = checkTitle(true);
    const bool messageOk = checkMessage(true);

    const bool allOk = emailOk && nameOk && titleOk && messageOk;

    if (!allOk) {
        QMessageBox::warning(this, "Ошибка",
                             "Не все поля заполнены корректно. Проверьте подсказки под полями.");
        return;
    }

    // 2. Спрашиваем путь у пользователя
    const QString defaultPath = QDir::homePath() + "/message.txt";
    const QString path = QFileDialog::getSaveFileName(
        this,
        "Сохранить сообщение",
        defaultPath,
        "Текстовые файлы (*.txt);;Все файлы (*)"
        );

    if (path.isEmpty())
        return;   // пользователь нажал «Отмена»

    // 3. Сохраняем
    if (!saveToFile(path)) {
        QMessageBox::warning(this, "Ошибка",
                             "Не удалось сохранить файл: " + path);
        return;
    }

    QMessageBox::information(this, "Готово",
                             "Сообщение сохранено:\n" + path);
}

// ------------------------------------------------------------------------------

// СОХРАНЕНИЕ В ФАЙЛ

bool MainWindow::saveToFile(const QString &path)
{
    QSaveFile file(path);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Text))
        return false;

    QTextStream out(&file);
    out.setEncoding(QStringConverter::Utf8);   // Qt 6
    // для Qt 5: out.setCodec("UTF-8");

    out << "E-mail: "   << ui->emailEdit->toPlainText().trimmed()   << '\n';
    out << "Имя: "      << ui->nameEdit->toPlainText().trimmed()    << '\n';
    out << "Тема: "     << ui->titleEdit->toPlainText().trimmed()   << '\n';
    out << "Сообщение:\n"
        << ui->messageEdit->toPlainText()                            << '\n';

    return file.commit();
}

// ------------------------------------------------------------------------------