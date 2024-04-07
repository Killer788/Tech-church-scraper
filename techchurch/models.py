from django.db import models
from django.conf import settings


# Create your models here.
class BaseModel(models.Model):
    is_active = models.BooleanField(
        default=False,
        verbose_name='Is Active'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At'
    )

    class Meta:
        abstract = True

    def __str__(self):
        raise NotImplementedError('Please implement the __str__ method.')


class Author(BaseModel):
    full_name = models.CharField(max_length=250, verbose_name='Full Name')

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
        ordering = ('pk',)

    def __str__(self):
        return self.full_name


class Tag(BaseModel):
    title = models.CharField(max_length=250, verbose_name='Title')

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ('pk',)

    def __str__(self):
        return self.title


class Article(BaseModel):
    title = models.CharField(max_length=250, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    thumbnail = models.TextField(verbose_name='Thumbnail')
    text = models.TextField(verbose_name='Text')

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ('pk',)

    def __str__(self):
        return self.title


class Keyword(BaseModel):
    title = models.CharField(max_length=250, verbose_name='Title')

    class Meta:
        verbose_name = 'Keyword'
        verbose_name_plural = 'Keywords'
        ordering = ('pk',)

    def __str__(self):
        return self.title


class SearchByKeyword(BaseModel):
    keyword = models.ForeignKey(Keyword, related_name='searches', on_delete=models.PROTECT, verbose_name='Keyword')
    page_count = models.IntegerField(default=settings.DEFAULT_PAGE_COUNT, verbose_name='Page Count')

    class Meta:
        verbose_name = 'Search By Keyword'
        verbose_name_plural = 'Search By Keywords'
        ordering = ('pk',)

    def __str__(self):
        return self.keyword.title


class ArticleSearchByKeywordItem(BaseModel):
    search_by_keyword = models.ForeignKey(
        SearchByKeyword,
        related_name='article_search_by_keyword_items',
        on_delete=models.PROTECT,
        verbose_name='Search By Keyword'
    )
    article = models.ForeignKey(
        Article,
        related_name='article_search_by_keyword_items',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name='Article'
    )
    title = models.CharField(max_length=250, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    url = models.TextField(verbose_name='Url')
    is_scraped = models.BooleanField(default=False, verbose_name='Is Scraped')

    class Meta:
        verbose_name = 'Article Search By Keyword Item'
        verbose_name_plural = 'Article Search By Keyword Items'
        ordering = ('pk',)

    def __str__(self):
        return f'{self.title}({self.search_by_keyword.keyword.title})'


class ArticleTag(BaseModel):
    article = models.ForeignKey(
        Article,
        related_name='article_tags',
        on_delete=models.PROTECT,
        verbose_name='Article'
    )
    tag = models.ForeignKey(
        Tag,
        related_name='article_tags',
        on_delete=models.PROTECT,
        verbose_name='Tag'
    )

    class Meta:
        verbose_name = 'Article Tag'
        verbose_name_plural = 'Article Tags'
        ordering = ('pk',)

    def __str__(self):
        return f'{self.article.title}{self.tag.title}'


class ArticleAuthor(BaseModel):
    article = models.ForeignKey(
        Article,
        related_name='article_authors',
        on_delete=models.PROTECT,
        verbose_name='Article',
    )
    author = models.ForeignKey(
        Author,
        related_name='article_authors',
        on_delete=models.PROTECT,
        verbose_name='Author',
    )

    class Meta:
        verbose_name = 'Article Author'
        verbose_name_plural = 'Article Authors'
        ordering = ('pk',)

    def __str__(self):
        return f'{self.article.title}{self.author.full_name}'
