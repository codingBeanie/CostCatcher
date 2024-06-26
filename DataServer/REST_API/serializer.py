# serializers.py
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    color = serializers.SerializerMethodField()
    categoryName = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = '__all__'

    def get_color(self, obj):
        if obj.category:
            color = obj.category.color
            return color

    def get_categoryName(self, obj):
        if obj.category:
            categoryName = obj.category.name
            return categoryName


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'


class FileSerializer(serializers.Serializer):
    class Meta:
        model = Transaction
        fields = ['fileName', 'fileDate']


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
    conflict = serializers.SerializerMethodField()
    numberOfAssignments = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = '__all__'

    def get_color(self, obj):
        if obj.category:
            color = obj.category.color
            return color

    def get_categoryName(self, obj):
        if obj.category:
            categoryName = obj.category.name
            return categoryName

    def get_conflict(self, obj):
        if obj.category:
            transactions = Transaction.objects.filter(assignments=obj)
            if transactions:
                for transaction in transactions:
                    amountRules = len(transaction.assignments.all())
                    if amountRules > 1:
                        return True
            else:
                return False
        return False

    def get_numberOfAssignments(self, obj):
        transactions = Transaction.objects.filter(assignments=obj)
        if transactions:
            return len(transactions)
        else:
            return 0
