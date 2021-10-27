import requests

from django.http import JsonResponse

class KakaoAPI :
    def __init__(self, access_token, social_url) :
        self.access_token = access_token
        self.social_url   = social_url
    
    def get_user(self) :
        headers  = {'Authorization' : f'Bearer {self.access_token}'}
        response = requests.get(self.social_url, headers=headers, timeout=3)
      
        if not response.status_code == 200 :
            return JsonResponse({'message' : 'Invalid Token'}, status=401)
        
        return response