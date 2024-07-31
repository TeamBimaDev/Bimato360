from core.abstract.serializers import AbstractSerializer
from rest_framework import serializers
from hr.offer.models import BimaHrOffre
from hr.vacancie.models import BimaHrVacancie
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from hr.offer.models import BimaHrOffre
from common.enums.position import offreStatus


class BimaHrOffreSerializer(AbstractSerializer):
    title = serializers.SerializerMethodField(read_only=True)
    title_public_id = serializers.SlugRelatedField(
        queryset=BimaHrVacancie.objects.all(),
        slug_field='public_id',
        source='title',
        write_only=True
    )

    def get_title(self, obj):
        if obj.title:
            return {
                'id': obj.title.public_id.hex,
                'name': obj.title.title,  # Accessing the title field of BimaHrPosition
            }
        return None

    class Meta:
        model = BimaHrOffre
        fields = [
            'id', 'title', 'title_public_id', 'work_location', 'description', 'seniority', 'tone', 'salary', 
            'selected_hard_skills', 'selected_soft_skills', 'inclusive_emojis', 'include_desc', 'inclusive_education', 
            'inclusive_contact', 'inclusive_location', 'inclusive_experience', 'created', 'updated', 'generated_content', 'activated_at','stopped_at','status' 
        ]
        
    def validate(self, data):
        self.validate_date_range(data)
        
        return data

    def validate_date_range(self, data):
        if data['stopped_at'] and data['stopped_at'] < data['activated_at']:
            raise serializers.ValidationError({
                "end_date": _("End date must be on or after the start date.")
            })
            
<<<<<<< HEAD
             


=======
>>>>>>> origin/ma-branch


