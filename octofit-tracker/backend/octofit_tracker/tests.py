from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Activity, LeaderboardEntry, Team, User, Workout


class OctoFitAPITestCase(APITestCase):
    def setUp(self):
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

        Activity.objects.create(
            user=self.user_tony,
            activity_type='running',
            duration_minutes=30,
            distance_km=5.0,
        )

        Workout.objects.create(
            user=self.user_tony,
            name='Strength',
            description='Strength workout',
            scheduled_at='2026-01-01T10:00:00Z',
        )

        LeaderboardEntry.objects.create(user=self.user_tony, score=100.0, rank=1)

    def test_users_list(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_teams_list(self):
        url = reverse('team-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_activities_list(self):
        url = reverse('activity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_leaderboard_list(self):
        url = reverse('leaderboard-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_workouts_list(self):
        url = reverse('workout-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
