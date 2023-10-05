from .models import CommentSection
from rest_framework import serializers

def validate_parent_comment(value):
    if value and value.parent_comment:
        raise serializers.ValidationError("Replies can't have replies.")
    return value