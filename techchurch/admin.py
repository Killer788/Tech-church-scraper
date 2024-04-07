from django.contrib import admin
from django.contrib.admin import register

from import_export.admin import ImportExportModelAdmin
from import_export import resources

from .models import (Author, Tag, Article, Keyword, SearchByKeyword, ArticleSearchByKeywordItem, ArticleTag,
                     ArticleAuthor)


class KeywordResource(resources.ModelResource):
    class Meta:
        model = Keyword
        exclude = ('is_active',)
        export_order = ('id', 'title', 'created_at', 'updated_at')


class ArticleResource(resources.ModelResource):
    class Meta:
        model = Article
        exclude = ('is_active',)
        export_order = ('id', 'title', 'description', 'thumbnail', 'text', 'created_at', 'updated_at',)


class TagResource(resources.ModelResource):
    class Meta:
        model = Tag
        exclude = ('is_active',)
        export_order = ('id', 'title', 'created_at', 'updated_at',)


class AuthorResource(resources.ModelResource):
    class Meta:
        model = Author
        exclude = ('is_active',)
        export_order = ('id', 'full_name', 'created_at', 'updated_at',)


class ArticleAuthorResource(resources.ModelResource):
    class Meta:
        model = ArticleAuthor
        exclude = ('is_active',)
        export_order = ('id', 'article', 'author', 'created_at', 'updated_at',)


class ArticleTagResource(resources.ModelResource):
    class Meta:
        model = ArticleTag
        exclude = ('is_active',)
        export_order = ('id', 'article', 'tag', 'created_at', 'updated_at',)


class ArticleSearchByKeywordItemResource(resources.ModelResource):
    class Meta:
        model = ArticleSearchByKeywordItem
        exclude = ('is_active', 'is_scraped')
        export_order = (
            'id',
            'search_by_keyword',
            'article',
            'title',
            'description',
            'url',
            'created_at',
            'updated_at',
        )


class SearchByKeywordResource(resources.ModelResource):
    class Meta:
        model = SearchByKeyword
        exclude = ('is_active',)
        export_order = ('id', 'keyword', 'page_count', 'created_at', 'updated_at',)


# Register your models here.
@admin.action(description="Activate the selected rows")
def activate_rows(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="Deactivate the selected rows")
def deactivate_rows(modeladmin, request, queryset):
    queryset.update(is_active=False)


class BaseAdmin(admin.ModelAdmin):
    actions = ('activate_rows', 'deactivate_rows')


@register(Author)
class AuthorAdmin(ImportExportModelAdmin, BaseAdmin):
    list_display = ('id', 'full_name', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('full_name',)
    list_filter = ('is_active', 'created_at', 'updated_at')
    list_editable = ('is_active',)
    search_fields = ('full_name',)
    resource_classes = (AuthorResource,)


@register(Tag)
class TagAdmin(ImportExportModelAdmin, BaseAdmin):
    list_display = ('id', 'title', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('title',)
    list_filter = ('is_active', 'created_at', 'updated_at')
    list_editable = ('is_active',)
    search_fields = ('title',)
    resource_classes = (TagResource,)


@register(Article)
class ArticleAdmin(ImportExportModelAdmin, BaseAdmin):
    list_display = ('id', 'title', 'description', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('title',)
    list_filter = ('is_active', 'created_at', 'updated_at')
    list_editable = ('is_active',)
    search_fields = ('title', 'description')
    resource_classes = (ArticleResource,)


@register(Keyword)
class KeywordAdmin(ImportExportModelAdmin, BaseAdmin):
    list_display = ('id', 'title', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('title',)
    list_filter = ('is_active', 'created_at', 'updated_at')
    list_editable = ('is_active',)
    search_fields = ('title',)
    resource_classes = (KeywordResource,)


@register(SearchByKeyword)
class SearchByKeywordAdmin(ImportExportModelAdmin, BaseAdmin):
    list_display = ('id', 'keyword', 'page_count', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('keyword',)
    list_filter = ('is_active', 'created_at', 'updated_at', 'keyword')
    list_editable = ('is_active',)
    search_fields = ('keyword__title',)
    resource_classes = (SearchByKeywordResource,)


@register(ArticleSearchByKeywordItem)
class ArticleSearchByKeywordItemAdmin(ImportExportModelAdmin, BaseAdmin):
    list_display = ('id', 'title', 'description', 'article', 'search_by_keyword', 'url', 'is_active', 'is_scraped',
                    'created_at', 'updated_at')
    list_display_links = ('title', 'search_by_keyword')
    list_filter = ('is_active', 'is_scraped', 'created_at', 'updated_at', 'search_by_keyword',)
    list_editable = ('is_active',)
    search_fields = ('title', 'description', 'article__title', 'search_by_keyword__keyword__title')
    resource_classes = (ArticleSearchByKeywordItemResource,)


@register(ArticleTag)
class ArticleTagAdmin(ImportExportModelAdmin, BaseAdmin):
    list_display = ('id', 'article', 'tag', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('article',)
    list_filter = ('is_active', 'created_at', 'updated_at', 'article', 'tag')
    list_editable = ('is_active',)
    search_fields = ('article__title', 'tag__title')
    resource_classes = (ArticleTagResource,)


@register(ArticleAuthor)
class ArticleAuthorAdmin(ImportExportModelAdmin, BaseAdmin):
    list_display = ('id', 'article', 'author', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('article',)
    list_filter = ('is_active', 'created_at', 'updated_at', 'article', 'author')
    list_editable = ('is_active',)
    search_fields = ('article__title', 'author__full_name')
    resource_classes = (ArticleAuthorResource,)
