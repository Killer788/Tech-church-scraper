from .models import Author, Tag, ArticleAuthor, ArticleTag

import matplotlib.pyplot as plt


x_axis_ids = list()
articles = list()


def number_of_articles_per_authors_chart():
    authors = Author.objects.all()

    # Check for number of articles per authors and store author ids and number of articles in lists
    for author in authors:
        x_axis_ids.append(author.id)
        articles.append(len(ArticleAuthor.objects.filter(author=author).all()))

    plt.bar(x_axis_ids, articles, width=0.4)
    plt.xlabel('Authors')
    plt.ylabel('Number of Articles')
    plt.title('Number of Articles / Authors')

    plt.show()


def number_of_articles_per_tags_chart():
    tags = Tag.objects.all()

    # Check for number of articles per tags and store tag ids and number of articles in lists
    for tag in tags:
        x_axis_ids.append(tag.id)
        articles.append(len(ArticleTag.objects.filter(tag=tag).all()))

    plt.bar(x_axis_ids, articles, width=0.4)
    plt.xlabel('Tags')
    plt.ylabel('Number of Articles')
    plt.title('Number of Articles / Tags')

    plt.show()
