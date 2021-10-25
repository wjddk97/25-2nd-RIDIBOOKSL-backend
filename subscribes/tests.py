import json

from django.test       import TestCase, Client

from products.models   import ( 
    Author,
    Book,
    Category,
    Menu,
    Publisher,
    Thumbnail
)
from subscribes.models import Subscribe
from users.models      import User

class SubscribePostViewTest(TestCase) :
    def setUp(self) :
        user   = User.objects.create(account_email="test1234@gmail.com", profile_nickname='test', profile_image='url')
        author = Author.objects.create(id=1, name='test', birthdate='1994-09-26', country='korea')
        Author.objects.create(name='created_author', birthdate='1994-09-26', country='korea')
        Subscribe.objects.create(author_id=author.id, user_id=user.id)
        
    def tearDown(self) :
        User.objects.all().delete()
        Author.objects.all().delete()
        Subscribe.objects.all().delete()

    def test_success_subscribe_get_or_create(self) :
        client = Client()

        headers = {'HTTP_Authorization' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.loTjeBWZ9SeXV-BcIxqOtX37AN30ROvsZl0_udeeRJU'}

        got_subscribe_info = {
            'user_id'   : User.objects.get(account_email="test1234@gmail.com").id ,
            'author_id' : Author.objects.get(name='test').id
        }

        created_subscribe_info = {
            'user_id'   : User.objects.get(account_email="test1234@gmail.com").id ,
            'author_id' : Author.objects.get(name='created_author').id
        }

        got_response     = client.post('/subscribe?author_id=1', json.dumps(created_subscribe_info), content_type='application/json', **headers)
        created_response = client.post('/subscribe?author_id=1', json.dumps(got_subscribe_info), content_type='application/json', **headers)

        self.assertEqual(got_response.status_code, 201)
        self.assertEqual(created_response.status_code, 201)

        self.assertEqual(got_response.json(),{
            'message' : 'delete success'
        })
        self.assertEqual(created_response.json(),{
            'message' : 'create success'
        })

    def test_success_subscribe_signature_verification_failed_by_wrong_token(self) :
        client = Client()

        headers = {'HTTP_Authorization' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.loTjeBWZ9SeXV-BcIxqOtX37AN30ROvsZl0_udeeRJUdd'}

        subscribe_info = {
            'user_id'   : User.objects.get(account_email="test1234@gmail.com").id,
            'author_id' : Author.objects.create(name='new_data', birthdate='1994-09-26', country='korea').id
        }

        response = client.post('/subscribe', json.dumps(subscribe_info), content_type='application/json', **headers)
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),{
            'message' : 'DECODE ERROR'
        })        
    
    def test_success_subscribe_raise_invalid_token_type_by_wrong_token(self) :
        client = Client()

        headers = {'HTTP_Authorizations' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.loTjeBWZ9SeXV-BcIxqOtX37AN30ROvsZl0_udeeRJU'}

        subscribe_info = {
            'user_id'   : User.objects.get(account_email="test1234@gmail.com").id,
            'author_id' : Author.objects.create(name='new_data', birthdate='1994-09-26', country='korea').id
        }

        response = client.post('/subscribe', json.dumps(subscribe_info), content_type='application/json', **headers)
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),{
            'message' : 'DECODE ERROR'
        })

