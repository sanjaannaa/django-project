from django.urls import path
from product import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('index/', views.index),
    path('filter/<category_value>', views.filter_by_catgory),
    path('sort/<sort_value>', views.sort_by_price),
    path('rating/<rating_value>', views.sort_by_rating),
    path('price', views.filter_by_price),
    path('details/<pid>', views.details),
    path('add/<pid>', views.add_to_cart),
    path('view/', views.view_cart),
    path('remove_item/<cid>', views.remove_item),
    path('update_quantity/<flag>/<cartid>', views.update_quantity),
    path('place_order/', views.place_order),
    path('make_payment/', views.make_payment),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)