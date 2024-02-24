from django.http import JsonResponse
from .models import Author,Book,Review
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import AuthorSerializer,BookSerializer,ReviewSerializer
from django.http import Http404
from django.shortcuts import get_object_or_404
from decimal import Decimal


class AuthorListCreateAPIView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(total_rating=0)  # Set the total rating to zero for the new author
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    


class BookCreateAPIView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            author_id = request.data.get('author_id')
            if not Author.objects.filter(id=author_id).exists():
                return Response({'error': 'Invalid author_id'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save(author_id=author_id)  
            author = Author.objects.get(id = author_id)
            author.published_books += int(1)
            author.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookListUpdateAPIView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = BookSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = BookSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        try:
            return Book.objects.get(pk=self.kwargs['pk'])
        except Book.DoesNotExist:
            raise Http404

        



class ReviewCreateAPIView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    
    serializer_class = ReviewSerializer

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to create a review.'}, status=status.HTTP_403_FORBIDDEN)

        author_id = request.data.get('author_id')
        book_id = request.data.get('book_id')
        rating = request.data.get('rating')
        if rating is not None and (rating < 0 or rating > 5):
            return Response({"message": "The rating must be a value between 0 and 5."})


        author = get_object_or_404(Author, id=author_id) if author_id else None
        book = get_object_or_404(Book, id=book_id) if book_id else None

        author_table = Author.objects.get(id = author_id)
        author_table.author_review_count += int(1)
        author_table.rating_sum += Decimal(rating)
        author_table.total_rating = Decimal( author_table.rating_sum) / Decimal(author_table.author_review_count)
        author_table.save()


        book_table = Book.objects.get(id = book_id)
        book_table.book_review_count += int(1)
        book_table.rating_sum += Decimal(rating)
        book_table.total_rating = Decimal( book_table.rating_sum) / Decimal(book_table.book_review_count)
        book_table.save()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, author=author, book=book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ReviewListView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self, request, *args, **kwargs):
        author_id = request.data.get('author_id')
        if author_id:
            reviews = Review.objects.filter(author__id=author_id)
            if not reviews.exists():
                return Response({"message": "The author has no reviews."})
        else:
            return Response({"message": "The author has no reviews."})
        
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

