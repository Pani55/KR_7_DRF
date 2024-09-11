from rest_framework import serializers

from habits.models import Habit
from habits.validators import validate_duration


class HabitSerializer(serializers.ModelSerializer):
    action_duration = serializers.CharField(
        validators=[validate_duration], required=False
    )
    periodicity = serializers.IntegerField(min_value=1, max_value=7, required=False)
    user = serializers.CharField(read_only=True)

    def validate(self, attrs):
        if attrs.get("is_pleasant") and (
            attrs.get("reward") or attrs.get("relation_habit")
        ):
            raise serializers.ValidationError(
                "Pleasant habit cannot has a reward or relation habit"
            )
        if not attrs.get("is_pleasant"):
            if not (attrs.get("reward") or attrs.get("relation_habit")):
                raise serializers.ValidationError(
                    "Non-pleasant habit must have a reward or relation habit"
                )
        if attrs.get("reward") and attrs.get("relation_habit"):
            raise serializers.ValidationError(
                "Habit cannot have both: reward and relation habit"
            )
        if attrs.get("relation_habit") and not attrs.get("relation_habit").is_pleasant:
            raise serializers.ValidationError("Relation habit must be pleasant")

        return attrs

    class Meta:
        model = Habit
        fields = "__all__"
