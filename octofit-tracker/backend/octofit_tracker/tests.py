from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Activity, LeaderboardEntry, Team, User, Workout


class OctoFitAPITestCase(APITestCase):
    def setUp(self):
        # Create test data
        self.team_marvel = Team.objects.create(name='Marvel', description='Marvel Team')
        self.team_dc = Team.objects.create(name='DC', description='DC Team')

        self.user_tony = User.objects.create(
            first_name='Tony',
            last_name='Stark',
            email='tony@stark.com',
            team=self.team_marvel,
        )
        self.user_diana = User.objects.create(
            first_name='Diana',
            last_name='Prince',
            email='diana@themyscira.com',
            team=self.team_dc,
        )

        self.activity = Activity.objects.create(
            user=self.user_tony,
            activity_type='running',
            duration_minutes=30,
            distance_km=5.0,
        )

        self.workout = Workout.objects.create(
            user=self.user_tony,
            name='Strength',
            description='Strength workout',
            scheduled_at='2026-01-01T10:00:00Z',
        )

        self.leaderboard_entry = LeaderboardEntry.objects.create(
            user=self.user_tony,
            score=100.0,
            rank=1
        )

    # Team CRUD Tests
    def test_teams_list(self):
        url = reverse('team-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_team_create(self):
        url = reverse('team-list')
        data = {'name': 'Avengers', 'description': 'Superhero team'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Avengers')

    def test_team_detail(self):
        url = reverse('team-detail', args=[self.team_marvel.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Marvel')

    # User CRUD Tests
    def test_users_list(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_user_create(self):
        url = reverse('user-list')
        data = {
            'first_name': 'Bruce',
            'last_name': 'Banner',
            'email': 'bruce@banner.com',
            'team': self.team_marvel.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], 'bruce@banner.com')

    def test_user_detail(self):
        url = reverse('user-detail', args=[self.user_tony.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'tony@stark.com')

    def test_user_update(self):
        url = reverse('user-detail', args=[self.user_tony.id])
        data = {'first_name': 'Anthony'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Anthony')

    def test_user_delete(self):
        url = reverse('user-detail', args=[self.user_diana.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Activity CRUD Tests
    def test_activities_list(self):
        url = reverse('activity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_activity_create(self):
        url = reverse('activity-list')
        data = {
            'user': self.user_diana.id,
            'activity_type': 'swimming',
            'duration_minutes': 45,
            'distance_km': 2.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['activity_type'], 'swimming')

    # Leaderboard CRUD Tests
    def test_leaderboard_list(self):
        url = reverse('leaderboard-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    # Workout CRUD Tests
    def test_workouts_list(self):
        url = reverse('workout-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_workout_create(self):
        url = reverse('workout-list')
        data = {
            'user': self.user_diana.id,
            'name': 'Yoga',
            'description': 'Relaxing yoga session',
            'scheduled_at': '2026-01-02T14:00:00Z'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Yoga')

    # Filtering Tests
    def test_user_filter_by_team(self):
        url = reverse('user-list') + f'?team={self.team_marvel.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return only Marvel team members
        for user in response.data:
            self.assertEqual(user['team'], str(self.team_marvel.id))

    def test_activity_filter_by_type(self):
        url = reverse('activity-list') + '?activity_type=running'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for activity in response.data:
            self.assertEqual(activity['activity_type'], 'running')

    # Search Tests
    def test_user_search(self):
        url = reverse('user-list') + '?search=tony'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_team_search(self):
        url = reverse('team-list') + '?search=Marvel'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
