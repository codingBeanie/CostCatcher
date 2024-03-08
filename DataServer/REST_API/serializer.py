# serializers.py
from rest_framework import serializers
from .models import Transaction, ImportSchema, Category, Assignment


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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'
