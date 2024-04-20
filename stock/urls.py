from django.urls import path
from .views import *

urlpatterns = [
    path('category/add/', CreateCategoryAPIView.as_view()),
    path('category/manage/<int:pk>/', ManageCategoryAPIView.as_view()),
    
    path('product/add/', ProductAPIView.as_view()),
    path('product/manage/<int:pk>/', ProductManageAPIView.as_view()),
    
    path('order/create/', OrderCreateAPIView.as_view()),
    
    path('cart/manage/<int:pk>/', ManageCartAPIView.as_view()),
]
