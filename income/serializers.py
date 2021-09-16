from rest_framework import serializers

from .models import Income

class IcomeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Income
        fields = ['id','date', 'desciption', 'amount', 'source']