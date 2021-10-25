from unittest.mock import MagicMock, patch
from django.test   import Client, TestCase

from users.models  import User

class UserLoignTest(TestCase):
    def setUp(self) :
        pass
    
    def tearDown(self) :
        User.objects.all().delete()

    @patch('users.kakao_users.requests')
    def test_success_kakao_login_create_new_user(self, mocked_requests) :
        client = Client()
        
        class MockedResponse :
            def __init__ (self) :
                self.status_code = 200

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
        headers             = {'HTTP_Authorization' : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.loTjeBWZ9SeXV-BcIxqOtX37AN30ROvsZl0_udeeRJUdddd"}
        response            = client.post('/account/sign-in/kakao', **headers)

        self.assertEqual(response.status_code, 200)

    @patch('users.kakao_users.requests')
    def test_success_kakao_login_invalid_token_error(self, mocked_requests) :
        client = Client()

        class MockedResponse :
            def __init__ (self) :
                self.status_code = 401

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
        self.assertEqual(response.json(), {'message':'Invalid Token'})