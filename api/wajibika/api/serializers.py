from .models import County, Constituency, Ward, Leaders, Post, Video, Image, Text, PostContent, PostComment, Profile
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.contenttypes.models import ContentType


class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = '__all__'

class ConstituencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Constituency
        fields = '__all__'

class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = '__all__'

class LeadersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaders
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = '__all__'

class PostContentSerializer(serializers.ModelSerializer):
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = PostContent
        fields = ['id', 'post', 'content', 'object_id', 'content_object']

    def get_content_object(self, obj):
        if obj.content.model == 'video':
            return VideoSerializer(obj.content_object).data
        elif obj.content.model == 'image':
            return ImageSerializer(obj.content_object).data
        elif obj.content.model == 'text':
            return TextSerializer(obj.content_object).data
        return None

class PostSerializer(serializers.ModelSerializer):
    contents = serializers.ListSerializer(child=serializers.DictField(), write_only=True, required=False)
    post_contents = PostContentSerializer(source='postcontent_set', many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'created_at', 'updated_at', 'leader', 'contents', 'author', 'post_contents']
        extra_kwargs = {
            'leader': {'required': False},
            'author': {'required': False},
        }
    
    def create(self, validated_data):
        contents_data = validated_data.pop('contents', [])
        print(validated_data)
        post = Post.objects.create(**validated_data)

        for content_data in contents_data:
            content_type = content_data.get('type')
            if content_type == 'text':
                content_serializer = TextSerializer(data=content_data)
            elif content_type == 'image':
                content_serializer = ImageSerializer(data=content_data)
            elif content_type == 'video':
                content_serializer = VideoSerializer(data=content_data)
            else:
                continue
            content_serializer.is_valid(raise_exception=True)
            content = content_serializer.save()

            content_type_instance = ContentType.objects.get_for_model(content)

            PostContent.objects.create(
                post=post,
                content=content_type_instance,
                object_id=content.id
            )

        return post
    
    def update(self, instance, validated_data):
        contents_data = validated_data.pop('contents', None)
        instance = super().update(instance, validated_data)

        if contents_data is not None:
            for content_data in contents_data:
                content_type = content_data.get('type')
                content_id = content_data.get('id', None)
                if content_type == 'text':
                    content_model = Text
                    content_serializer_class = TextSerializer
                elif content_type == 'image':
                    content_model = Image
                    content_serializer_class = ImageSerializer
                elif content_type == 'video':
                    content_model = Video
                    content_serializer_class = VideoSerializer
                else:
                    continue

                if content_id:
                    try:
                        content_instance = content_model.objects.get(id=content_id)
                        content_serializer = content_serializer_class(content_instance, data=content_data, partial=True)
                    except content_model.DoesNotExist:
                        content_serializer = content_serializer_class(data=content_data)
                else:
                    content_serializer = content_serializer_class(data=content_data)

                content_serializer.is_valid(raise_exception=True)
                content = content_serializer.save()

                content_type_instance = ContentType.objects.get_for_model(content)

                # Check if the content already exists
                PostContent.objects.update_or_create(
                    post=instance,
                    content=content_type_instance,
                    object_id=content.id,
                    defaults={'content': content_type_instance, 'object_id': content.id}
                )
            return instance
    
    def validate(self, data):
        contents = data.get('contents', None)
        if contents is None:
            raise serializers.ValidationError('Content is required')
        return data


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'post', 'author']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
        

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['user']

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    