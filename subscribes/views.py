from django.http       import JsonResponse
from django.views      import View

from subscribes.models import Subscribe
from products.models   import (
    Author, 
    BookAuthor, 
    Book, 
    Publisher
)

from users.utils       import login_decorator
class SubscribeView(View) :
    @login_decorator
    def post(self, request) :
        try :
            author_id = int(request.GET.get('author_id'))

            subscribe, state = Subscribe.objects.get_or_create(
                author_id = author_id,
                user_id   = request.user.id
            )

            if not state :
                subscribe.delete()
                return JsonResponse({'message' : 'delete success'}, status=201)
            
            return JsonResponse({'message' : 'create success'}, status=201)

        except KeyError :
            JsonResponse({'message' : 'KEY ERROR'}, status=400)

        except AttributeError :
            JsonResponse({'message' : 'Attribute Error'}, status=400)
        
        except TypeError :
            JsonResponse({'message' : 'Type Error'}, status=400)            

class SearchView(View) :
    def get(self, request) :
        try :
            keyword = request.GET.get('keyword')

            author_list = [
                {
                    'author_id'    : author.id,
                    'author_name'  : author.name,
                    'author_books' : [Book.objects.get(id=book.book_id).main_name for book in BookAuthor.objects.filter(author_id=author.id)]
                }
            for author in Author.objects.filter(name__icontains=keyword)]

            book_list = [
                {
                    'book_id'        : book.id,
                    'book_name'      : book.main_name,
                    'book_author'    : [Author.objects.get(id=author.author_id).name for author in BookAuthor.objects.filter(book_id=book.id)],
                    'book_publisher' : Publisher.objects.get(id=book.publisher_id).name
                }
            for book in Book.objects.filter(main_name__icontains=keyword)]
            
            return JsonResponse({'author_list' : author_list, 'book_list' : book_list}, status=200)

        except Author.DoesNotExist :
            return JsonResponse({'message' : 'Author DoesNotExist'}, status=400)

        except BookAuthor.DoesNotExist :
            return JsonResponse({'message' : 'BookAuthor DoesNotExist'}, status=400)

        except Book.DoesNotExist :
            return JsonResponse({'message' : 'Book DoesNotExist'}, status=400)