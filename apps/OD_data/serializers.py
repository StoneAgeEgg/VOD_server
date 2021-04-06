from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import UploadRecord, OneFrameData, LabelCategory
 
 
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')
 
 
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LabelCategory
        fields = '__all__'