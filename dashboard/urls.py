from django.urls import path
from . import views

app_name='dashboard'

urlpatterns = [
    path('post_list/', views.post_list, name='post_list'),
    path('<int:id>/', views.post_detail, name='post_detail'),
    path('profile/', views.profile_view, name='profile'),
    path('', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('add_blog_post/', views.add_blog_post, name='add_blog_post'), 
    path('<int:id>/delete/', views.post_delete, name='post_delete'),
    path('lipa-na-mpesa/', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),
    path('mpesa-callback/', views.mpesa_callback, name='mpesa_callback'),
# Add this line

]

