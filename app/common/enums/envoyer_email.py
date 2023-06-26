from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def envoyer_email(request):
    sujet = request.data.get('sujet', '')
    message = request.data.get('message', '')
    destinataires = request.data.get('destinataires', [])

    send_mail(
        sujet,
        message,
        'expediteur@example.com',
        destinataires,
        fail_silently=False,
    )

    return Response({'message': 'E-mail envoyé avec succès !'})
