
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .models import BimaHrOffre
from .serializers import BimaHrOffreSerializer
from common.permissions.action_base_permission import ActionBasedPermission
from langchain_community.llms import Ollama

class BimaHrOffreViewSet(viewsets.ModelViewSet):
    queryset = BimaHrOffre.objects.all()
    serializer_class = BimaHrOffreSerializer
    permission_classes = [ActionBasedPermission]
    action_permissions = {
        'list': ['offre.can_read'],
        'create': ['offre.can_create'],
        'retrieve': ['offre.can_read'],
        'update': ['offre.can_update'],
        'partial_update': ['offre.can_update'],
        'destroy': ['offre.can_delete'],
        'description': ['offre.can.generate_description'],
    }

    def generate_job_description(self, offre):
        # Load the Ollama model (replace with the actual model setup)
        llm = Ollama(model="llama2")

        # Extract data from the BimaHrOffre instance
        jobTitle = offre.title
        industry = offre.work_location
        numWords = 200  # Default number of words
        tone = offre.tone or 'neutre'
        emojisString = '😊🚀' if offre.inclusive_emojis else ''
        inclusiveLocalisation = offre.inclusive_location
        includeDesc = offre.include_desc
        salaire = offre.salary
        inclusiveEtude = offre.inclusive_education
        inclusiveExperience = offre.inclusive_experience
        selectedHardSkills = offre.selected_hard_skills
        selectedSoftSkills = offre.selected_soft_skills
        CandidatType = ""  # Assuming this field is not in the model
        inclusiveContact = offre.inclusive_contact

        # Build the prompt
        prompt = f"""En tant que responsable de recrutement rédige moi une offre d'emploi en {jobTitle}
        {f"dans l'entreprise {industry}" if industry else ""} qui comporte environ {numWords} mots dans un ton {tone} pour le postuler sur LinkedIn{emojisString}.
        La structure de l'offre est divisée en 4 parties (les titres des parties doivent écrites en gras):
        Le poste devrait être décrit de manière conviviale pour le référencement (SEO), en mettant en évidence ses caractéristiques et avantages uniques.
        
        Voila la structure de l'offre :
        
        **A propos de nous**
        - Besoin de l'entreprise (brève description contient {f"la localisation de l'entreprise." if inclusiveLocalisation else ""} ne dépassant pas 2 lignes)
        
        **Les missions du poste**
        - Définir les missions du poste {f"en prenant en compte la description de l'entreprise dans le processus de génération {includeDesc}" if includeDesc else ""} (sous forme des puces)
        
        **Nous vous offrons**
        - Décrire l'environnement du travail et les bénéfices de la poste par l'entreprise, {f"Inclure la plage de salaire : {salaire} à offrir par l'entreprise" if salaire else ""} (sous forme des puces)
        
        **Profil recherché**
        - Pour définir le Profil souhaité de candidat sous forme de puces (en premier ligne mentionner {f"le niveau d'étude requis: {inclusiveEtude}" if inclusiveEtude else ""} et {f"l'expérience requise: {inclusiveExperience}" if inclusiveExperience else ""},
        en deuxième ligne {f"Incorporez les mots clés suivants : {selectedHardSkills} pour définir les hard skills" if selectedHardSkills else ""}
        en troisième ligne {f"Incorporez les mots clés suivants : {selectedSoftSkills} pour définir les soft skills)" if selectedSoftSkills else ""}. {f"Définir le profil recherché selon le type de candidat ciblé {CandidatType}" if CandidatType else ""}
        
        Ajouter aussi : la Prise de poste, Lieu de travail - {f"Inclure le type de contact à utiliser pour postuler : {inclusiveContact}" if inclusiveContact else ""} (telque Mail de candidature)
        
        Commencer! N'oubliez pas de respecter la structure de l'offre définie par le responsable de recrutement lorsque vous donnez votre réponse finale."""

        # Generate the job description
        generated_text = llm.invoke(prompt)
        return generated_text

    @action(detail=True, methods=['post'], url_path='generate-description')
    def generate_description(self, request, pk=None):
        offre = self.get_object()

        # Generate the job description
        generated_content = self.generate_job_description(offre)
        print(generated_content)

        # Update the generated_content field in the database
        offre.generated_content = generated_content
        offre.save()

        if offre.title:
            vacancie = offre.title
            vacancie.description = generated_content
            vacancie.save()
            
        serializer = self.get_serializer(offre)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='create-offre')
    def create_offre(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='read-offre')
    def read_offre(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['put'], url_path='update-offre')
    def update_offre(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['delete'], url_path='delete-offre')
    def delete_offre(self, request, pk=None):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='list-offres')
    def list_bimahr_offres(self, request):
        offres = BimaHrOffre.objects.all().order_by('created')
        serializer = BimaHrOffreSerializer(offres, many=True)
        return JsonResponse(serializer.data, safe=False)
























