from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from user.views import authenticate
from user.models import User
import simplejson
import datetime
from .models import Post, Content
import math


@authenticate
def pub(request: HttpRequest):
    post = Post()
    content = Content()
    try:
        payload = simplejson.loads(request.body)
        post.title = payload['title']
        # post.author = User(id=request.user.id)
        post.author = request.user
        post.postdate = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))

        post.save()

        content.content = payload['content']
        content.post = post

        content.save()

        return JsonResponse({"post_id": post.id})
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()


def get(request: HttpRequest, id):
    try:
        id = int(id)
        post = Post.objects.get(pk=id)
        print(1, post)
        if post:
            return JsonResponse({
                'post': {
                    'post_id': post.id,
                    'title': post.title,
                    'author': post.author.name,
                    'author_id': post.author_id,
                    'postdate': post.postdate.timestamp(),
                    'content': post.content.content
                }
            })
    except Exception as e:
        print(e)
        return HttpResponseNotFound()


def validate(d: dict, name: str, type_func, default, validate_func):
    try:
        result = type_func(d.get(name, default))
        result = validate_func(result, default)
    except:
        result = default
    return result


def getall(request: HttpRequest):
    page = validate(request.GET, 'page', int, 2, lambda x, y: x if x > 0 else 2)
    size = validate(request.GET, 'size', int, 20, lambda x, y: x if x > 0 and x<20 else y)

    print(request.GET)
    try:
        start = (page - 1) * size
        posts = Post.objects.order_by('-id')
        print(1, posts.query)
        count = posts.count()

        posts = posts[start:start + size]
        print(2, posts.query)

        return JsonResponse({
            'posts': [
                {
                    'post_id': post.id,
                    'title': post.title
                } for post in posts
            ], 'pagination': {
                'page': page,  # 当前页
                'size': size,  # 每页行数
                'count': count,  # 总行数
                'pages': math.ceil(count / size)  # 总页数
            }
        })
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()
