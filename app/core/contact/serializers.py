from core.contact.models import BimaCoreContact
from core.abstract.serializers import AbstractSerializer


class BimaCoreContactserializer(AbstractSerializer):

    class Meta:
        model = BimaCoreContact
        fields = '__all__'
