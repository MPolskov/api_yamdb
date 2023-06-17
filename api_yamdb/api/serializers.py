from collections import OrderedDict
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Genre, Title


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

    def to_internal_value(self, data):
        if 'genre' in data:
            data = data.copy()
            genres = data.pop('genre')
        else:
            genres = None
        ret = super().to_internal_value(data)
        if genres:
            if type(genres) != list:
                raise ValidationError(
                    {f'Ожидался {type(list)} вместо {type(genres)}': genres}
                )
            result = []
            errors = OrderedDict()
            for slug in genres:
                try:
                    genre = Genre.objects.get(slug=slug)
                except Exception as error:
                    errors[slug] = error
                else:
                    result.append(genre)
            if errors:
                raise ValidationError(errors)
            ret['genre'] = result
        return ret

    def create(self, validated_data):
        if 'genre' not in validated_data:
            title = Title.objects.create(**validated_data)
            return title
        else:
            genres = validated_data.pop('genre')
            title = Title.objects.create(**validated_data)
            for genre in genres:
                title.genre.add(genre)
            return title


class TitleListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
