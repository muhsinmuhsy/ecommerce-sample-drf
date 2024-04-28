from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cart, CartItem,Order
from .serializers import CartItemSerializer, OrderSerializer


# class AddToCartView(APIView):
#     def post(self, request):
#         serializer = CartItemSerializer(data=request.data)
#         if serializer.is_valid():
#             product_id = serializer.validated_data['product'].id  # Extract the ID of the product
#             quantity = serializer.validated_data['quantity']
#             user = request.user

#             # Check if the user has a cart, create one if not
#             cart, created = Cart.objects.get_or_create(user=user)

#             # Add or update the quantity of the product in the cart
#             cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)
#             cart_item.quantity += quantity
#             cart_item.save()

#             return Response({'message': 'Item added to cart successfully'}, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddToCartView(APIView):
    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product'].id
            quantity = serializer.validated_data['quantity']
            user = request.user

            # Check if the user has a cart, create one if not
            cart, created = Cart.objects.get_or_create(user=user)

            # Add or update the quantity of the product in the cart
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id, defaults={'quantity': quantity})

            # If the cart item already exists, update the quantity
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            return Response({'message': 'Item added to cart successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# {
#     "product": 1,
#     "quantity": 2
# }




class CreateOrderView(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            shipping_address = serializer.validated_data['shipping_address']
            billing_address = serializer.validated_data['billing_address']

            # Get the user's cart
            cart = Cart.objects.get(user=user)

            # Create the order
            order = Order.objects.create(
                user=user,
                shipping_address=shipping_address,
                billing_address=billing_address,
            )

            # Add items from the cart to the order
            for cart_item in cart.cart_items.all():
                order.items.add(cart_item.product, through_defaults={'quantity': cart_item.quantity})

            # Clear the cart after creating the order
            cart.cart_items.clear()

            return Response({'message': 'Order created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
