
from rest_framework import generics, viewsets, permissions
from .models import Category, SubCategory, Product, Cart, Order, User
from .serializers import (CategorySerializer, SubCategorySerializer, ProductSerializer,
                          CartSerializer, OrderSerializer, UserSerializer)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


# Registration view
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

class RegisterSellerView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        # Create user with role 'SELLER'
        user = User.objects.create_user(username=username, password=password, email=email)
        user.role = 'SELLER'  # Assign seller role
        user.save()

        # Create JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'role': user.role
        }, status=status.HTTP_201_CREATED)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class SubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [permissions.AllowAny]

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class AddCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'SELLER':
            return Response({'error': 'Only sellers can add category'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        category = Category.objects.create(
            name=data['name'],
        )
        return Response({'message': 'Category added successfully'}, status=status.HTTP_201_CREATED)

class AddSub_CategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'SELLER':
            return Response({'error': 'Only sellers can add sub category'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        category = SubCategory.objects.create(
            name=data['name'],
            category_id=data['category'],
        )
        return Response({'message': 'Category added successfully'}, status=status.HTTP_201_CREATED)

class AddProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'SELLER':
            return Response({'error': 'Only sellers can add products'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        # Logic to add the product
        product = Product.objects.create(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            stock=data['stock'],
            category_id=data['category'],
            subcategory_id=data['subcategory'],
            seller=request.user
        )
        return Response({'message': 'Product added successfully'}, status=status.HTTP_201_CREATED)



class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

# Admin can view all APIs
class AdminProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
