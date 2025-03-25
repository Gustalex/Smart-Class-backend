from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user_data = {
            'name': 'Test User',
            'cpf': '00000000001',
            'email': 'test_auth@example.com',
            'password': '123456',
            'role': 'manager'
        }
        self.user = User.objects.create_user_entity(
            name='testuser',
            cpf='00000000002',
            email='test@example.com',
            password='123456',
            role='manager'
        )

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        login_data = {
            'cpf': self.user.cpf, 
            'password': '123456'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_logout_user(self):
        login_data = {
            'cpf': self.user.cpf,
            'password': '123456'
        }
        login_response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', login_response.data)
        self.assertIn('refresh', login_response.data)
        access_token = login_response.data['access']
        refresh_token = login_response.data['refresh']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        logout_response = self.client.post(self.logout_url, {'refresh': refresh_token}, format='json')
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)

class UserTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.list_users_url = reverse('users')
        self.retrieve_user_url = reverse('user', args=[2])
        self.update_user_url = reverse('update_user', args=[2])
        self.delete_user_url = reverse('delete_user', args=[2])
        
        self.user = User.objects.create_user_entity(
            name='testuser',
            cpf='00000000002',
            email='test@example.com',
            password='123456',
            role='manager'
        )
        
        self.client.force_authenticate(user=self.user)

    def test_list_users(self):
        response = self.client.get(self.list_users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) 

    def test_retrieve_user(self):
        response = self.client.get(self.retrieve_user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_user(self):
        update_data = {
            'name': 'Updated Name', 
            'email': 'updated@example.com',
            'role': 'student',
            'curso': 1 
        }

        response = self.client.patch(self.update_user_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 
                    f"Response data: {response.data}")

        updated_user = User.objects.get(pk=2)
        self.assertEqual(updated_user.name, 'Updated Name')
        self.assertEqual(updated_user.email, 'updated@example.com')
        self.assertTrue(updated_user.is_student)
        self.assertEqual(updated_user.curso, 1)
        self.assertEqual(updated_user.cursos, [])
        
    def test_delete_user(self):
        response = self.client.delete(self.delete_user_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=2).exists())