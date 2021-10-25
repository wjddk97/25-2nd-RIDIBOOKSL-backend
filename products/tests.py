import json
from django.http import response
from django.test     import TestCase, Client, client
from users.models    import User
from products.models import (
    BookAuthor,
    Menu,
    Category,
    Rating,
    Thumbnail,
    Publisher,
    Book,
    Author
)

class ProductsAppTest(TestCase) :
    def setUp(self) :
        menu_id      = Menu.objects.create(id=1 ,name='test').id
        category_id  = Category.objects.create(id=1, menu_id=menu_id, name='test').id
        user_list = [
            User(
                id               = 1,
                account_email    = 'ridi1@test.com',
                profile_nickname = 'ridi1'
            ),
            User(
                id               = 2,
                account_email    = 'ridi2@test.com',
                profile_nickname = 'ridi1'
            ),
            User(
                id               = 3,
                account_email    = 'ridi3@test.com',
                profile_nickname = 'ridi1'
            ),
            User(
                id               = 4,
                account_email    = 'ridi4@test.com',
                profile_nickname = 'ridi1'
            ),
            User(
                id               = 5,
                account_email    = 'ridi5@test.com',
                profile_nickname = 'ridi1'
            ),
            User(
                id               = 6,
                account_email    = 'ridi6@test.com',
                profile_nickname = 'ridi1'
            ),
            User(
                id               = 7,
                account_email    = 'ridi7@test.com',
                profile_nickname = 'ridi1'
            ),
            User(
                id               = 8,
                account_email    = 'ridi8@test.com',
                profile_nickname = 'ridi1'
            ),
            User(
                id               = 9,
                account_email    = 'ridi9@test.com',
                profile_nickname = 'ridi1'
            ),
            User(
                id               = 10,
                account_email    = 'ridi10@test.com',
                profile_nickname = 'ridi1'
            )
        ]
        User.objects.bulk_create(user_list)
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
        publisher_id = Publisher.objects.create(id=1, name='test').id
        book_list = [
            Book(
                id            = 1,
                menu_id       = menu_id,
                category_id   = category_id,
                thumbnail_id  = Thumbnail.objects.get(id=1).id,
                publisher_id  = publisher_id,
                price         = 5000,
                main_name     = 'test1',
                rent_discount = 1
            ),
            Book(
                id            = 2,
                menu_id       = menu_id,
                category_id   = category_id,
                thumbnail_id  = Thumbnail.objects.get(id=2).id,
                publisher_id  = publisher_id,
                price         = 5000,
                main_name     = 'test2',
                rent_discount = 1
            ),
            Book(
                id            = 3,
                menu_id       = menu_id,
                category_id   = category_id,
                thumbnail_id  = Thumbnail.objects.get(id=3).id,
                publisher_id  = publisher_id,
                price         = 5000,
                main_name     = 'test3',
                rent_discount = 1
            ),
            Book(
                id            = 4,
                menu_id       = menu_id,
                category_id   = category_id,
                thumbnail_id  = Thumbnail.objects.get(id=4).id,
                publisher_id  = publisher_id,
                price         = 5000,
                main_name     = 'test4',
                rent_discount = 1
            ),
            Book(
                id            = 5,
                menu_id       = menu_id,
                category_id   = category_id,
                thumbnail_id  = Thumbnail.objects.get(id=5).id,
                publisher_id  = publisher_id,
                price         = 5000,
                main_name     = 'test5',
                rent_discount = 1
            ),
            Book(
                id            = 6,
                menu_id       = menu_id,
                category_id   = category_id,
                thumbnail_id  = Thumbnail.objects.get(id=6).id,
                publisher_id  = publisher_id,
                price         = 5000,
                main_name     = 'test6',
                rent_discount = 0
            ),
            Book(
                id            = 7,
                menu_id       = menu_id,
                category_id   = category_id,
                thumbnail_id  = Thumbnail.objects.get(id=7).id,
                publisher_id  = publisher_id,
                price         = 5000,
                main_name     = 'test7',
                rent_discount = 0
            ),
            Book(
                id            = 8,
                menu_id       = menu_id,
                category_id   = category_id,
                thumbnail_id  = Thumbnail.objects.get(id=8).id,
                publisher_id  = publisher_id,
                price         = 5000,
                main_name     = 'test8',
                rent_discount = 0
            ),
            Book(
                id            = 9,
                menu_id       = menu_id,
                category_id   = category_id,
                thumbnail_id  = Thumbnail.objects.get(id=9).id,
                publisher_id  = publisher_id,
                price         = 5000,
                main_name     = 'test9',
                rent_discount = 0
            ),
            Book(
                id            = 10,
                menu_id       = menu_id,
                category_id   = category_id,
                thumbnail_id  = Thumbnail.objects.get(id=10).id,
                publisher_id  = publisher_id,
                price         = 5000,
                main_name     = 'test10',
                rent_discount = 0
            )
        ]
        Book.objects.bulk_create(book_list)
        author_list = [
            Author(
                id         = 1,
                name       = 'test1',
                birthdate  = '1994-09-26',
                country    = 'korea',
                updated_at = '2021-10-28'
            ),
            Author(
                id         = 2,
                name       = 'test2',
                birthdate  = '1994-09-26',
                country    = 'korea',
                updated_at = '2021-10-28'
            ),
            Author(
                id         = 3,
                name       = 'test3',
                birthdate  = '1994-09-26',
                country    = 'korea',
                updated_at = '2021-10-28'
            ),
            Author(
                id         = 4,
                name       = 'test4',
                birthdate  = '1994-09-26',
                country    = 'korea',
                updated_at = '2021-10-28'
            ),
            Author(
                id         = 5,
                name       = 'test5',
                birthdate  = '1994-09-26',
                country    = 'korea',
                updated_at = '2021-10-28'
            ),
            Author(
                id         = 6,
                name       = 'test6',
                birthdate  = '1994-09-26',
                country    = 'korea',
                updated_at = '2021-10-28'
            ),
            Author(
                id         = 7,
                name       = 'test7',
                birthdate  = '1994-09-26',
                country    = 'korea',
                updated_at = '2021-10-28'
            ),
            Author(
                id         = 8,
                name       = 'test8',
                birthdate  = '1994-09-26',
                country    = 'korea',
                updated_at = '2021-10-28'
            ),
            Author(
                id         = 9,
                name       = 'test9',
                birthdate  = '1994-09-26',
                country    = 'korea',
                updated_at = '2021-10-28'
            ),
            Author(
                id         = 10,
                name       = 'test10',
                birthdate  = '1994-09-26',
                country    = 'korea',
                updated_at = '2021-10-28'
            )
        ]
        Author.objects.bulk_create(author_list)
        rating_list = [
            Rating(
                id      = 1,
                book_id = Book.objects.get(id=1).id,
                user_id = User.objects.get(id=1).id,
                rating  = 1
            ),
            Rating(
                id      = 2,
                book_id = Book.objects.get(id=1).id,
                user_id = User.objects.get(id=2).id,
                rating  = 2
            ),
            Rating(
                id      = 3,
                book_id = Book.objects.get(id=1).id,
                user_id = User.objects.get(id=3).id,
                rating  = 3
            ),
            Rating(
                id      = 4,
                book_id = Book.objects.get(id=1).id,
                user_id = User.objects.get(id=4).id,
                rating  = 4
            ),
            Rating(
                id      = 5,
                book_id = Book.objects.get(id=1).id,
                user_id = User.objects.get(id=5).id,
                rating  = 5
            ),
            Rating(
                id      = 6,
                book_id = Book.objects.get(id=1).id,
                user_id = User.objects.get(id=6).id,
                rating  = 1
            ),
            Rating(
                id      = 7,
                book_id = Book.objects.get(id=1).id,
                user_id = User.objects.get(id=7).id,
                rating  = 2
            ),
            Rating(
                id      = 8,
                book_id = Book.objects.get(id=1).id,
                user_id = User.objects.get(id=8).id,
                rating  = 3
            ),
            Rating(
                id      = 9,
                book_id = Book.objects.get(id=1).id,
                user_id = User.objects.get(id=9).id,
                rating  = 4
            ),
            Rating(
                id      = 10,
                book_id = Book.objects.get(id=1).id,
                user_id = User.objects.get(id=10).id,
                rating  = 5
            )
        ]
        Rating.objects.bulk_create(rating_list)

        BookAuthor.objects.bulk_create([BookAuthor(id=i+1, book_id=Book.objects.get(id=i+1).id, author_id=Author.objects.get(id=i+1).id) for i in range(10)])

    def tearDown(self) :
        Menu.objects.all().delete()
        Category.objects.all().delete()
        Rating.objects.all().delete()
        Thumbnail.objects.all().delete()
        Publisher.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()

    def test_success_get_author_list(self) :
        client   = Client()
        response = client.get('/products/authors/1')
        self.assertEqual(response.status_code, 200)

    def test_success_get_author_list_not_found_url(self) :
        client   = Client()
        response = client.get('/produc/authors/6')
        self.assertEqual(response.status_code, 404)

    def test_success_product_main_view(self) :
        client   = Client()
        response = client.get('/products/main')
        self.assertEqual(response.status_code, 200)

    def test_success_product_view(self) :
        client   = Client()
        response = client.get('/products?offset=0&limit=10&descending=3&menu=1')
        self.assertEqual(response.status_code, 200)
    
    def test_success_product_view_invalid_query_parameter(self) :
        client   = Client()
        response = client.get('/products?offset=0&limit=10&descending=3&menu=10')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{
            'message' : "MENU_DOES_NOT_EXIST"
        })

    def test_success_search_view(self) :
        client   = Client()
        response = client.get('/products/search?keyword=t')
        self.assertEqual(response.status_code, 200)
    
    def test_success_detail_product_view(self) :
        client   = Client()
        response = client.get('/products/1')
        self.assertEqual(response.status_code, 200)
    
    def test_success_detail_view_create_rating(self) :
        client = Client()

        headers = {'HTTP_Authorization' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.loTjeBWZ9SeXV-BcIxqOtX37AN30ROvsZl0_udeeRJU'}

        new_rating = {
            'user_id' : User.objects.get(id=1).id,
            'book_id' : Book.objects.get(id=2).id,
            'rating'  : 3
        }

        response = client.post('/products/1', json.dumps(new_rating), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),{
            'message':'SUCCESS'
        })