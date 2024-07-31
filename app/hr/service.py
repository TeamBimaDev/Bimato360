<<<<<<< HEAD
from django.utils.translation import gettext_lazy as _
from hr.models import BimaHrPersonExperience
from hr.serializers import BimaHrPersonExperienceSerializer
from hr.skill.models import BimaHrPersonSkill
from hr.skill.models import BimaHrSkill
from rest_framework.exceptions import NotFound, ValidationError


def get_skill_by_public_id(skill_public_id):
    try:
        return BimaHrSkill.objects.get_object_by_public_id(public_id=skill_public_id)
    except BimaHrSkill.DoesNotExist:
        raise NotFound(detail={'error': 'Skill not found'})


def add_or_update_person_skill(person, skill_public_id, level):
    skill = get_skill_by_public_id(skill_public_id)
    person_skill, created = _get_or_update_person_skill_instance(person, skill, level)
    return person_skill, created


def _get_or_update_person_skill_instance(person, skill, level):
    try:
        person_skill = BimaHrPersonSkill.objects.get(person=person, skill=skill)
        person_skill.level = level
        person_skill.save(update_fields=['level'])
        created = False
    except BimaHrPersonSkill.DoesNotExist:
        person_skill = BimaHrPersonSkill.objects.create(person=person, skill=skill, level=level)
        created = True

    return person_skill, created


def delete_person_skill(person, skill_public_id):
    skill = get_skill_by_public_id(skill_public_id)
    try:
        person_skill = BimaHrPersonSkill.objects.get(person=person, skill=skill)
        person_skill.delete()
    except BimaHrPersonSkill.DoesNotExist:
        raise NotFound(detail={'error': _('Skill not found for this person')})


def get_experience_by_public_id(public_id):
    try:
        return BimaHrPersonExperience.objects.get_object_by_public_id(public_id=public_id)
    except BimaHrPersonExperience.DoesNotExist:
        raise NotFound(detail={'error': _('Experience not found')})


def add_or_update_person_experience(person, experience_data):
    experience_id = experience_data.get('experience_public_id')

    if experience_id:
        try:
            experience = get_experience_by_public_id(experience_id)
        except NotFound:
            raise NotFound(detail={'error': _('Experience not found')})
    else:
        experience = None

    serializer = BimaHrPersonExperienceSerializer(instance=experience, data=experience_data)
    if serializer.is_valid():
        serializer.save(person=person)
        return serializer.data, not bool(experience)
    else:
        raise ValidationError(serializer.errors)


def delete_person_experience(person, experience_public_id):
    try:
        experience = get_experience_by_public_id(experience_public_id)
        if experience.person.public_id.hex != person.public_id.hex:
            raise NotFound(detail={'error': _('Experience not found for this person')})
        experience.delete()
    except BimaHrPersonExperience.DoesNotExist:
        raise NotFound(detail={'error': _('Experience not found')})
=======
from django.utils.translation import gettext_lazy as _
from hr.models import BimaHrPersonExperience
from hr.serializers import BimaHrPersonExperienceSerializer
from hr.skill.models import BimaHrPersonSkill
from hr.skill.models import BimaHrSkill
from rest_framework.exceptions import NotFound, ValidationError


def get_skill_by_public_id(skill_public_id):
    try:
        return BimaHrSkill.objects.get_object_by_public_id(public_id=skill_public_id)
    except BimaHrSkill.DoesNotExist:
        raise NotFound(detail={'error': 'Skill not found'})


def add_or_update_person_skill(person, skill_public_id, level):
    skill = get_skill_by_public_id(skill_public_id)
    person_skill, created = _get_or_update_person_skill_instance(person, skill, level)
    return person_skill, created


def _get_or_update_person_skill_instance(person, skill, level):
    try:
        person_skill = BimaHrPersonSkill.objects.get(person=person, skill=skill)
        person_skill.level = level
        person_skill.save(update_fields=['level'])
        created = False
    except BimaHrPersonSkill.DoesNotExist:
        person_skill = BimaHrPersonSkill.objects.create(person=person, skill=skill, level=level)
        created = True

    return person_skill, created


def delete_person_skill(person, skill_public_id):
    skill = get_skill_by_public_id(skill_public_id)
    try:
        person_skill = BimaHrPersonSkill.objects.get(person=person, skill=skill)
        person_skill.delete()
    except BimaHrPersonSkill.DoesNotExist:
        raise NotFound(detail={'error': _('Skill not found for this person')})


def get_experience_by_public_id(public_id):
    try:
        return BimaHrPersonExperience.objects.get_object_by_public_id(public_id=public_id)
    except BimaHrPersonExperience.DoesNotExist:
        raise NotFound(detail={'error': _('Experience not found')})


def add_or_update_person_experience(person, experience_data):
    experience_id = experience_data.get('experience_public_id')

    if experience_id:
        try:
            experience = get_experience_by_public_id(experience_id)
        except NotFound:
            raise NotFound(detail={'error': _('Experience not found')})
    else:
        experience = None

    serializer = BimaHrPersonExperienceSerializer(instance=experience, data=experience_data)
    if serializer.is_valid():
        serializer.save(person=person)
        return serializer.data, not bool(experience)
    else:
        raise ValidationError(serializer.errors)


def delete_person_experience(person, experience_public_id):
    try:
        experience = get_experience_by_public_id(experience_public_id)
        if experience.person.public_id.hex != person.public_id.hex:
            raise NotFound(detail={'error': _('Experience not found for this person')})
        experience.delete()
    except BimaHrPersonExperience.DoesNotExist:
        raise NotFound(detail={'error': _('Experience not found')})
>>>>>>> origin/ma-branch
