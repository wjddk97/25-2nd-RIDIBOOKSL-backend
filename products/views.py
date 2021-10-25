import json

from datetime                     import date, timedelta
from logging import log
from django.db.models.aggregates  import Count, Max, Sum
from django.db.models.query_utils import Q
from django.views                 import View
from django.http                  import JsonResponse
from django.db.models             import Avg

from products.models              import Book, BookAuthor, ViewCount, Thumbnail, Menu, Rating, Author, Category, Publisher
from users.utils                  import login_decorator

class ProductMainView(View):
    def get(serlf, request):
        products  = Book.objects.all().order_by('-created_at')
        new_books = [{
            'book_id'   : product.id,
            'thumbnail' : product.thumbnail.image_url,
            'book_name' : product.main_name,
            'author'    : BookAuthor.objects.filter(book_id = product.id).first().author.name,
            'patch'     : int(product.rent_discount)
        } for product in products]
            
        yesterday   = date.today() - timedelta(1)
        view_counts = ViewCount.objects.filter(created_at=yesterday).values('book_id').annotate(max_count=Count('book_id')).order_by('-max_count')
        daily_best  = [{
            'book_id'   : view_count['book_id'],
            'thumbnail' : Thumbnail.objects.get(id=Book.objects.get(id=view_count['book_id']).thumbnail_id).image_url,
            'book_name' : Book.objects.get(id=view_count['book_id']).main_name,
            'author'    : BookAuthor.objects.filter(book_id = view_count['book_id']).first().author.name,
            'patch'     : int(Book.objects.get(id=view_count['book_id']).rent_discount)
        } for view_count in view_counts]


        view_counts = ViewCount.objects.values('book_id').annotate(max_count=Count('book_id')).order_by('-max_count')
        best_seller = [{
            'book_id'   : view_count['book_id'],
            'thumbnail' : Thumbnail.objects.get(id=Book.objects.get(id=view_count['book_id']).thumbnail_id).image_url,
            'book_name' : Book.objects.get(id=view_count['book_id']).main_name,
            'author'    : BookAuthor.objects.filter(book_id = view_count['book_id']).first().author.name,
            'patch'     : int(Book.objects.get(id=view_count['book_id']).rent_discount)
        } for view_count in view_counts]
        
        return JsonResponse({'new_books': new_books, 'daily_best': daily_best, 'best_seller': best_seller}, status=200)    

class ProductView(View):
    def get(self, request):
        try:
            menu       = request.GET.get('menu',1)
            category   = request.GET.get('category', None)
            descending = int(request.GET.get('descending', 4))
            offset     = int(request.GET.get('offset', 0))
            limit      = int(request.GET.get('limit', 100))
            menu_name  = Menu.objects.get(id=menu).name

            order_dic = {
                0 : '-created_at',
                1 : 1,
                2 : 2,
                3 : 'max_count',
                4 : 'created_at'
            }

            q = Q()

            if menu:
                q.add(Q(menu_id=menu), q.AND)
                books = Book.objects.filter(q)[offset:limit+offset]

            if category:
                q.add(Q(category_id=category), q.AND)
                books         = Book.objects.filter(q)[offset:limit+offset]
                category_name = Category.objects.get(id=category).name
            else:
                category_name = []

            if descending == 0 or descending == 4:
                books = Book.objects.filter(q).order_by(order_dic[descending])[offset:limit+offset]
            
            if descending == 1 or descending == 2:
                books = Book.objects.filter(q, rent_discount=order_dic[descending])[offset:limit+offset]

            if descending == 3:
                books = Book.objects.filter(q).annotate(max_count=Count('viewcount__book_id')).order_by(order_dic[descending])[offset:limit+offset]

            products = [{
                'book_id'        : book.id,
                'book_category'  : book.category.name,
                'menu'           : book.menu.name,
                'book_thumbnail' : book.thumbnail.image_url,
                'book_name'      : book.main_name,
                'author_id'      : BookAuthor.objects.filter(book_id=book.id).first().author.id,
                'author_name'    : BookAuthor.objects.filter(book_id=book.id).first().author.name,
                'rating'         : Rating.objects.filter(book_id=book.id).aggregate(Avg('rating'))['rating__avg'],
                'rating_count'   : Rating.objects.filter(book_id=book.id).count(),
                'book_publisher' : book.publisher.name,
                'book_price'     : book.price,
                'patch'          : int(book.rent_discount),
                'sale_price'     : int(book.price * 0.9) if book.rent_discount == 1 else None,
            } for book in books]

        except Menu.DoesNotExist:
            return JsonResponse({'message': 'MENU_DOES_NOT_EXIST'}, status=400)
        
        except Category.DoesNotExist:
            return JsonResponse({'message': 'CATEGORY_DOES_NOT_EXIST'}, status=400)

        return JsonResponse({'products': products, 'menu_name' : menu_name, 'category_name' : category_name}, status=200)

