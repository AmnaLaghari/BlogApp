from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import AddReplyView, AddSuggestionView, DeleteSuggestionView, SuggestionViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
     'api/suggestionsviewset', SuggestionViewSet, basename='suggestion'
)

urlpatterns = [
    path('<int:pk>/suggestion/add_suggestion', login_required(
        AddSuggestionView.as_view(), login_url='signin'), name='add_suggestion'),
    path('suggestions/delete_suggestion/<int:pk>', login_required(
        DeleteSuggestionView.as_view(), login_url='signin'), name='delete_suggestion'),
    path('suggestions/reply_suggestion/<int:pk>',
         login_required(AddReplyView.as_view(), login_url='signin'), name='reply_suggestion'),
]+router.urls
