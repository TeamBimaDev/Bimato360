from django.utils import timezone
from core.abstract.serializers import AbstractSerializer
from jsonschema import ValidationError
from common.enums.position import get_seniority_choices, get_tone_choices, get_offre_status_choices, offreStatus
from core.abstract.models import AbstractModel
import uuid


from django.db import models


    
class BimaHrOffre(AbstractModel):
    title = models.ForeignKey('BimaHrVacancie', on_delete=models.CASCADE, null=True)
    work_location = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    seniority = models.CharField(max_length=100, choices=get_seniority_choices(), blank=True, null=True)                             
    tone = models.CharField(max_length=50, choices=get_tone_choices(), blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    selected_hard_skills = models.TextField(blank=True, null=True)
    selected_soft_skills = models.TextField(blank=True, null=True)
    inclusive_emojis = models.BooleanField(default=False)
    include_desc = models.BooleanField(default=False)
    inclusive_education = models.CharField(max_length=100, blank=True, null=True)
    inclusive_contact = models.CharField(max_length=100, blank=True, null=True)
    inclusive_location = models.BooleanField(default=False)
    inclusive_experience = models.BooleanField(default=False)
    generated_content = models.TextField(blank=True, null=True)
    activated_at = models.DateField(null=True, blank=True)
    stopped_at = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20,choices=get_offre_status_choices(),default='Unpublished')
    

    def __str__(self) -> str:
        return f"{self.title}"
    
    def save(self, *args, **kwargs):
        self._verify_if_date_expired_change_status_to_expired()
        super().save(*args, **kwargs)

    
    def _verify_if_date_expired_change_status_to_expired(self):
        current_date = timezone.localdate()

        if self.activated_at and current_date >= self.activated_at and self.status == 'unpublished':
            self.status = 'published'

        if self.stopped_at and current_date >= self.stopped_at and self.status == 'published':
            self.status = 'unpublished'
    
    class Meta:
        ordering = ['title']
        permissions = []
        default_permissions = ()

    

    