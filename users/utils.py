import jwt

from django.http  import JsonResponse

from users.models import User
from my_settings  import SECRET_KEY, ALGORITHMS

def login_decorator(func) :
    def wrapper(self, request, *args, **kwargs) :
        try :
            access_toekn = request.headers.get('Authorization', None)
            payload      = jwt.decode(access_toekn, SECRET_KEY, ALGORITHMS)
            user         = User.objects.get(account_email=payload['kakao_account']['email'])
            request.user = user
        
        except jwt.exceptions.DecodeError :
            return JsonResponse({'message' : 'json decode error'}, status=400)
        
        return func(self, request, *args, **kwargs)

    return wrapper