"""
Tests for Animals
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.management import call_command

class GetAnimalsTest(TestCase):
    """
    Test module to GET Animals
    """

    def setUp(self):
        """ Creating some first """
        call_command('loaddata', 'initial_data.json', verbosity=0)  # Load fixtures
        self.user = User.objects.create_user(pk=1, username='testuser', password='12345')
        self.client = Client()

    def test_get_all_animals(self):
        """ try to retrieve all animals """
        response = self.client.get('/animals/')
        self.assertEqual(response.status_code, 302)
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/animals/')
        self.assertEqual(response.status_code, 200)

    def test_get_one_animal(self):
        """ try to retrieve individual animals """
        response = self.client.get('/animals/1')
        self.assertEqual(response.status_code, 302)
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/animals/1')
        self.assertEqual(response.status_code, 200)

    def test_claim_one_animal(self):
        """ try to claim individual animals """
        response = self.client.get('/animals/claim/1')
        self.assertEqual(response.status_code, 302)
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/animals/claim/1')
        self.assertEqual(response.status_code, 200)
