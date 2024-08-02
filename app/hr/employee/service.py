import logging
from collections import defaultdict
from datetime import datetime

logger = logging.getLogger(__name__)


class BimaHrEmployeeService:
    @staticmethod
    def group_by_date(history_data):
        grouped = defaultdict(list)

        for record in history_data:
            date_without_time = datetime.fromisoformat(record["history_date"]).date()
            grouped[date_without_time].append(record)

        return grouped
