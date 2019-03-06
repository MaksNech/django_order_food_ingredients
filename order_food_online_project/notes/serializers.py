from rest_framework import serializers
from .models import Note, NotedModel
from foods.models import Dish, Order
from foods.serializers import DishSerializer, OrderSerializer


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'title', 'description', 'created_on')


class NoteTargetField(serializers.Field):

    def to_representation(self, obj):
        if obj.__class__ == Dish:
            return DishSerializer(obj).data
        elif obj.__class__ == Order:
            return OrderSerializer(obj).data


class NotedModelSerializer(serializers.ModelSerializer):
    note = serializers.PrimaryKeyRelatedField(queryset=Note.objects.all(), allow_null=False, required=True)
    target_object = NoteTargetField(source='content_object')

    class Meta:
        model = Note
        fields = ('id', 'note', 'target_object')
