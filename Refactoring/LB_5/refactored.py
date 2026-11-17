# after_lr6.py
from abc import ABC, abstractmethod


# ---------- Доменные классы ----------
class Report(ABC):
    @abstractmethod
    def name(self) -> str:
        ...

class PdfReport(Report):
    def name(self) -> str:
        return "PDF"

class HtmlReport(Report):
    def name(self) -> str:
        return "HTML"


# ---------- Паттерн «Фабричный метод» ----------
class ReportFactory(ABC):
    @abstractmethod
    def create(self) -> Report:
        ...

class PdfReportFactory(ReportFactory):
    def create(self) -> Report:
        return PdfReport()

class HtmlReportFactory(ReportFactory):
    def create(self) -> Report:
        return HtmlReport()


# ---------- Паттерн «Стратегия» ----------
class ExportStrategy(ABC):
    @abstractmethod
    def export(self, report: Report) -> None:
        ...

class PdfExportStrategy(ExportStrategy):
    def export(self, report: Report) -> None:
        print(f"Export {report.name()} to PDF")

class CsvExportStrategy(ExportStrategy):
    def export(self, report: Report) -> None:
        print(f"Export {report.name()} to CSV")


# ---------- Паттерн «Наблюдатель» ----------
class ReportListener(ABC):
    @abstractmethod
    def on_report_ready(self, report: Report) -> None:
        ...

class EmailNotifier(ReportListener):
    def on_report_ready(self, report: Report) -> None:
        print(f"Email: report {report.name()} ready")

class LogNotifier(ReportListener):
    def on_report_ready(self, report: Report) -> None:
        print(f"Log: report {report.name()} ready")


class ReportService:
    def __init__(self, factory: ReportFactory, strategy: ExportStrategy):
        self._factory = factory
        self._strategy = strategy
        self._listeners: list[ReportListener] = []

    def add_listener(self, listener: ReportListener) -> None:
        self._listeners.append(listener)

    def generate(self) -> Report:
        report = self._factory.create()
        for l in self._listeners:
            l.on_report_ready(report)
        return report

    def export(self, report: Report) -> None:
        self._strategy.export(report)


# ---------- Клиент ----------
if __name__ == "__main__":
    service = ReportService(PdfReportFactory(), CsvExportStrategy())
    service.add_listener(EmailNotifier())
    service.add_listener(LogNotifier())

    report = service.generate()
    service.export(report)