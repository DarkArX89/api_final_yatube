from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Post, Group, Follow


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
        if user.username == following_name:
            raise serializers.ValidationError(
                'Нельзя подписываться на самого себя!'
            )
        if Follow.objects.filter(
            user=user, following__username=following_name
        ).exists():
            raise serializers.ValidationError(
                'Подписка пользователя на этого автора уже существует!'
            )
        return data
