<<<<<<< HEAD
from core.abstract.serializers import AbstractSerializer
from django.db.models import ForeignKey
from hr.activity_type.models import BimaHrActivityType
from hr.employee.models import BimaHrEmployee
from rest_framework import serializers

from .models import BimaHrActivity, BimaHrActivityParticipant
from ..models import BimaHrPerson


class BimaHrActivitySerializer(AbstractSerializer):
    organizer = serializers.SerializerMethodField(read_only=True)
    organizer_public_id = serializers.SlugRelatedField(
        queryset=BimaHrEmployee.objects.all(),
        slug_field='public_id',
        source='organizer',
        write_only=True
    )

    def get_organizer(self, obj):
        return {
            'id': obj.organizer.public_id.hex,
            'name': obj.organizer.full_name,
        }

    activity_type = serializers.SerializerMethodField(read_only=True)
    activity_type_public_id = serializers.SlugRelatedField(
        queryset=BimaHrActivityType.objects.all(),
        slug_field='public_id',
        source='activity_type',
        write_only=True
    )

    def get_activity_type(self, obj):
        return {
            'id': obj.activity_type.public_id.hex,
            'name': obj.activity_type.name,
        }

    class Meta:
        model = BimaHrActivity
        fields = [
            'id', 'name', 'description', 'status', 'start_date', 'end_date', 'activity_type',
            'activity_type_public_id', 'organizer', 'organizer_public_id', 'created', 'updated'
        ]


class BimaHrActivityHistorySerializer(serializers.ModelSerializer):
    changes = serializers.SerializerMethodField()
    changed_by = serializers.SerializerMethodField()

    class Meta:
        model = BimaHrActivity.history.model
        fields = ("id", "changes", "changed_by", "history_date")

    def get_changes(self, instance):
        changes = []
        if instance.prev_record:
            diffs = instance.diff_against(instance.prev_record)
            for change in diffs.changes:
                old_value = self.get_readable_value(change.field, change.old)
                new_value = self.get_readable_value(change.field, change.new)
                changes.append(
                    {"field": change.field, "old": old_value, "new": new_value}
                )
        return changes

    def get_readable_value(self, field, value):
        model_cls = self.Meta.model

        field_obj = model_cls._meta.get_field(field)

        if isinstance(field_obj, ForeignKey):
            related_model_cls = field_obj.related_model
            try:
                related_obj = related_model_cls.objects.get(pk=value)
                return str(related_obj)
            except related_model_cls.DoesNotExist:
                return ""
        else:
            return value

    def get_changed_by(self, instance):
        return instance.history_user.name if instance.history_user else None


class BimaHrActivityParticipantSerializer(AbstractSerializer):
    activity = serializers.SerializerMethodField(read_only=True)
    activity_public_id = serializers.SlugRelatedField(
        queryset=BimaHrActivity.objects.all(),
        slug_field='public_id',
        source='activity',
        write_only=True
    )

    person = serializers.SerializerMethodField(read_only=True)
    person_public_id = serializers.SlugRelatedField(
        queryset=BimaHrPerson.objects.all(),
        slug_field='public_id',
        source='person',
        write_only=True
    )

    def get_activity(self, obj):
        return {
            'id': obj.activity.public_id.hex,
            'name': obj.activity.name,
            'status': obj.activity.status,
            'start_date': obj.activity.start_date,
            'end_date': obj.activity.end_date,
            'activity_type': obj.activity.activity_type.name,
        }

    def get_person(self, obj):
        return {
            'id': obj.person.public_id.hex,
            'full_name': f"{obj.person.full_name}",
        }

    class Meta:
        model = BimaHrActivityParticipant
        fields = [
            'id', 'activity', 'activity_public_id', 'person', 'person_public_id',
            'presence_status', 'created', 'updated'
        ]
=======
from core.abstract.serializers import AbstractSerializer
from django.db.models import ForeignKey
from hr.activity_type.models import BimaHrActivityType
from hr.employee.models import BimaHrEmployee
from rest_framework import serializers

from .models import BimaHrActivity, BimaHrActivityParticipant
from ..models import BimaHrPerson


class BimaHrActivitySerializer(AbstractSerializer):
    organizer = serializers.SerializerMethodField(read_only=True)
    organizer_public_id = serializers.SlugRelatedField(
        queryset=BimaHrEmployee.objects.all(),
        slug_field='public_id',
        source='organizer',
        write_only=True
    )

    def get_organizer(self, obj):
        return {
            'id': obj.organizer.public_id.hex,
            'name': obj.organizer.full_name,
        }

    activity_type = serializers.SerializerMethodField(read_only=True)
    activity_type_public_id = serializers.SlugRelatedField(
        queryset=BimaHrActivityType.objects.all(),
        slug_field='public_id',
        source='activity_type',
        write_only=True
    )

    def get_activity_type(self, obj):
        return {
            'id': obj.activity_type.public_id.hex,
            'name': obj.activity_type.name,
        }

    class Meta:
        model = BimaHrActivity
        fields = [
            'id', 'name', 'description', 'status', 'start_date', 'end_date', 'activity_type',
            'activity_type_public_id', 'organizer', 'organizer_public_id', 'created', 'updated'
        ]


class BimaHrActivityHistorySerializer(serializers.ModelSerializer):
    changes = serializers.SerializerMethodField()
    changed_by = serializers.SerializerMethodField()

    class Meta:
        model = BimaHrActivity.history.model
        fields = ("id", "changes", "changed_by", "history_date")

    def get_changes(self, instance):
        changes = []
        if instance.prev_record:
            diffs = instance.diff_against(instance.prev_record)
            for change in diffs.changes:
                old_value = self.get_readable_value(change.field, change.old)
                new_value = self.get_readable_value(change.field, change.new)
                changes.append(
                    {"field": change.field, "old": old_value, "new": new_value}
                )
        return changes

    def get_readable_value(self, field, value):
        model_cls = self.Meta.model

        field_obj = model_cls._meta.get_field(field)

        if isinstance(field_obj, ForeignKey):
            related_model_cls = field_obj.related_model
            try:
                related_obj = related_model_cls.objects.get(pk=value)
                return str(related_obj)
            except related_model_cls.DoesNotExist:
                return ""
        else:
            return value

    def get_changed_by(self, instance):
        return instance.history_user.name if instance.history_user else None


class BimaHrActivityParticipantSerializer(AbstractSerializer):
    activity = serializers.SerializerMethodField(read_only=True)
    activity_public_id = serializers.SlugRelatedField(
        queryset=BimaHrActivity.objects.all(),
        slug_field='public_id',
        source='activity',
        write_only=True
    )

    person = serializers.SerializerMethodField(read_only=True)
    person_public_id = serializers.SlugRelatedField(
        queryset=BimaHrPerson.objects.all(),
        slug_field='public_id',
        source='person',
        write_only=True
    )

    def get_activity(self, obj):
        return {
            'id': obj.activity.public_id.hex,
            'name': obj.activity.name,
        }

    def get_person(self, obj):
        return {
            'id': obj.person.public_id.hex,
            'full_name': f"{obj.person.full_name}",
        }

    class Meta:
        model = BimaHrActivityParticipant
        fields = [
            'id', 'activity', 'activity_public_id', 'person', 'person_public_id',
            'presence_status', 'created', 'updated'
        ]
>>>>>>> origin/ma-branch
