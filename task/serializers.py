from rest_framework import serializers

from task.models import Task


class TaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=2, max_length=200)
    description = serializers.CharField(min_length=2, max_length=200)
    done_at = serializers.DateTimeField(
        required=False,
        input_formats=['%I:%M %p %d %B %Y'], format=None, allow_null=True,
        help_text='Accepted format is "12:01 PM 16 April 2019"',
        style={'input_type': 'text', 'placeholder': '12:01 AM 28 July 2019'},
    )
    deadline_at = serializers.DateTimeField(
        required=False,
        input_formats=['%I:%M %p %d %B %Y'], format=None, allow_null=True,
        help_text='Accepted format is "12:01 PM 16 April 2019"',
        style={'input_type': 'text', 'placeholder': '12:01 AM 28 July 2019'},
    )

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'done_at', 'deadline_at')

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def create(self, validated_data):
        return Task.objects.create(**validated_data)
