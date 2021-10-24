import json
import jwt
from unittest.mock import MagicMock, patch
from django.test   import Client, TestCase

from users.models        import User
from ridibooksl.settings import (
    ALGORITHMS,
    SECRET_KEY
)

class UserTest(TestCase):

    def setUp(self) :
        pass
    
    def tearDown(self) :
        User.objects.all().delete()

    @patch('users.views.requests')
    def test_kakao_signin_new_user_success(self, mocked_requests) :
        client = Client()
        
        class MockedResponse :
            def json(self) :
                return {
                    'id': 195564, 
                    'properties': 
                        {
                            'nickname': 'k용현'
                        }, 
                    'kakao_account': 
                        {
                            'email': 'dydgus04211111@gmail.com',
                            'profile' : {
                                "profile_image_url" : "image url"
                            }
                        }
                    }
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'HTTP_Authorization' : "fake token"}
        response            = client.post('/account/sign-in/kakao', **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'new_token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.loTjeBWZ9SeXV-BcIxqOtX37AN30ROvsZl0_udeeRJU', 'user_id':1})

    @patch('users.views.requests')
    def test_kakao_signin_key_error(self, mocked_requests) :
        client = Client()

        class MockedResponse :
            def json(self) :
                return {
                    'id': 1955676444, 
                    'properties': 
                        {
                            'nckname': '용현'
                        }, 
                    'kakao_account': 
                        {
                            'email': 'dydgus04211@gmail.com',
                            'profile' : {
                                "profile_image_url" : "image url"
                            }
                        }
                    }
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'HTTP_Authorization' : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyfQ.Iao6z7UkLoTMl3v4duh_30iwBS4ZgMBJeMHjHe8aXCM"}
        response            = client.post('/account/sign-in/kakao', **headers)

        self.assertEqual(response.status_code, 400) 
        self.assertEqual(response.json(), {'message':'KEY ERROR'})

    @patch('users.views.requests')
    def test_kakao_signin_token_error(self, mocked_requests) :
        client = Client()

        class MockedResponse :
            def json(self) :
                return {
                    'id': 1955676444, 
                    'properties': 
                        {
                            'nickname': '용현'
                        }, 
                    'kakao_account': 
                        {
                            'email': 'dydgus04211@gmail.com',
                            'profile' : {
                                "profile_image_url" : "image url"
                            }
                        }
                    }
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'HTTP_Authorizations' : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyfQ.Iao6z7UkLoTMl3v4duh_30iwBS4ZgMBJeMHjHe8aXCMㅇㅇㅇㅇㅇ33"}
        response            = client.post('/account/sign-in/kakao', **headers)

        self.assertEqual(response.status_code, 401) 
        self.assertEqual(response.json(), {'message':'ACCESS_TOKEN_REQUIRED'})