# serializers.py
from rest_framework import serializers
from .models import *


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class FileSerializer(serializers.Serializer):
    class Meta:
        model = Transaction
        fields = ['fileName', 'fileDate']


class ImportSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportSchema
        fields = '__all__'


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    color = serializers.SerializerMethodField()
    categoryName = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = '__all__'

    def get_color(self, obj):
        color = obj.category.color
        return color

    def get_categoryName(self, obj):
        categoryName = obj.category.name
        return categoryName
