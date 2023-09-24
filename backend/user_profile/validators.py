from rest_framework import serializers 
from django.utils import timezone
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

#implemented in models.py instead of serializers.py, in this case it was easier that way.
def requires_age_of_18(value):
    age = timezone.now().year - value.year
    if age < 18:
        raise serializers.ValidationError("Underage people are not allowed on this app.")
    

def validated_password(value):
    try:
        password_validation.validate_password(value)
    except ValidationError as e:
        raise serializers.ValidationError(e.messages)
    return value

unique_username = UniqueValidator(queryset=User.objects.all(), lookup="iexact")


def email_validation(value):
    if not ".com" in value:
        raise serializers.ValidationError("Invalid e-mail address.")
    return value

unique_email = UniqueValidator(queryset=User.objects.all(), lookup="iexact", 
                               message="This e-mail is already in use.")

