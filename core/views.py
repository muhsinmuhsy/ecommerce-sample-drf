from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Cart, CartItem, Address, Order, OrderItem, Payment, Product
from .serializers import CartSerializer, CartItemSerializer, AddressSerializer, OrderSerializer, PaymentSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import User

# user = User.objects.get(username='your_username')
# token = Token.objects.create(user=user)
# print(token.key)



class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)



class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        product = Product.objects.get(id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

class ViewCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        return Response(CartSerializer(cart).data)

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        shipping_address_data = request.data.get('shipping_address')
        billing_address_data = request.data.get('billing_address', shipping_address_data)
        payment_data = request.data.get('payment')

        shipping_address_serializer = AddressSerializer(data=shipping_address_data)
        billing_address_serializer = AddressSerializer(data=billing_address_data)
        payment_serializer = PaymentSerializer(data=payment_data)

        if shipping_address_serializer.is_valid() and billing_address_serializer.is_valid() and payment_serializer.is_valid():
            shipping_address = shipping_address_serializer.save(user=request.user)
            billing_address = billing_address_serializer.save(user=request.user)
            order = Order.objects.create(user=request.user, shipping_address=shipping_address, billing_address=billing_address)
            for cart_item in cart.cart_items.all():
                OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
            cart.cart_items.all().delete()
            payment = payment_serializer.save(user=request.user, order=order, amount=order.total_price())
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

        return Response({
            'shipping_address_errors': shipping_address_serializer.errors,
            'billing_address_errors': billing_address_serializer.errors,
            'payment_errors': payment_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class OrderConfirmationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = Order.objects.get(id=order_id, user=request.user)
        return Response(OrderSerializer(order).data)




# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .models import Cart, CartItem,Order
# from .serializers import CartItemSerializer, OrderSerializer


# # class AddToCartView(APIView):
# #     def post(self, request):
# #         serializer = CartItemSerializer(data=request.data)
# #         if serializer.is_valid():
# #             product_id = serializer.validated_data['product'].id  # Extract the ID of the product
# #             quantity = serializer.validated_data['quantity']
# #             user = request.user

# #             # Check if the user has a cart, create one if not
# #             cart, created = Cart.objects.get_or_create(user=user)

# #             # Add or update the quantity of the product in the cart
# #             cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)
# #             cart_item.quantity += quantity
# #             cart_item.save()

# #             return Response({'message': 'Item added to cart successfully'}, status=status.HTTP_201_CREATED)
# #         else:
# #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AddToCartView(APIView):
#     def post(self, request):
#         serializer = CartItemSerializer(data=request.data)
#         if serializer.is_valid():
#             product_id = serializer.validated_data['product'].id
#             quantity = serializer.validated_data['quantity']
#             user = request.user

#             # Check if the user has a cart, create one if not
#             cart, created = Cart.objects.get_or_create(user=user)

#             # Add or update the quantity of the product in the cart
#             cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id, defaults={'quantity': quantity})

#             # If the cart item already exists, update the quantity
#             if not created:
#                 cart_item.quantity += quantity
#                 cart_item.save()

#             return Response({'message': 'Item added to cart successfully'}, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # {
# #     "product": 1,
# #     "quantity": 2
# # }




# class CreateOrderView(APIView):
#     def post(self, request):
#         serializer = OrderSerializer(data=request.data)
#         if serializer.is_valid():
#             user = request.user
#             shipping_address = serializer.validated_data['shipping_address']
#             billing_address = serializer.validated_data['billing_address']

#             # Get the user's cart
#             cart = Cart.objects.get(user=user)

#             # Create the order
#             order = Order.objects.create(
#                 user=user,
#                 shipping_address=shipping_address,
#                 billing_address=billing_address,
#             )

#             # Add items from the cart to the order
#             for cart_item in cart.cart_items.all():
#                 order.items.add(cart_item.product, through_defaults={'quantity': cart_item.quantity})

#             # Clear the cart after creating the order
#             cart.cart_items.clear()

#             return Response({'message': 'Order created successfully'}, status=status.HTTP_201_CREATED)
#         else:   
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
