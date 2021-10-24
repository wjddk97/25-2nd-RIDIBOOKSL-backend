import requests
import jwt

from django.views import View
from django.http  import JsonResponse

from users.models        import User
from ridibooksl.settings import (
    SECRET_KEY,
    ALGORITHMS
)

class KakaoLoginView(View):
    def post(self, request):
        try :
            access_token = request.headers.get("Authorization", None)

            if not access_token:
                return JsonResponse({'message' : 'ACCESS_TOKEN_REQUIRED'}, status=401)

            headers      = {'Authorization' : f"Bearer {access_token}"}
            URL          = "https://kapi.kakao.com/v2/user/me"
            response     = requests.get(URL, headers=headers)
            user_data    = response.json()

            if not user_data:
                return JsonResponse({'message' : 'INVALID_TOKEN'}, status=401)

            login_user, created  = User.objects.get_or_create(
                profile_nickname = user_data['properties']['nickname'],
                account_email    = user_data['kakao_account']['email'],
                profile_image    = user_data['kakao_account']['profile'].get('profile_image_url', None)
            )

            new_token = jwt.encode({'user_id' : login_user.id}, SECRET_KEY, ALGORITHMS)

            return JsonResponse({'new_token' : new_token, 'user_id': login_user.id}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY ERROR'}, status = 400)

        except User.DoesNotExist :
            return JsonResponse({'message' : "OBJECT 'USER' NOT EXIST"}, status=400)

        except AttributeError :
            return JsonResponse({'message' : 'Attribure ERROR'}, status=400) 