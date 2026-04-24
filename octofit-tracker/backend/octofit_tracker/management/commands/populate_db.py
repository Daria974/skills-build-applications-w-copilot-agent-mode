from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Try to clear using ORM, fallback to PyMongo if needed
        try:
            for model in [Leaderboard, Activity, User, Team, Workout]:
                model.objects.all().delete()
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'ORM delete failed: {e}. Attempting direct collection drop.'))
            from pymongo import MongoClient
            client = MongoClient('localhost', 27017)
            db = client['octofit_db']
            for coll in ['leaderboard', 'activities', 'users', 'teams', 'workouts']:
                db[coll].drop()
            client.close()

        # Teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Users
        tony = User.objects.create(name='Tony Stark', email='tony@marvel.com', team=marvel)
        steve = User.objects.create(name='Steve Rogers', email='steve@marvel.com', team=marvel)
        bruce = User.objects.create(name='Bruce Wayne', email='bruce@dc.com', team=dc)
        clark = User.objects.create(name='Clark Kent', email='clark@dc.com', team=dc)

        # Activities
        Activity.objects.create(user=tony, type='Running', duration=30, date=timezone.now())
        Activity.objects.create(user=steve, type='Cycling', duration=45, date=timezone.now())
        Activity.objects.create(user=bruce, type='Swimming', duration=60, date=timezone.now())
        Activity.objects.create(user=clark, type='Yoga', duration=20, date=timezone.now())

        # Workouts
        Workout.objects.create(name='Super Strength', description='Strength workout for heroes', suggested_for='Marvel')
        Workout.objects.create(name='Flight Training', description='Flight skills for heroes', suggested_for='DC')

        # Leaderboard
        Leaderboard.objects.create(user=tony, score=100)
        Leaderboard.objects.create(user=steve, score=90)
        Leaderboard.objects.create(user=bruce, score=95)
        Leaderboard.objects.create(user=clark, score=85)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))