class SearchView(View):
    def get(self, request):
        descending = int(request.GET.get('descending', 4))
        keyword    = request.GET.get('keyword',None) 
        offset     = int(request.GET.get('offset', 0))
        limit      = int(request.GET.get('limit', 100))         
        authors    = Author.objects.filter(name__icontains=keyword)
        
        order_dic = {
                0 : '-created_at',
                1 : 1,
                2 : 2,
                3 : 'max_count',
                4 : 'created_at'
            }
        
        if descending == 0 or descending == 4:
            books = Book.objects.filter(main_name__icontains=keyword).order_by(order_dic[descending])[offset:limit+offset]
            
        if descending == 1 or descending == 2:
            books = Book.objects.filter(main_name__icontains=keyword, rent_discount=order_dic[descending])[offset:limit+offset]
        
        if descending == 3:
            books = Book.objects.filter(main_name__icontains=keyword).annotate(max_count=Count('viewcount__book_id')).order_by(order_dic[descending])[offset:limit+offset]

        author_list = [{
            'author_id'    : author.id,
            'author_name'  : author.name,
            'author_books' : [Book.objects.get(id=book.book_id).main_name for book in BookAuthor.objects.filter(author_id=author.id)]
        } for author in authors]

        book_list = [{
            'book_category'  : book.category.name,
            'book_id'        : book.id,
            'book_thumbnail' : book.thumbnail.image_url,
            'book_name'      : book.main_name,
            'author_id'      : BookAuthor.objects.filter(book_id=book.id).first().author.id,
            'author_name'    : BookAuthor.objects.filter(book_id=book.id).first().author.name,
            'book_publisher' : book.publisher.name,
            'rating'         : Rating.objects.filter(book_id=book.id).aggregate(Avg('rating'))["rating__avg"],
            'rating_count'   : Rating.objects.filter(book_id=book.id).count(),
            'book_price'     : book.price,
            'sale_price'     : int(book.price * 0.9) if book.rent_discount == 1 else None,
            'patch'          : int(book.rent_discount) 
        } for book in books]
       
        return JsonResponse({'author_list': author_list, 'book_list' : book_list}, status=200)

