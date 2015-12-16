from rest_framework import serializers
from cmdapp.models import todo, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User


class todoSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='todo-highlight', format='json')

    class Meta:
        model = todo
        fields = ('url', 'highlight', 'owner',
                  'title', 'todo', 'completed', 'language', 'style')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    cmdapp = serializers.HyperlinkedRelatedField(many=True, view_name='todo-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'cmdapp')