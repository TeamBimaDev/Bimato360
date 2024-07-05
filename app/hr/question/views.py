import django_filters
from common.converters.default_converters import str_to_bool
from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet
from django.db.models import Q

from .models import BimaHrQuestion
from .serializers import BimaHrQuestionSerializer


class BimaHrQuestionFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    active = django_filters.CharFilter(method='filter_active')

    class Meta:
        model = BimaHrQuestion
        fields = ['active', 'search']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) 
        )

    def filter_active(self, queryset, name, value):
        if value == 'all' or value is None:
            return queryset
        else:
            return queryset.filter(active=str_to_bool(value))


class BimaHrQuestionViewSet(AbstractViewSet):
    queryset = BimaHrQuestion.objects.all()
    serializer_class = BimaHrQuestionSerializer
    permission_classes = []
    filterset_class = BimaHrQuestionFilter
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        'list': ['question.can_read'],
        'create': ['question.can_create'],
        'retrieve': ['question.can_read'],
        'update': ['question.can_update'],
        'partial_update': ['question.can_update'],
        'destroy': ['question.can_delete'],
    }

    def get_object(self):
        obj = BimaHrQuestion.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
