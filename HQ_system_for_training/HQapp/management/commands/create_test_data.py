from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from HQapp.models import Product, Lesson, UserLessonView
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
        UserLessonView.objects.all().delete()

        # Create some test users
        users = []
        for _ in range(10):
            username = f"{fake.user_name()}{random.randint(1000, 9999)}"  # Добавляем к имени пользователя уникальное число
            email = fake.email()
            password = 'testpassword'

            user = User.objects.create_user(username, email, password)
            users.append(user)
        #superuser = User.objects.create_superuser('superuser', 'superuser@example.com', 'superpassword')

        # Create some test products and lessons with fake data
        for _ in range(10):  # e.g. creating 5 products and 10 lessons
            product = Product.objects.create(title=fake.word(), owner=random.choice(users))
            product.users_with_access.set(random.sample(users, k=3))  # Randomly adding 3 users with access to this product

            for _ in range(10):
                lesson = Lesson.objects.create(
                    title=fake.sentence(),
                    video_link=fake.url(),
                    duration=fake.random_int(min=300, max=3600)  # Duration between 5 mins and 1 hour
                )
                product.lessons.add(lesson)

                for user in users:  # Создаем объекты UserLessonView для каждого пользователя и урока
                    UserLessonView.objects.create(
                        user=user,
                        lesson=lesson,
                        viewed_duration=random.randint(0, lesson.duration),  # Случайное значение от 0 до duration
                    )
        self.stdout.write(self.style.SUCCESS('Successfully created test data'))
