from django.shortcuts import render

def bookmark_list(request):
    bookmarks = [
        {'title': 'Django 공식문서', 'url': 'https://docs.djangoproject.com/'},
        {'title': 'Python 공식문서', 'url': 'https://docs.python.org/'},
        {'title': 'GitHub', 'url': 'https://github.com/'},
    ]
    return render(request, 'bookmark/bookmark_list.html', {'bookmarks': bookmarks})
