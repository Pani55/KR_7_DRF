from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCaseIsOwner(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="testuser@test.su")
        self.habit = Habit.objects.create(
            user=self.user,
            action="Test habit",
            periodicity=5,
            reward="Test reward",
            place="Test place",
        )
        self.data = {
            "place": "New test place",
            "action": "New test action",
            "first_date": "2024-01-01T00:00:00",
            "next_date": "2024-01-01T00:00:00",
            "reward": "New test reward",
            "periodicity": 1,
            "duration": "02:00",
        }
        self.client.force_authenticate(user=self.user)

    def test_habit_create(self):
        url = reverse("habits:habit_create")
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)

    def test_habit_list(self):
        url = reverse("habits:habit_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 1)

    def test_habit_update(self):
        url = reverse("habits:habit_update", kwargs={"pk": self.habit.pk})
        response = self.client.put(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit = Habit.objects.get(pk=self.habit.pk)
        self.assertEqual(habit.place, "New test place")

    def test_habit_delete(self):
        url = reverse("habits:habit_delete", kwargs={"pk": self.habit.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)


class HabitTestCaseNotOwner(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(email="testuser1@test.su")
        self.user2 = User.objects.create(email="testuser2@test.su")
        self.habit = Habit.objects.create(
            user=self.user1,
            action="Test habit",
            periodicity=5,
            reward="Test reward",
            place="Test place",
        )
        self.data = {
            "place": "New test place",
            "action": "New test action",
            "first_date": "2024-01-01T00:00:00",
            "next_date": "2024-01-01T00:00:00",
            "reward": "New test reward",
            "periodicity": 1,
            "duration": "02:00",
        }
        self.client.force_authenticate(user=self.user2)

    def test_habit_update(self):
        url = reverse("habits:habit_update", args=(self.habit.pk,))
        response = self.client.patch(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Habit.objects.get(pk=self.habit.pk).place, "Test place")

    def test_habit_list(self):
        url = reverse("habits:habit_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 0)

    def test_habit_delete(self):
        url = reverse("habits:habit_delete", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Habit.objects.count(), 1)


class HabitTestCaseNotAuthenticated(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="testuser@test.su")
        self.habit = Habit.objects.create(
            user=self.user,
            action="Test habit",
            periodicity=5,
            reward="Test reward",
            place="Test place",
        )
        self.data = {
            "place": "New test place",
            "action": "New test action",
            "first_date": "2024-01-01T00:00:00",
            "next_date": "2024-01-01T00:00:00",
            "reward": "New test reward",
            "periodicity": 1,
            "duration": "02:00",
        }

    def test_habit_create(self):
        url = reverse("habits:habit_create")
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Habit.objects.count(), 1)

    def test_habit_update(self):
        url = reverse("habits:habit_update", args=(self.habit.pk,))
        response = self.client.patch(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Habit.objects.get(pk=self.habit.pk).place, "Test place")

    def test_habit_delete(self):
        url = reverse("habits:habit_delete", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Habit.objects.count(), 1)

    def test_habit_list(self):
        url = reverse("habits:habit_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
