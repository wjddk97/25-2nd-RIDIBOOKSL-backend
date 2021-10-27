import jwt

from json.decoder import JSONDecodeError
from django.views import View
from django.http  import JsonResponse

from users.models        import User
from users.kakao_users  import KakaoAPI
from ridibooksl.settings import (
    SECRET_KEY,
    ALGORITHMS
)

class KakaoLoginView(View):
    def post(self, request):
        try :
            access_token = request.headers.get("Authorization", None)
            kakao_user   = KakaoAPI(access_token, "https://kapi.kakao.com/v2/user/me")
            response     = kakao_user.got_user()

            if not response.status_code == 200 :
                return JsonResponse({'message' : 'Invalid Token'}, status=401)
            
            user_data = response.json()

        except KeyError:
            return JsonResponse({'message' : 'KEY ERROR'}, status=400)   
            
        except JSONDecodeError :
            return JsonResponse({'message' : 'JSON DECODE ERROR'}, status=400)

        login_user , state = User.objects.get_or_create(
            profile_nickname = user_data['properties']['nickname'],
            account_email    = user_data['kakao_account']['email'],
            profile_image    = user_data['kakao_account']['profile'].get('profile_image_url', None)
        )

        new_token = jwt.encode({'user_id' : login_user.id}, SECRET_KEY, ALGORITHMS)

        return JsonResponse({'new_token' : new_token, 'user_id': login_user.id}, status = 200)