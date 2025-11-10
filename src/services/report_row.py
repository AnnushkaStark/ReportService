from repositories.report_row import ReportRowRepository
from services.report_value import ReportValueService


class ReportRowService:
    def __init__(self, repository: ReportRowRepository, report_value_service: ReportValueService):
        self.repository = repository
        self.report_value_service = report_value_service
