from common.enums.position import ContractStatus
from core.abstract.serializers import AbstractSerializer
from core.department.models import BimaCoreDepartment
from django.db.models import Q, ForeignKey
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
        if obj.department:
            return {
                'id': obj.department.public_id.hex,
                'name': obj.department.name,
            }
        return None

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
            'id', 'employee', 'employee_public_id', 'start_date', 'end_date', 'contract_type', 'salary', 'note',
            'job_description', 'department', 'department_public_id', 'manager_who_stopped', 'status', 'stopped_at',
            'reason_stopped', 'manager_who_stopped_public_id', 'probation_end_date', 'exit_notice_date', 'created',
            'updated'
        ]

    def validate(self, data):
        self.validate_date_range(data)
        self.validate_active_contract(data)
        self.validate_overlapping_contracts(data)
        return data

    def validate_date_range(self, data):
        if data['end_date'] and data['end_date'] < data['start_date']:
            raise serializers.ValidationError({
                "end_date": _("End date must be on or after the start date.")
            })

    def validate_active_contract(self, data):
        employee = data.get('employee', self.instance.employee if self.instance else None)
        current_status = data.get('status', None)
        if not employee:
            raise serializers.ValidationError({"employee": "An employee must be associated with the contract."})

        active_contract = BimaHrContract.objects.filter(
            employee=employee,
            status=ContractStatus.ACTIVE.name
        ).first()
        if active_contract and current_status == ContractStatus.ACTIVE.name and (
                self.instance is None or self.instance.pk != active_contract.pk):
            raise serializers.ValidationError({
                "contract": "This employee already has an active contract."
            })

    def validate_overlapping_contracts(self, data):
        employee = data.get('employee', self.instance.employee if self.instance else None)
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        overlapping_contracts = BimaHrContract.objects.filter(
            (Q(start_date__lte=start_date, end_date__gte=start_date) |
             Q(start_date__lte=end_date, end_date__gte=end_date)) &
            ~Q(pk=self.instance.pk if self.instance else None),
            employee=employee,
        )
        if overlapping_contracts.exists():
            raise serializers.ValidationError({
                "date": "The contract date range overlaps with an existing contract for this employee."
            })


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
            'contract': f"{obj.contract.start_date} {obj.contract.end_date} ",
        }

    class Meta:
        model = BimaHrContractAmendment
        fields = [
            'id', 'contract', 'contract_public_id', 'amendment_date', 'notes',
            'new_salary', 'new_end_date', 'new_start_date', 'other_changes', 'status', 'created', 'updated'
        ]

    def validate(self, data):
        self.validate_date_range(data)

        return data

    def validate_date_range(self, data):
        if data['new_end_date'] and data['new_start_date'] and data['new_end_date'] < data['new_start_date']:
            raise serializers.ValidationError({
                "end_date": _("End date must be on or after the start date.")
            })
