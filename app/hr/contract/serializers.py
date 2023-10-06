from core.abstract.serializers import AbstractSerializer
from core.department.models import BimaCoreDepartment
from django.utils.translation import gettext_lazy as _
from hr.employee.models import BimaHrEmployee
from rest_framework import serializers

from .models import BimaHrContract, BimaHrContractAmendment


class BimaHrContractSerializer(AbstractSerializer):
    employee = serializers.SerializerMethodField(read_only=True)
    employee_public_id = serializers.SlugRelatedField(
        queryset=BimaHrEmployee.objects.all(),
        slug_field='public_id',
        source='employee',
        write_only=True
    )

    department = serializers.SerializerMethodField(read_only=True)
    department_public_id = serializers.SlugRelatedField(
        queryset=BimaCoreDepartment.objects.all(),
        slug_field='public_id',
        source='department',
        write_only=True,
        required=False,
        allow_null=True,
        allow_empty=True
    )

    manager_who_stopped = serializers.SerializerMethodField(read_only=True)
    manager_who_stopped_public_id = serializers.SlugRelatedField(
        queryset=BimaHrEmployee.objects.all(),
        slug_field='public_id',
        source='manager_who_stopped',
        write_only=True,
        required=False,
        allow_null=True,
        allow_empty=True
    )

    def get_employee(self, obj):
        return {
            'id': obj.employee.public_id.hex,
            'name': obj.employee.full_name,
        }

    def get_department(self, obj):
        return {
            'id': obj.department.public_id.hex,
            'name': obj.department.full_name,
        }

    def get_manager_who_stopped(self, obj):
        if obj.manager_who_stopped:
            return {
                'id': obj.manager_who_stopped.public_id.hex,
                'name': obj.manager_who_stopped.full_name,
            }
        return None

    class Meta:
        model = BimaHrContract
        fields = [
            'id', 'name', 'employee', 'employee_public_id', 'start_date', 'end_date', 'contract_type', 'salary', 'note',
            'job_description', 'department', 'department_public_id', 'manager_who_stopped', 'status', 'stopped_at',
            'reason_stopped', 'manager_who_stopped_public_id', 'created', 'updated'
        ]

    def validate(self, data):
        if data['date_end'] and data['date_end'] < data['date_start']:
            raise serializers.ValidationError({
                "date_end": _("End date must be on or after the start date.")
            })
        return data


class BimaHrContractHistorySerializer(serializers.ModelSerializer):
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


class BimaHrContractAmendmentSerializer(AbstractSerializer):
    contract = serializers.SerializerMethodField(read_only=True)
    contract_public_id = serializers.SlugRelatedField(
        queryset=BimaHrContract.objects.all(),
        slug_field='public_id',
        source='contract',
        write_only=True
    )

    def get_contract(self, obj):
        return {
            'id': obj.contract.public_id.hex,
            'name': obj.contract.name,
        }

    class Meta:
        model = BimaHrContractAmendment
        fields = [
            'id', 'contract', 'contract_public_id', 'amendment_date', 'notes',
            'new_salary', 'new_end_date', 'other_changes', 'status', 'created', 'updated'
        ]
