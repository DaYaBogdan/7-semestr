# before_lr6.py
# Плохой код: создание объектов и выбор алгоритма через if/elif,
# ручное оповещение слушателей с проверкой типа

class PdfReport:
    pass

class HtmlReport:
    pass

class EmailNotifier:
    def notify_ready(self, report):
        print(f"Email: report {type(report).__name__} ready")

class LogNotifier:
    def notify_ready(self, report):
        print(f"Log: report {type(report).__name__} ready")


class ReportService:
    def __init__(self):
        self._listeners = []

    def create_report(self, type_: str):
        if type_ == "PDF":
            return PdfReport()
        elif type_ == "HTML":
            return HtmlReport()
        else:
            raise ValueError("Unknown report type")

    def export(self, report, format_: str):
        if format_ == "PDF":
            print("Export to PDF")
        elif format_ == "CSV":
            print("Export to CSV")
        else:
            raise ValueError("Unknown format")

    def add_listener(self, listener):
        self._listeners.append(listener)

    def generate(self):
        report = self.create_report("PDF")
        # ручное оповещение с проверкой типа — «запах» кода
        for l in self._listeners:
            if isinstance(l, EmailNotifier):
                l.notify_ready(report)
            elif isinstance(l, LogNotifier):
                l.notify_ready(report)


if __name__ == "__main__":
    svc = ReportService()
    svc.add_listener(EmailNotifier())
    svc.add_listener(LogNotifier())
    svc.generate()
    svc.export(PdfReport(), "CSV")