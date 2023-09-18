from .models import Article, ArticleCategory
from rest_framework import serializers

class ArticleSerializer(serializers.ModelSerializer):
    time_posted = serializers.SerializerMethodField(read_only=True)
    author = serializers.CharField(read_only=True)
    detail_url = serializers.HyperlinkedIdentityField(
        view_name="article-detail"
    )
    category = serializers.SlugRelatedField(
        queryset=ArticleCategory.objects.all(),
        slug_field='name',
    )
    email = serializers.CharField(source="author.email", read_only=True)

    class Meta:
        model = Article

        fields = [
            'author',
            'email',
            'detail_url',
            'title',
            'content',
            'image',
            'category',
            'time_posted',
        ]
        extra_kwargs = {
            'category': {'required': False}
        }

    def get_time_posted(self, obj):
        if not isinstance(obj, Article):
            return None
        return obj.posted_on
    
class ArticleDetailSerializer(ArticleSerializer):
    edit_url = serializers.HyperlinkedIdentityField(
        view_name="article-update"
    )
    delete_url = serializers.HyperlinkedIdentityField(
        view_name='article-delete'
    )
    class Meta:
        model = Article
        fields = [
            'author',
            'title',
            'content',
            'image',
            'time_posted',
            'category',
            'edit_url',
            'delete_url',
        ]


class ArticleCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleCategory
        fields = ['name',]
