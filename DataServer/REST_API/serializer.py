# serializers.py
from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class FileSerializer(serializers.Serializer):
    class Meta:
        model = Transaction
        fields = ['fileID', 'fileName', 'fileDate']
