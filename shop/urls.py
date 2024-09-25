from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RegisterView, CategoryViewSet, SubCategoryViewSet, ProductViewSet, CartViewSet, OrderViewSet, \
    AdminProductViewSet, RegisterSellerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'subcategories', SubCategoryViewSet, basename='subcategory')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'admin/products', AdminProductViewSet, basename='admin_product')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/seller/', RegisterSellerView.as_view(), name='register_seller'),
]
urlpatterns += router.urls
