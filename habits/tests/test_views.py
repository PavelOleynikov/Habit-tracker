from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from habits.models import Habit
from users.models import User


class HabitCRUDTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email="test@example.com", password="testpassword")
        self.client.force_authenticate(user=self.user)
        self.habit_data = {
            "user": self.user,
            "place": "Test",
            "action": "Проверка",
            "time": "15:30",
            "period": 1,
            "reward": "Отдых",
            "time_success": 60,
            "is_pleasant": False,
        }
        self.public_habit_data = {
            "user": self.user,
            "place": "Public Place",
            "action": "Public Action",
            "time": "16:00",
            "period": 1,
            "reward": "Public Reward",
            "time_success": 60,
            "is_pleasant": False,
            "is_public": True,
        }

    def test_create_habit(self):
        """Тест создания привычки"""

        habit = Habit.objects.create(**self.habit_data)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(habit.action, "Проверка")

    def test_create_pleasant_habit(self):
        """Тест создания приятной привычки"""

        pleasant_data = {
            "place": "Pleasant Place",
            "action": "Pleasant Action",
            "time": "15:30",
            "time_success": 60,
            "is_pleasant": True,
        }

        response = self.client.post("/habits/new/", pleasant_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_habits(self):
        """Тест списка привычек"""

        Habit.objects.create(**self.habit_data)
        response = self.client.get("/habits/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_public_habits_list_view(self):
        """Тест списка публичных привычек"""

        Habit.objects.create(**self.public_habit_data)
        Habit.objects.create(**self.habit_data)
        response = self.client.get("/habits/public/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_habit(self):
        """Тест чтения привычки"""

        habit = Habit.objects.create(**self.habit_data)
        read_habit = Habit.objects.get(id=habit.id)
        self.assertEqual(read_habit.action, "Проверка")

    def test_update_habit(self):
        """Тест обновления привычки"""

        habit = Habit.objects.create(**self.habit_data)
        habit.action = "Updated Action"
        habit.save()
        updated_habit = Habit.objects.get(id=habit.id)
        self.assertEqual(updated_habit.action, "Updated Action")

    def test_delete_habit(self):
        """Тест удаления привычки"""

        habit = Habit.objects.create(**self.habit_data)
        habit.delete()
        self.assertEqual(Habit.objects.count(), 0)

    def test_retrieve_habit_not_owner(self):
        """Тест доступа к чужой привычке"""

        other_user = User.objects.create(email="other@example.com", password="testpassword")

        habit = Habit.objects.create(
            user=other_user,
            place=self.habit_data["place"],
            action=self.habit_data["action"],
            time=self.habit_data["time"],
            period=self.habit_data["period"],
            reward=self.habit_data["reward"],
            time_success=self.habit_data["time_success"],
            is_pleasant=self.habit_data["is_pleasant"],
        )

        response = self.client.get(f"/habits/{habit.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_public_habits_list_empty(self):
        """Тест пустого списка публичных привычек"""

        response = self.client.get("/habits/public/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
