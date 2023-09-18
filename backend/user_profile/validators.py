from rest_framework import serializers 
from django.utils import timezone


#implemented in models.py instead of serializers.py, in this case it was easier that way.
def requires_age_of_18(value):
    age = timezone.now().year - value.year
    if age < 18:
        raise serializers.ValidationError("Underage people are not allowed on this app.")