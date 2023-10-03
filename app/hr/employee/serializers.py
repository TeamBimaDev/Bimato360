from datetime import datetime

from core.abstract.serializers import AbstractSerializer
from core.country.models import BimaCoreCountry
from hr.position.models import BimaHrPosition
from rest_framework import serializers

from .models import BimaHrEmployee


class BimaHrEmployeeSerializer(AbstractSerializer):
    full_name = serializers.ReadOnlyField()
    is_user_account_created = serializers.ReadOnlyField()
    country = serializers.SerializerMethodField(read_only=True)
    country_public_id = serializers.SlugRelatedField(
        queryset=BimaCoreCountry.objects.all(),
        slug_field='public_id',
        source='country',
        write_only=True,
        required=False,
        allow_null=True,
        allow_empty=True
    )

    position = serializers.SerializerMethodField(read_only=True)
    position_public_id = serializers.SlugRelatedField(
        queryset=BimaHrPosition.objects.all(),
        slug_field='public_id',
        source='position',
        write_only=True,
        required=False,
        allow_null=True,
        allow_empty=True
    )

    def get_country(self, obj):
        if obj.country:
            return {
                'id': obj.country.public_id.hex,
                'name': obj.country.name,
            }
        return None

    def get_position(self, obj):
        if obj.position:
            return {
                'id': obj.position.public_id.hex,
                'name': obj.position.title,
            }
        return None

    class Meta:
        model = BimaHrEmployee
        fields = [
            'id', 'unique_id', 'gender', 'marital_status', 'num_children', 'first_name', 'last_name', 'date_of_birth',
            'place_of_birth', 'country', 'position', 'position_public_id', 'country_public_id', 'nationality',
            'full_name', 'identity_card_number', 'phone_number', 'second_phone_number', 'email', 'education_level',
            'latest_degree', 'latest_degree_date', 'institute', 'employment_type', 'work_mode', 'job_type',
            'employment_status', 'probation_end_date', 'salary', 'is_user_account_created', 'created', 'updated'
        ]

    def validate(self, data):
        date_fields = ['last_performance_review', 'probation_end_date', 'hiring_date']
        for field_name in date_fields:
            date_value = data.get(field_name)
            if date_value:
                try:
                    datetime.strptime(str(date_value), '%Y-%m-%d')
                except ValueError:
                    data[field_name] = None
        return data


class EmployeeHistorySerializer(serializers.ModelSerializer):
    changes = serializers.SerializerMethodField()
    changed_by = serializers.SerializerMethodField()

    class Meta:
        model = BimaHrEmployee.history.model
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
        return value

    def get_changed_by(self, instance):
        return instance.history_user.name if instance.history_user else None