class DetailProductView(View):
    def get(self, request, book_id):
        try:    
            product      = Book.objects.get(id=book_id)
            author       = BookAuthor.objects.filter(book_id=book_id).first().author
            book_rating  = Rating.objects.filter(book_id=book_id).aggregate(Avg('rating'))
        
            books        = BookAuthor.objects.filter(author_id=author.id)
            author_books = [{
                'name'      : book.book.main_name,
                'thumbnail' : book.book.thumbnail.image_url,
                'rating'    : Rating.objects.filter(book_id=book.book.id).aggregate(Avg('rating'))["rating__avg"]
            } for book in books]
            
            author_info = [{
                'author_id'   : author.id,
                'name'        : author.name,
                'country'     : author.country,
                'birthdate'   : author.birthdate,
                'info_update' : author.updated_at.strftime('%Y.%m.%d'),
                'books'       : author_books 
            }]

            product_detail = [{
                'id'               : product.id, 
                'menu'             : product.menu.name,
                'category'         : product.category.name,
                'thumbnail'        : product.thumbnail.image_url,
                'name'             : product.main_name,
                'sub_name'         : product.sub_name,
                'rating'           : int(book_rating["rating__avg"]),
                'translator'       : product.translator,
                'publisher'        : product.publisher.name,
                'price'            : product.price,
                'publication_date' : product.created_at.strftime('%Y.%m.%d'),
                'patch'            : int(product.rent_discount),
                'sale_price'       : int(product.price * 0.9) if product.rent_discount == 1 else None,
                'author_info'      : author_info,
            }]
            
            return JsonResponse({'product_detail' : product_detail}, status=200) 
        
        except Book.DoesNotExist:
            return JsonResponse({'message': 'BOOK_DOES_NOT_EXIST'}, status=400)
    
    @login_decorator
    def post(self, request, book_id):
        try:
            data    = json.loads(request.body)
            user_id = request.user.id
            rating  = data['rating']
            
            book_rating = Rating.objects.filter(user_id=user_id, book_id=book_id).first()
            if Rating.objects.filter(user_id=user_id, book_id=book_id).exists():
                book_rating.rating = rating
                book_rating.save()
            else:    
                Rating.objects.create(
                    user_id = user_id,
                    book_id = book_id,
                    rating  = rating
                )

            return JsonResponse({'message':'SUCCESS'}, status=201)  
        
        except json.JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class AuthorListView(View) :
    def get(self, request, author_id) :
        try :
            obj_author      = Author.objects.get(id=author_id)
            books_authors   = BookAuthor.objects.filter(author_id=obj_author.id)
            books           = Book.objects.all()
            thumbnail_image = Thumbnail.objects.all()
            publisher       = Publisher.objects.all()
            category        = Category.objects.all()
            rating          = Rating.objects.all()
            author_info = {
                'author_name'      : obj_author.name,
                'author_country'   : obj_author.country,
                'author_birthdate' : obj_author.birthdate.strftime('%Y')
            }
            author_books = [
                {   'book_id'         : book.book_id,
                    'book_category'   : category.get(id=books.get(id=book.book_id).category_id).name,
                    'author_id'       : book.author_id,
                    'patch'           : int(books.get(id=book.book_id).rent_discount),
                    'book_name'       : books.get(id=book.book_id).main_name,
                    'author_name'     : obj_author.name,
                    'sale_price'      : int(books.get(id=book.book_id).price * 0.9),
                    'book_price'      : int(books.get(id=book.book_id).price),
                    'book_publisher'  : publisher.get(id=books.get(id=book.book_id).publisher_id).name,
                    'book_thumbnail'  : thumbnail_image.get(id=books.get(id=book.book_id).thumbnail_id).image_url,
                    'rating'          : round(rating.filter(book_id=book.book_id).aggregate(Avg('rating'))['rating__avg'],2),
                    'rating_count'    : rating.filter(book_id=book.book_id).aggregate(Count('book_id'))['book_id__count']
                }
            if books.get(id=book.book_id).rent_discount == 1
            else
            {       'book_id'         : book.book_id,
                    'book_category'   : category.get(id=books.get(id=book.book_id).category_id).name,
                    'author_id'       : book.author_id,
                    'patch'           : int(books.get(id=book.book_id).rent_discount),
                    'book_name'       : books.get(id=book.book_id).main_name,
                    'author_name'     : obj_author.name,
                    'book_price'      : int(books.get(id=book.book_id).price),
                    'book_publisher'  : publisher.get(id=books.get(id=book.book_id).publisher_id).name,
                    'book_thumbnail'  : thumbnail_image.get(id=books.get(id=book.book_id).thumbnail_id).image_url,
                    'rating'          : round(rating.filter(book_id=book.book_id).aggregate(Avg('rating'))['rating__avg'],2),
                    'rating_count'    : rating.filter(book_id=book.book_id).aggregate(Count('book_id'))['book_id__count']
                }
            for book in books_authors]
            return JsonResponse({'author_info' : author_info, 'author_books' : author_books},  status=200)
        except Book.DoesNotExist :
            return JsonResponse({'message' : 'Book Does Not Exist'}, status=400)
        except Author.DoesNotExist :
            return JsonResponse({'message' : 'Author Does Not Exist'}, status=400)
        except BookAuthor.DoesNotExist :
            return JsonResponse({'message' : 'BookAuthor Does Not Exist'}, status=400)