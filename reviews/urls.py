from django.urls import path
from . import views

app_name = 'reviews'
urlpatterns = [
    # ex: /reviews/
    path('', views.IndexView.as_view(), name='index'),
    # ex: /reviews/5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # ex: /reviews/5/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # ex: /reviews/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),

    path('add_review_form/', views.AddReviewForm.as_view(), name='add_review_form'),
    path('add_review_form/add_review_action', views.add_review_action, name='add_review_action'),
]