<<<<<<< HEAD
from datetime import datetime

from rest_framework import serializers


class CustomDateField(serializers.DateField):

    def to_internal_value(self, data):
        try:
            return datetime.strptime(data, '%Y-%m-%d').date()
        except ValueError:
            return None
=======
from datetime import datetime

from rest_framework import serializers


class CustomDateField(serializers.DateField):

    def to_internal_value(self, data):
        try:
            return datetime.strptime(data, '%Y-%m-%d').date()
        except ValueError:
            return None
>>>>>>> origin/ma-branch
