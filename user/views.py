from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse, HttpRequest, HttpResponseBadRequest, HttpResponse
import simplejson
from .models import User
from django.conf import settings
import jwt
import bcrypt
import datetime

AUTH_EXPILE = 8 * 60 * 60  # 8小时过期


def gen_token(user_id):
    """生成token"""
    # 增加时间戳，判断是否重发token或重新登录
    return jwt.encode({
        'user_id': user_id,
        'exp': int(datetime.datetime.now().timestamp()) + AUTH_EXPILE
    }, settings.SECRET_KEY, 'HS256').decode()


def authenticate(view):
    def wrapper(request: HttpRequest):
        payload = request.META.get('HTTP_JWT')
        if not payload:  # 没拿到，认证失败
            return HttpResponse(status=401)
        try:  # 拿到了，进行解码
            payload = jwt.decode(payload, settings.SECRET_KEY, algorithms=['HS256'])
        # except Exception as e:
        #     print(e, '过期啦')
        #     return HttpResponse(status=401)

        # # 验证过期时间
        # current = datetime.datetime.now().timestamp()
        # if (current - payload.get('timestamp', 0)) > AUTH_EXPILE:
        #     return HttpResponse(status=401)
        # try:
            user_id = payload.get('user_id', -1)
            user = User.objects.filter(pk=user_id).get()
            request.user = user  # 成功则注入user
            print(request.user, '验证通过')
        except Exception as e:
            print(e)
            return HttpResponse(status=401)

        ret = view(request)
        return ret

    return wrapper


def reg(request: HttpRequest):
    try:
        payload = simplejson.loads(request.body)  # dict

        email = payload['email']
        query = User.objects.filter(email=email)
        if query.first():
            return HttpResponseBadRequest('用户名已存在')

        name = payload['name']
        password = bcrypt.hashpw(payload['password'].encode(), bcrypt.gensalt())

        user = User()
        user.email = email
        user.name = name
        user.password = password

        try:
            user.save()
            return JsonResponse({"user_id": user.id, "token": gen_token(user.id)})
        except Exception:
            raise

    except Exception as e:
        return HttpResponseBadRequest('参数错误')


def login(request: HttpRequest):
    payload = simplejson.loads(request.body)
    try:
        email = payload['email']
        user = User.objects.filter(email=email).get()

        if bcrypt.checkpw(payload['password'].encode(), user.password.encode()):
            token = gen_token(user.id)  # 验证通过
            res = JsonResponse({
                'user': {
                    'user_id': user.id,
                    'name': user.name,
                    'email': user.email,
                }, 'token': token
            })
            res.set_cookie('Jwt', token)  # set cookie
            return res
        else:
            return HttpResponseBadRequest()
    except Exception as e:
        print(e)
        return HttpResponseBadRequest('用户名或密码错误')


def show(request):
    u1 = User.objects.filter(pk__lt=7).first()  # id<7
    print(1, u1)
    u2 = User.objects.filter(pk__lte=7)  # id=<7
    print(2, u2)
    u3 = User.objects.filter(pk__gt=7)  # id>8
    print(3, u3)
    print(4, request.GET)
    print(5, request.POST)
    print(6, request.body)
    res = JsonResponse({'test':'ok'})
    res['Access-Control-Allow-Origin'] = '*'

    return res


@authenticate  # 自由应用在需要验证的view函数上
def test(request: HttpRequest):
    return HttpResponse('test')

# def getall(request: HttpRequest):
#     try:
#         name_id = int(request.GET.get('id'))
#         size = int(request.GET.get('size'))
#         start = (name_id - 1)*size
#         names = User.objects.order_by('-pk')
#         counrt = names.count()
#
#         names = names[]
