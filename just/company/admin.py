from django.contrib import admin
from .models import (Company,
                     JobCategory,
                     JobPositionGroup,
                     JobPosition,
                     Article,
                     ArticleSection,
                     CommentArticle,
                     Hashtag,
                     Vacancy
                     )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'number_of_employees', 'admin', 'created_at', 'has_link')
    list_filter = ('number_of_employees', 'has_link')
    search_fields = ('name', 'admin__email', 'admin__phone')


class JobCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(JobCategory, JobCategoryAdmin)


class JobPositionAdmin(admin.ModelAdmin):
    filter_horizontal = ('categories', 'groups')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'name_ru', 'groups__name')


admin.site.register(JobPosition, JobPositionAdmin)

admin.site.register(JobPositionGroup)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'author_position', 'publication_date', 'views_count')
    search_fields = ('title', 'author__username', 'author_position')
    list_filter = ('publication_date',)
    ordering = ('-publication_date',)


admin.site.register(Article, ArticleAdmin)


class ArticleSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'article')
    search_fields = ('title', 'article__title')
    list_filter = ('article',)


admin.site.register(ArticleSection, ArticleSectionAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'date_time', 'parent_comment')
    search_fields = ('user__username', 'article__title', 'text')
    list_filter = ('date_time', 'article')


admin.site.register(CommentArticle, CommentAdmin)

admin.site.register(Hashtag)
admin.site.register(Vacancy)