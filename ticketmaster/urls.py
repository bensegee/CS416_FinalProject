from django.urls import path
from . import views

urlpatterns = [
   path('comments/<str:id>/add', views.add_product, name="add"),
   path('comments/<str:name>/update/<str:id>', views.update_product, name="update"),
   path('comments/<str:name>/delete/<str:id>', views.delete_product, name="delete"),
   path('', views.eventSearch, name='ticketmaster-index'),
   path('comments/<str:id>',views.comments,name='comments'),
]

