import jwt

from django.http  import JsonResponse

from users.models        import User
from ridibooksl.settings import (
    ALGORITHMS,
    SECRET_KEY
)

def login_decorator(func) :
    def wrapper(self, request, *args, **kwargs) :
        try :
            access_token = request.headers.get('Authorization', None)
            payload      = jwt.decode(access_token, SECRET_KEY, ALGORITHMS)
            user         = User.objects.get(id=payload['user_id'])
            request.user = user

            return func(self, request, *args, **kwargs)
        
        except jwt.exceptions.DecodeError :
            return JsonResponse({'message' : 'DECODE ERROR'}, status=401)
    
    return wrapper