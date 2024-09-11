from rest_framework import generics

from habits.models import Habit
from habits.paginations import HabitListPagination
from habits.permissions import IsOwner, IsPublic
from habits.serializers import HabitSerializer
from habits.tasks import send_habit_reminder


# Create your views here.
class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        next_date = serializer.validated_data["first_date"]
        habit = serializer.save(user=self.request.user, next_date=next_date)

        try:
            tg_id = self.request.user.telegram_id
            habit_id = habit.pk
            send_habit_reminder.apply_async((habit_id, tg_id), eta=habit.next_date)
        except Exception as e:
            print(f"Failed to send reminder for habit {habit.pk}: {e}")


class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = HabitListPagination

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsPublic | IsOwner,)


class HabitPublicListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = HabitListPagination

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)


class HabitUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)


class HabitDestroyAPIView(generics.DestroyAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)