class SearchTest(TestCase) :
    def setUp(self) :
        menu_id        = Menu.objects.create(name='test').id
        category_id    = Category.objects.create(menu_id=menu_id, name='test').id

        thumbnail_list = [

        Thumbnail(
            id        = 1,
            image_url = "url_1"
        ),
        Thumbnail(
            id        = 2,
            image_url = "url_2"
        ),
        Thumbnail(
            id        = 3,
            image_url = "url_3"
        ),
        Thumbnail(
            id        = 4,
            image_url = "url_4"
        ),
        Thumbnail(
            id        = 5,
            image_url = "url_5"
        ),
        Thumbnail(
            id        = 6,
            image_url = "url_6"
        ),
        Thumbnail(
            id        = 7,
            image_url = "url_7"
        ),
        Thumbnail(
            id        = 8,
            image_url = "url_8"
        ),
        Thumbnail(
            id        = 9,
            image_url = "url_9"
        ),
        Thumbnail(
            id        = 10,
            image_url = "url_10"
        )
        ]

        Thumbnail.objects.bulk_create(thumbnail_list)

        publisher_id   = Publisher.objects.create(name='test').id

        book_list = [
            
        Book(
            id           = 1,
            menu_id      = menu_id,
            category_id  = category_id,
            thumbnail_id = Thumbnail.objects.get(id=1).id,
            publisher_id = publisher_id,
            price        = 5000,
            main_name    = 'test1'
        ),
        Book(
            id           = 2,
            menu_id      = menu_id,
            category_id  = category_id,
            thumbnail_id = Thumbnail.objects.get(id=2).id,
            publisher_id = publisher_id,
            price        = 5000,
            main_name    = 'test2'
        ),
        Book(
            id           = 3,
            menu_id      = menu_id,
            category_id  = category_id,
            thumbnail_id = Thumbnail.objects.get(id=3).id,
            publisher_id = publisher_id,
            price        = 5000,
            main_name    = 'test3'
        ),
        Book(
            id           = 4,
            menu_id      = menu_id,
            category_id  = category_id,
            thumbnail_id = Thumbnail.objects.get(id=4).id,
            publisher_id = publisher_id,
            price        = 5000,
            main_name    = 'test4'
        ),
        Book(
            id           = 5,
            menu_id      = menu_id,
            category_id  = category_id,
            thumbnail_id = Thumbnail.objects.get(id=5).id,
            publisher_id = publisher_id,
            price        = 5000,
            main_name    = 'test5'
        ),
        Book(
            id           = 6,
            menu_id      = menu_id,
            category_id  = category_id,
            thumbnail_id = Thumbnail.objects.get(id=6).id,
            publisher_id = publisher_id,
            price        = 5000,
            main_name    = 'test6'
        ),
        Book(
            id           = 7,
            menu_id      = menu_id,
            category_id  = category_id,
            thumbnail_id = Thumbnail.objects.get(id=7).id,
            publisher_id = publisher_id,
            price        = 5000,
            main_name    = 'test7'
        ),
        Book(
            id           = 8,
            menu_id      = menu_id,
            category_id  = category_id,
            thumbnail_id = Thumbnail.objects.get(id=8).id,
            publisher_id = publisher_id,
            price        = 5000,
            main_name    = 'test8'
        ),
        Book(
            id           = 9,
            menu_id      = menu_id,
            category_id  = category_id,
            thumbnail_id = Thumbnail.objects.get(id=9).id,
            publisher_id = publisher_id,
            price        = 5000,
            main_name    = 'test9'
        ),
        Book(
            id           = 10,
            menu_id      = menu_id,
            category_id  = category_id,
            thumbnail_id = Thumbnail.objects.get(id=10).id,
            publisher_id = publisher_id,
            price        = 5000,
            main_name    = 'test10'
        )
        ]

        Book.objects.bulk_create(book_list)

        author_list = [
        Author(
            id        = 1,
            name      = 'test1',
            birthdate = '1994-09-26', 
            country   = 'korea'
        ),
        Author(
            id        = 2,
            name      = 'test2',
            birthdate = '1994-09-26', 
            country   = 'korea'
        ),
        Author(
            id        = 3,
            name      = 'test3',
            birthdate = '1994-09-26', 
            country   = 'korea'
        ),
        Author(
            id        = 4,
            name      = 'test4',
            birthdate = '1994-09-26', 
            country   = 'korea'
        ),
        Author(
            id        = 5,
            name      = 'test5',
            birthdate = '1994-09-26', 
            country   = 'korea'
        ),
        Author(
            id        = 6,
            name      = 'test6',
            birthdate = '1994-09-26', 
            country   = 'korea'
        ),
        Author(
            id        = 7,
            name      = 'test7',
            birthdate = '1994-09-26', 
            country   = 'korea'
        ),
        Author(
            id        = 8,
            name      = 'test8',
            birthdate = '1994-09-26', 
            country   = 'korea'
        ),
        Author(
            id        = 9,
            name      = 'test9',
            birthdate = '1994-09-26', 
            country   = 'korea'
        ),
        Author(
            id        = 10,
            name      = 'test10',
            birthdate = '1994-09-26', 
            country   = 'korea'
        )
        ]

        Author.objects.bulk_create(author_list)

    def tearDown(self) :
        Menu.objects.all().delete()
        Category.objects.all().delete()
        Thumbnail.objects.all().delete()
        Publisher.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()
    
    def test_success_get_book_and_author_list(self) :
        client = Client()

        response = client.get('/subscribe/search?keyword=t')
        self.assertEqual(response.status_code, 200)

    def test_success_get_raise_url_error(self) :
        client = Client()

        response = client.get('/subscribe/sarch?keyword=a')
        self.assertEqual(response.status_code, 404)        