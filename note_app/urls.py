from django.urls import path
from .views import (
    login_page, 
    register_page,
    home_page, 
    logout_page,
    note_view,
    save_note,
    delete_note,
    create_note
)


urlpatterns = [
    path('', home_page, name='home'),
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout/', logout_page, name='logout'),
    path('note-list/', note_view, name='note-list'),
    path('note/save/<int:pk>/', save_note, name='save-note'),
    path('note/delete/<int:pk>/', delete_note, name='delete-note'),
    path('note/create/', create_note, name='create-note'),
]