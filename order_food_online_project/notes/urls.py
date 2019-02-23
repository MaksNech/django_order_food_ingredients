from django.urls import path

from . import views

# urlpatterns = [
#     path('', views.NotesTemplateView.as_view(), name='notes'),
#     path('<str:model>/', views.NotesListView.as_view(), name='notes_by_type'),
#     path('add/<str:item>/<int:pk>/', views.NoteCreateView.as_view(), name='note_create'),
# ]

urlpatterns = [
    path('note/', views.note_list, name='note_list'),
    path('note/search/', views.note_search, name='note_search'),
    path('note/add/', views.note_add, name='note_add'),
    path('note/view/<int:note_id>/', views.note_view, name='note_view'),
    path('note/edit/<int:note_id>/', views.note_edit, name='note_edit'),
    path('note/delete/<int:note_id>/', views.note_delete, name='note_delete'),
]
