from django.contrib import admin

from .models import Category, Genre, Title, GenreTitle, Review, Comment


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'year', 'name', 'description', 'get_genres', 'category')
    search_fields = ('name',)
    list_filter = ('year',)

    @admin.display(description='Жанры')
    def get_genres(self, obj):
        return [g.name for g in obj.genre.all()]


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(GenreTitle)
admin.site.register(Review)
admin.site.register(Comment)
