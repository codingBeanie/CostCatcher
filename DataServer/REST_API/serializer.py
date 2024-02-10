# serializers.py
from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['sourceFile', 'sourceFileDate']
