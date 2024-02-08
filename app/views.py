from django.http import JsonResponse
import stripe
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from rest_framework import viewsets
from rest_framework.views import APIView
from .stripe import PaymentView, create_stripe_customer
from .models import IceCream, Order
from .serializers import UserSerializer, IceCreamSerializer, OrderSerializer


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            customer_id = create_stripe_customer(
                name=request.data.get("first_name"), email=request.data.get("email")
            )
            serializer.save(customer=customer_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IceCreamViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = IceCream.objects.all()
    serializer_class = IceCreamSerializer


class OrderGetAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, order_id=None):
        if order_id is not None:
            try:
                order = Order.objects.get(id=order_id)
                serializer = OrderSerializer(order)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Order.DoesNotExist:
                return Response(
                    {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class OrderCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            with transaction.atomic():
                order_instance = serializer.save()
                icecream_ids = request.data.get("icecreams", [])
                order_instance.icecreams.add(*icecream_ids)
                total_price = order_instance.icecreams.aggregate(
                    total_price=Sum("price")
                )["total_price"]
                order_instance.total_price = total_price
                request.data["total_price"] = total_price
                user_first_name = serializer.validated_data["user"].first_name
                request.data["user"] = user_first_name
                request.data["order_id"] = serializer.data.get("id")
                order_instance.save()
                payment_view = PaymentView()
                payment_response = payment_view.post(request)
                if payment_response.status_code == 201:
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    transaction.set_rollback(True)
                    return payment_response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentConfirmView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            payment_method = request.data.get("payment_method")
            return_url = request.data.get("return_url")
            payment_id = request.data.get("payment_id")

            response = stripe.PaymentIntent.confirm(
                payment_id,
                payment_method=payment_method,
                return_url=return_url,
            )
            return JsonResponse(
                {
                    "data": response.next_action._previous.get(
                        "redirect_to_url", {}
                    ).get("url"),
                    "message": "Order Created successful",
                }
            )
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
