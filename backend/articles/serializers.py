from .models import Article, ArticleCategory, CommentSection
from rest_framework import serializers
from . import validators
from django.contrib.auth.models import User


class AuthorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

class ChildCommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(queryset=CommentSection.objects.all(), source='parent_comment.id')
    article = serializers.CharField(source='article.title', read_only=True)
    class Meta:
        model = CommentSection
        fields = ['author','article', 'content', 'id', 'parent_id']

    def get_author(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}"

    def create(self, validated_data):
        parent_id = validated_data.pop('parent_id')
        parent_comment = CommentSection.objects.get(id=parent_id)
        validated_data['parent_comment'] = parent_comment
        validated_data['article'] = parent_comment.article

        return CommentSection.objects.create(**validated_data)

class CommentCreateSerializer(serializers.ModelSerializer):
        article = serializers.CharField(read_only=True, source="article.title")
        class Meta:
            model = CommentSection
            fields = [
                'article',            
                'content',
                'parent_comment',
                ]
            
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            return self.fields['parent_comment'].validators.append(validators.validate_parent_comment)
        

class CommentUpdateSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    article = serializers.CharField(read_only=True)
    parent_comment = serializers.CharField(read_only=True)
    class Meta:
        model = CommentSection
        fields = ['author','article','content','parent_comment']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)
    time_posted = serializers.SerializerMethodField(read_only=True)
    # replies = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()
    parent_comment = serializers.SlugRelatedField(
        queryset=CommentSection.objects.all(),
        slug_field="content"
    )
    article = serializers.CharField(source="article.title")
    edit_url = serializers.HyperlinkedIdentityField(
        view_name="comment-update"
    )
    delete_url = serializers.HyperlinkedIdentityField(
        view_name="comment-delete"
    )
    class Meta:
        model = CommentSection
        fields = [
            'pk',
            'author',
            'article',
            'content',
            'time_posted',
            'parent_comment',
            'reply_count',
            'edit_url',
            'delete_url'
        ]

    def get_time_posted(self, obj):
        if not isinstance(obj, CommentSection):
            return None
        return obj.created_at

    def get_author(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}"

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return None
    
    def get_replies(self, obj):
        if obj.is_parent:
            return ChildCommentSerializer(obj.children(), many=True).data
        return None

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
    comments = serializers.SerializerMethodField()

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
            'comments',
        ]
        extra_kwargs = {
            'category': {'required': False}
        }

    def get_time_posted(self, obj):
        if not isinstance(obj, Article):
            return None
        return obj.posted_on
    
    def get_comments(self, obj):
        comments = CommentSection.objects.filter(article=obj)
        comment_data = [{'author': comment.author.first_name and comment.author.last_name, 'content': comment.content} for comment in comments]
        return comment_data
    

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
