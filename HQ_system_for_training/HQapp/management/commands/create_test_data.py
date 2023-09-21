from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from HQapp.models import Product, Lesson
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Create test data for the application'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Optionally, clear existing data (be cautious with this in a real environment)
        Product.objects.all().delete()
        Lesson.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        # Create some test users
        users = [User.objects.create_user(fake.user_name(), fake.email(), 'testpassword') for _ in range(5)]
        superuser = User.objects.create_superuser('superuser', 'superuser@example.com', 'superpassword')

        # Create some test products and lessons with fake data
        for _ in range(5):  # e.g. creating 5 products and 10 lessons
            product = Product.objects.create(title=fake.word(), owner=random.choice(users))
            product.users_with_access.set(random.sample(users, k=3))  # Randomly adding 3 users with access to this product

            for _ in range(2):
                lesson = Lesson.objects.create(
                    title=fake.sentence(),
                    video_link=fake.url(),
                    duration=fake.random_int(min=300, max=3600)  # Duration between 5 mins and 1 hour
                )
                product.lessons.add(lesson)

        self.stdout.write(self.style.SUCCESS('Successfully created test data'))
