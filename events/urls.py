from django.urls import path

from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.event_list_view, name = "event-list-view"),
    path('<int:event_id>/', views.event_detail_view, name = "detail"),
    path('create-event/', views.event_view, name = "event-list"),
    path('create-event/retry', views.create_event, name = "create-event"),
    path('search/', views.search, name="search"),
    path('rsvp/<int:event_id>/', views.rsvp, name="rsvp"),
    path('delete/', views.delete, name="delete"),
    path('editEvent/', views.edit_event, name='editEvent'),
    path('submitEdit/', views.submit_edit, name="submitEdit"),
]
