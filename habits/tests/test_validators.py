from django.test import TestCase
from rest_framework.exceptions import ValidationError
from habits.validators import HabitValidator


class ValidatorSimpleTest(TestCase):
    """Тесты валидаторов"""

    def setUp(self):
        self.validator = HabitValidator()

    def test_time_success_valid(self):
        """Тест успешной валидации времени выполнения привычки"""

        attrs = {"time_success": 60}
        self.validator.validate_time_success(attrs)

    def test_time_success_invalid(self):
        """Тест неуспешной валидации времени выполнения привычки"""

        attrs = {"time_success": 121}
        with self.assertRaises(ValidationError):
            self.validator.validate_time_success(attrs)

    def test_time_success_none(self):
        """Тест валидации с None"""

        attrs = {"time_success": None}
        self.validator.validate_time_success(attrs)
