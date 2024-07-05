import django_filters
from common.converters.default_converters import str_to_bool
from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet
from django.db.models import Q

from .models import BimaHrSkill
from .serializers import BimaHrSkillSerializer


class BimaHrSkillFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    active = django_filters.CharFilter(method='filter_active')

    class Meta:
        model = BimaHrSkill
        fields = ['active', 'search']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value)
        )

    def filter_active(self, queryset, name, value):
        if value == 'all' or value is None:
            return queryset
        else:
            return queryset.filter(active=str_to_bool(value))


class BimaHrSkillViewSet(AbstractViewSet):
    queryset = BimaHrSkill.objects.all()
    serializer_class = BimaHrSkillSerializer
    permission_classes = []
    filterset_class = BimaHrSkillFilter
    #permission_classes = (ActionBasedPermission,)
    action_permissions = {
        'list': ['skill.can_read'],
        'create': ['skill.can_create'],
        'retrieve': ['skill.can_read'],
        'update': ['skill.can_update'],
        'partial_update': ['skill.can_update'],
        'destroy': ['skill.can_delete'],
    }

    def get_object(self):
        obj = BimaHrSkill.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
