from .models import ProfilePage, Hobbies
from rest_framework import serializers
from .validators import requires_age_of_18
from django.contrib.auth.models import User
from . import validators



class CreatedDateFormat(serializers.Field):
    def to_representation(self, value):
        formatted_date = value.strftime(("%d/%m/%Y %H:%M:%S"))
        return formatted_date

class ProfilePageSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='author', read_only=True)
    hobbies = serializers.SlugRelatedField(
        queryset=Hobbies.objects.all(),
        slug_field="name",
        many=True,
    )
    created_at = CreatedDateFormat(label="Created at", read_only=True)
    profile_detail = serializers.HyperlinkedIdentityField(
        view_name="profile-detail"
    )
    class Meta:
        model = ProfilePage
        fields = [
            'user',
            'profile_detail',
            'profile_picture',
            'bio',
            'birthday',
            'workplace',
            'education',
            'marriage_status',
            'hobbies',
            'instagram',
            'facebook',
            'linkedin',
            'github',
            'twitter',
            'tiktok',
            'is_public',
            'created_at',

            
        ]


  

class ProfilePageDetailSerializer(ProfilePageSerializer):
    author_full_name = serializers.SerializerMethodField()
    edit_url = serializers.HyperlinkedIdentityField(view_name="profile-edit")
    delete_url = serializers.HyperlinkedIdentityField(view_name="profile-delete")
    hobbies = serializers.SlugRelatedField(
        queryset=Hobbies.objects.all(),
        slug_field="name",
        many=True,
    )
    class Meta:
        model = ProfilePage
        fields = [
            'author_full_name',
            'edit_url',
            'delete_url',
            'profile_picture',
            'bio',
            'birthday',
            'workplace',
            'education',
            'marriage_status',
            'hobbies',
            'instagram',
            'facebook',
            'linkedin',
            'github',
            'twitter',
            'tiktok',
            'is_public',
            'created_at',
        ]

    def get_author_full_name(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}" 


#registration
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validators.validated_password])
    username = serializers.CharField(validators=[validators.unique_username])
    email = serializers.EmailField(validators=[validators.email_validation,
                                               validators.unique_email])
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', ]


    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150, write_only=True)