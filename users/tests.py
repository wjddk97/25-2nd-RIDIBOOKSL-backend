from os import makedev
from unittest.mock import MagicMock, patch
from django.test   import Client, TestCase


class UserTest(TestCase):
    @patch('users.views.requests')
    def test_kakao_signin_new_user_success(self, mocked_requests) :
        client = Client()

        class MockedResponse :
            def json(self) :
                return {
                    'id': 1955676444, 
                    'connected_at': '2021-10-19T03:58:18Z', 
                    'properties': 
                        {
                            'nickname': '용현'
                        }, 
                    'kakao_account': 
                        {
                            'profile_nickname_needs_agreement': False, 
                            'profile_image_needs_agreement': False, 
                            'profile': 
                            {
                                'nickname': '용현', 
                                'thumbnail_image_url': 'http://k.kakaocdn.net/dn/dpk9l1/btqmGhA2lKL/Oz0wDuJn1YV2DIn92f6DVK/img_110x110.jpg', 
                                'profile_image_url': 'http://k.kakaocdn.net/dn/dpk9l1/btqmGhA2lKL/Oz0wDuJn1YV2DIn92f6DVK/img_640x640.jpg', 
                                'is_default_image': True
                            }, 
                            'has_email': True, 
                            'email_needs_agreement': False, 
                            'is_email_valid': True, 
                            'is_email_verified': True, 
                            'email': 'dydgus0421@gmail.com'
                        }
                    }
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'HTTP_Authorization' : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyfQ.Iao6z7UkLoTMl3v4duh_30iwBS4ZgMBJeMHjHe8aXCM"}
        response            = client.post('/account/sign-in/kakao/callback', **headers)

        self.assertEqual(response.status_code, 200)