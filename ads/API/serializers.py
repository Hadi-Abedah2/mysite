from ads.models import Ad, Comment
from rest_framework import serializers
from taggit.models import Tag
from django.contrib.auth import get_user_model 


class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ['name']



class CommentSerializer(serializers.ModelSerializer):
    ad = serializers.PrimaryKeyRelatedField(queryset=Ad.objects.all())
    owner =  serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Comment
        fields = ["id", "text", "ad", "owner"]


class CommentDetailSerializer(serializers.ModelSerializer):
    owner =  serializers.StringRelatedField(read_only=True)
    ad = serializers.PrimaryKeyRelatedField(queryset=Ad.objects.all())
   
    class Meta:
        model = Comment
        fields = "__all__"


class AdSerializer(serializers.ModelSerializer):
    owner =  serializers.StringRelatedField(read_only=True)
    comments_count = serializers.SerializerMethodField()
    
    #tags = TagSerializer(many=True) I will comment out this field since lists can not be added as HTML forms and my focus now is on Browsable API

    class Meta:
        model = Ad
        fields = ['id', 'title', 'text', 'price', 'owner', 'created_at', 'comments_count']
        read_only_fields = ('owner', 'created_at', 'comments_count')

    def get_comments_count(self, obj):
        return Comment.objects.filter(ad=obj).count()


class AdDetailSerializer(serializers.ModelSerializer):
    owner =  serializers.StringRelatedField(read_only=True)
    tags = TagSerializer(many=True)
    comments = CommentSerializer(many=True, read_only=True, source='comment_set')
    class Meta:
        model = Ad
        fields = "__all__"
        read_only_fields = ('owner', 'created_at')


