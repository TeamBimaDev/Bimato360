from core.abstract.views import AbstractViewSet

from .serializers import BimaHrCondidatPosteSerializer
from .models import BimaHrCondidatPoste


class BimaHrCondidatPosteViewSet(AbstractViewSet):
    queryset = BimaHrCondidatPoste.objects.all()
    serializer_class = BimaHrCondidatPosteSerializer
    permission_classes = []

    #def activitycandidat(request, pk):

     #   liste_candidat_activity = BimaHrActivity.objects.filter(id_candidat=pk)
      #  context = {'liste_candidat_activity': liste_candidat_activity}
       # return Response(request, context)
