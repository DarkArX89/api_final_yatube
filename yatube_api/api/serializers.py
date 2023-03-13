from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from django.shortcuts import get_object_or_404

from posts.models import Comment, Post, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    posts = SlugRelatedField(
        many=True, read_only=True, slug_field='text'
    )

    class Meta:
        model = Group
        fields = ('__all__')


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(read_only=True, slug_field='username')
    following = SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, data):
        following_name = self.initial_data.get('following')
        if following_name is None:
            raise serializers.ValidationError(
                'В запросе некорректные данные!'
            )
        user = self.context['request'].user
        following = get_object_or_404(User, username=following_name)
        if user == following:
            raise serializers.ValidationError(
                'Нельзя подписываться на самого себя!'
            )
        unique = Follow.objects.filter(user=user, following=following)
        if len(unique) > 0:
            raise serializers.ValidationError(
                'Подписка пользователя на этого автора уже существует!'
            )
        return data
