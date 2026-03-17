"""Django management command to populate the octofit_db with sample data.

This command uses the Django ORM to create test records for:
- users
- teams
- activities
- leaderboard
- workouts

Usage:
    python manage.py populate_db

"""

from django.core.management.base import BaseCommand
from django.utils import timezone

from octofit_tracker.models import Activity, LeaderboardEntry, Team, User, Workout


class Command(BaseCommand):
    help = 'octofit_db 데이터베이스에 테스트 데이터를 입력합니다.'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing data...')
        # Delete in dependency order
        Activity.objects.all().delete()
        LeaderboardEntry.objects.all().delete()
        Workout.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()

        self.stdout.write('Creating teams...')
        marvel = Team.objects.create(name='Marvel', description='Marvel Superhero Team')
        dc = Team.objects.create(name='DC', description='DC Superhero Team')

        self.stdout.write('Creating users...')
        users = [
            {'first_name': 'Tony', 'last_name': 'Stark', 'email': 'tony@stark.com', 'team': marvel},
            {'first_name': 'Steve', 'last_name': 'Rogers', 'email': 'steve@avengers.com', 'team': marvel},
            {'first_name': 'Bruce', 'last_name': 'Wayne', 'email': 'bruce@wayne.com', 'team': dc},
            {'first_name': 'Diana', 'last_name': 'Prince', 'email': 'diana@themyscira.com', 'team': dc},
        ]
        created_users = []
        for data in users:
            created_users.append(User.objects.create(**data))

        self.stdout.write('Creating activities...')
        for u in created_users:
            Activity.objects.create(
                user=u,
                activity_type='running',
                duration_minutes=30,
                distance_km=5.0,
            )
            Activity.objects.create(
                user=u,
                activity_type='cycling',
                duration_minutes=45,
                distance_km=15.0,
            )

        self.stdout.write('Creating workouts...')
        now = timezone.now()
        for u in created_users:
            Workout.objects.create(
                user=u,
                name='Full Body Strength',
                description='A basic full body strength training routine.',
                scheduled_at=now,
            )

        self.stdout.write('Creating leaderboard entries...')
        rank = 1
        for u in created_users:
            LeaderboardEntry.objects.create(
                user=u,
                score=1000 - rank * 50,
                rank=rank,
            )
            rank += 1

        self.stdout.write(self.style.SUCCESS('Database population complete.'))
