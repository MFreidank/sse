from django.urls import path
from .views import AutocompletionView


urlpatterns = [
    path('autocompletion/', AutocompletionView.as_view()),
]
