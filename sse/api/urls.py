from django.urls import path
from .views import AutocompletionView
from .views import SearchView


urlpatterns = [
    path('autocompletion/', AutocompletionView.as_view()),
    path('search/', SearchView.as_view()),
]
