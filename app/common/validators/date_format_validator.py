<<<<<<< HEAD
from datetime import datetime


class DateFormatValidator:
    @staticmethod
    def validate(date_str):
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return None
=======
from datetime import datetime


class DateFormatValidator:
    @staticmethod
    def validate(date_str):
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return None
>>>>>>> origin/ma-branch
