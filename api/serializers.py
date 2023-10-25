from rest_framework import serializers
from base.models import *
from django.contrib.auth.models import User
from drf_extra_fields.fields import Base64ImageField

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='idUser.username') #Esto permite hacer la relacion de la PK con el campo username
    class Meta:
        model = BlogPost
        fields = '__all__'

class CommentsSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='authorId.username')
    class Meta:
        model = Comments
        fields = '__all__'

class LikesSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source = 'idUser.username')
    class Meta:
        model = Likes
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class PhraseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phrase
        fields = '__all__'

class ChatBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatBot
        fields = '__all__'

class UserDetailsSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='idUser.username')  # Include username field from related User model
    picture = Base64ImageField(required=False)  # Nuevo ! ! ! ! ! ! ! !
    banner = Base64ImageField(required=False)
    class Meta:
        model = UserDetails
        fields = '__all__'

class UserBioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBio
        fields = '__all__'