'''from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BimaHrOffre
from hr.vacancie.models import BimaHrVacancie
from .serializers import BimaHrOffreSerializer
from langchain_community.llms import Ollama
from django.http import JsonResponse
from common.permissions.action_base_permission import ActionBasedPermission
import json
from rest_framework.permissions import IsAuthenticated



class BimaHrOffreViewSet(viewsets.ModelViewSet):
    queryset = BimaHrOffre.objects.all()
    serializer_class = BimaHrOffreSerializer
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        'list': ['offre.can_read'],
        'create': ['offre.can_create'],
        'retrieve': ['offre.can_read'],
        'update': ['offre.can_update'],
        'partial_update': ['offre.can_update'],
        'destroy': ['offre.can_delete'],
        'description': ['offre.can.generate_description'],
        
    }
    
    
    def generate_job_description(self, offre):
        # Load the Ollama model (replace with the actual model setup)
        llm = Ollama(model="llama2")

        # Extract data from the BimaHrOffre instance
        jobTitle = offre.title
        industry = offre.work_location
        numWords = 200  # Default number of words
        tone = offre.tone or 'neutre'
        emojisString = '😊🚀' if offre.inclusive_emojis else ''
        inclusiveLocalisation = offre.inclusive_location
        includeDesc = offre.include_desc
        salaire = offre.salary
        inclusiveEtude = offre.inclusive_education
        inclusiveExperience = offre.inclusive_experience
        selectedHardSkills = offre.selected_hard_skills
        selectedSoftSkills = offre.selected_soft_skills
        CandidatType = ""  # Assuming this field is not in the model
        inclusiveContact = offre.inclusive_contact

        # Build the prompt
        prompt = f"""En tant que responsable de recrutement rédige moi une offre d'emploi en {jobTitle}
        {f"dans l'entreprise {industry}" if industry else ""} qui comporte environ {numWords} mots dans un ton {tone} pour le postuler sur LinkedIn{emojisString}.
        La structure de l'offre est divisée en 4 parties (les titres des parties doivent écrites en gras):
        Le poste devrait être décrit de manière conviviale pour le référencement (SEO), en mettant en évidence ses caractéristiques et avantages uniques.
        
        Voila la structure de l'offre :
        
        **A propos de nous**
        - Besoin de l'entreprise (brève description contient {f"la localisation de l'entreprise." if inclusiveLocalisation else ""} ne dépassant pas 2 lignes)
        
        **Les missions du poste**
        - Définir les missions du poste {f"en prenant en compte la description de l'entreprise dans le processus de génération {includeDesc}" if includeDesc else ""} (sous forme des puces)
        
        **Nous vous offrons**
        - Décrire l'environnement du travail et les bénéfices de la poste par l'entreprise, {f"Inclure la plage de salaire : {salaire} à offrir par l'entreprise" if salaire else ""} (sous forme des puces)
        
        **Profil recherché**
        - Pour définir le Profil souhaité de candidat sous forme de puces (en premier ligne mentionner {f"le niveau d'étude requis: {inclusiveEtude}" if inclusiveEtude else ""} et {f"l'expérience requise: {inclusiveExperience}" if inclusiveExperience else ""},
        en deuxième ligne {f"Incorporez les mots clés suivants : {selectedHardSkills} pour définir les hard skills" if selectedHardSkills else ""}
        en troisième ligne {f"Incorporez les mots clés suivants : {selectedSoftSkills} pour définir les soft skills)" if selectedSoftSkills else ""}. {f"Définir le profil recherché selon le type de candidat ciblé {CandidatType}" if CandidatType else ""}
        
        Ajouter aussi : la Prise de poste, Lieu de travail - {f"Inclure le type de contact à utiliser pour postuler : {inclusiveContact}" if inclusiveContact else ""} (telque Mail de candidature)
        
        Commencer! N'oubliez pas de respecter la structure de l'offre définie par le responsable de recrutement lorsque vous donnez votre réponse finale."""

        # Generate the job description
        generated_text = llm.invoke(prompt)
        return generated_text

    @action(detail=True, methods=['post'])
    def generate_description(self, request, pk=None):
        offre = self.get_object()

        # Generate the job description
        generated_content = self.generate_job_description(offre)  
        print(generated_content)

        # Update the generated_content field in the database
        offre.generated_content = generated_content
        offre.save()

        if offre.title:
            vacancie = offre.title
            vacancie.description = generated_content
            vacancie.save()
            
        serializer = self.get_serializer(offre)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'],url_path='create-offre')
    def create_offre(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='read-offre')
    def read_offre(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['put'], url_path='update-offre')
    def update_offre(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['delete'], url_path='delete-offre')
    def delete_offre(self, request, pk=None):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path='generate-description')
    def generate_description(self, request, pk=None):
        offre = self.get_object()

        # Generate the job description
        generated_content = self.generate_job_description(offre)

        # Update the generated_content field in the database
        offre.generated_content = generated_content
        offre.save()

        if offre.title:
            vacancie = offre.title
            vacancie.description = generated_content
            vacancie.save()

        serializer = self.get_serializer(offre)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='list-offres')
    def list_bimahr_offres(self, request):
        offres = BimaHrOffre.objects.all().order_by('created')  
        serializer = BimaHrOffreSerializer(offres, many=True)
        return JsonResponse(serializer.data, safe=False)
'''









   