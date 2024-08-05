
import pytz
from rest_framework.response import Response
from rest_framework.views import APIView

from common.enums.language import LanguageEnum


class CoreView(APIView):
    def get_timezones(self, request):
        timezones = [(tz, tz) for tz in pytz.all_timezones]
        return Response({'timezones': timezones})

    def get_languages(self, request):
        languages = [(lang.value, lang.label) for lang in LanguageEnum]
        return Response({'languages': languages})

    def get(self, request, action):
        if action == 'timezones':
            return self.get_timezones(request)
        elif action == 'languages':
            return self.get_languages(request)
        else:
            return Response({'error': 'Invalid action'}, status=400)
