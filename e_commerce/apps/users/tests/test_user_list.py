from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from e_commerce.apps.users.models import User
from e_commerce.apps.users.views import UserListCreateView


class UserCreationTest(APITestCase):
    def create_dummy_users(self):
        """Create n users"""
        for ind in range(self.total_users):
            self.client.post(self.url, {
                "full_name": f'Test User {ind}',
                "password": "test-password",
                "password2": "test-password",
                'username': f"testUser{ind}"
            })

    def setUp(self):
        self.admin = User.objects.create_superuser("admin", 
                                                    "admin@admin.com", 
                                                        "admin")
        self.view = UserListCreateView.as_view({"get": "list", 
                                                    "post": "create"} )
        self.url = reverse('user-list')
        
        self.total_users = 5
        self.create_dummy_users()

    def test_list_all_users(self):
        """
        Test checks whether the admin user can see all users in the database.
        """
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code,  status.HTTP_200_OK)
        self.assertEqual(len(response.json()),  self.total_users+1)

    def test_get_user_list_without_authentication(self):
        """
        Anonymus user cannot access to the list of users.
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code,  status.HTTP_403_FORBIDDEN)
        self.assertDictEqual(response.json(), {
                    'detail': 'Authentication credentials were not provided.'
                })
    
    def test_non_superuser_gets_only_his_user(self):
        """
        Non-super user can access only his credentials.
        """
        user = User.objects.filter(is_superuser=False).first()
        
        self.client.force_authenticate(user=user)
        response = self.client.get(self.url)
        breakpoint()
        self.assertEqual(response.status_code,  status.HTTP_403_FORBIDDEN)
        self.assertDictEqual(response.json(), {
                    'detail': 'Authentication credentials were not provided.'
                })
