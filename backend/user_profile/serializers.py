from .models import ProfilePage, Hobbies
from rest_framework import serializers
from .validators import requires_age_of_18

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
