from repositories.report_value import ReportValueRepository


class ReportValueService:
    def __init__(self, repository: ReportValueRepository):
        self.repository = repository
