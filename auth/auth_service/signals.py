from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver

User = get_user_model()

@receiver(post_migrate)
def create_root_user(sender, **kwargs):
    if sender.name == 'auth_service':
        user_name = settings.ROOT_NAME
        cpf = settings.ROOT_CPF
        email = settings.ROOT_EMAIL
        password = settings.ROOT_PASSWORD
        role = settings.ROOT_ROLE
    
        if not User.objects.filter(cpf=cpf).exists():
            User.objects.create_user_entity(role, cpf, email, password, name=user_name)
            print(f'Root user created: {user_name} - {cpf} - {email} - {role}')
        