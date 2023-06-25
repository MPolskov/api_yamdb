from collections import OrderedDict

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title, Review, Comment

REVIEW_ERROR = 'Можно оставить только 1 отзыв на произведение.'
SCORE_ERROR = 'Выберите оценку от 1 до 10'
TITLE_ERROR = 'Ожидался {0} вместо {1}'
GENRE_NOTFOUND_ERROR = 'Жанр не найден'


class CustomSlugRelatedField(serializers.SlugRelatedField):
    def to_representation(self, obj):
        return obj.to_dict()


class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        lookup_field = 'slug'
        abstract = True


class CategorySerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Category


class GenreSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CustomSlugRelatedField(slug_field='slug',
                                      queryset=Category.objects.all())
    genre = GenreSerializer(required=False, many=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        ordering = ('pk', )

    def type_validate(self, target, obj):
        """Проверка соответствия типа объекта."""
        if type(obj) != target:
            raise ValidationError(
                {TITLE_ERROR.format(type(target), type(obj)): obj}
            )

    def to_internal_value(self, data):
        if 'genre' in data:
            data = data.copy()
            slugs = data.pop('genre')
            data['genre'] = []
        else:
            slugs = None
        ret = super().to_internal_value(data)
        if slugs:
            self.type_validate(list, slugs)
            errors = OrderedDict()
            genres = Genre.objects.filter(slug__in=slugs)
            genres_slug = genres.values_list('slug', flat=True)
            for slug in slugs:
                self.type_validate(str, slug)
                if slug not in genres_slug:
                    errors[slug] = GENRE_NOTFOUND_ERROR
            if errors:
                raise ValidationError(errors)
            ret['genre'] = list(genres)
        return ret

    def create(self, validated_data):
        genres = 'genre' in validated_data and validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        if genres:
            title.genre.set(genres)
        return title

    def update(self, instance, validated_data):
        for key in validated_data.keys():
            if key != 'genre':
                setattr(instance, key, validated_data.get(key))
            else:
                instance.genre.set(validated_data.get('genre'))
        instance.save()
        return instance


class TitleListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Title.objects.all(),
        required=False
    )
    author = SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError(SCORE_ERROR)
        return value

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        user = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if user.reviews.filter(title_id=title_id).exists():
            raise serializers.ValidationError(
                REVIEW_ERROR
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
