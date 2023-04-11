from core.abstract.views import AbstractViewSet

from .serializers import  BimaHrActivitySerializer
from .models import BimaHrActivity
from rest_framework.response import Response

class BimaHrActivityViewSet(AbstractViewSet):
    queryset = BimaHrActivity.objects.all()
    serializer_class = BimaHrActivitySerializer
    permission_classes = []

    #def activitycandidat(request, pk):

     #   liste_candidat_activity = BimaHrActivity.objects.filter(id_candidat=pk)
      #  context = {'liste_candidat_activity': liste_candidat_activity}
       # return Response(request, context)
