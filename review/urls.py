from django.urls import path
from .views import ReviewListView,AuthorListCreateAPIView, ReviewCreateAPIView
from .views import AuthorListCreateAPIView,BookListUpdateAPIView,BookCreateAPIView


urlpatterns = [
    path('authors/', AuthorListCreateAPIView.as_view(), name='author-list-create'),
    path('books_create/', BookCreateAPIView.as_view(), name='book-create'),
    path('books/<int:pk>/', BookListUpdateAPIView.as_view(), name='book-list-update'),
    path('review_create/', ReviewCreateAPIView.as_view(), name='review-create'),
    path('reviews/author/', ReviewListView.as_view(), name='review-list'),
]

    
   