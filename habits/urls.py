from django.urls import path

from habits.apps import HabitsConfig
from habits.views import (HabitCreateAPIView, HabitListAPIView,
                          HabitPublicListAPIView, HabitUpdateAPIView,
                          HabitDestroyAPIView, HabitRetrieveAPIView)

app_name = HabitsConfig.name

urlpatterns = [
    path("habit_create/", HabitCreateAPIView.as_view(), name="habit_create"),
    path("habit_list/", HabitListAPIView.as_view(), name="habit_list"),
    path("habit_public_list/", HabitPublicListAPIView.as_view(), name="habit_public_list"),
    path("habit_retrieve/<int:pk>/", HabitRetrieveAPIView.as_view(), name="habit_retrieve"),
    path("habit_update/<int:pk>/", HabitUpdateAPIView.as_view(), name="habit_update"),
    path("habit_delete/<int:pk>/", HabitDestroyAPIView.as_view(), name="habit_delete"),
]
