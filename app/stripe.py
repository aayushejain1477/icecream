import stripe
from django.conf import settings
from django.views.generic.base import View
from django.http import JsonResponse


def create_stripe_customer(name, email):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    response = stripe.Customer.create(name=name, email=email)
    return response.stripe_id


class PaymentView(View):
    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            token = settings.STRIPE_SECRET_KEY
            amount = request.data.get("total_price")
            currency = "USD"
            payment_intent = stripe.PaymentIntent.create(
                amount=int(request.data.get("total_price")),
                currency="USD",
                payment_method_types=["card"],
                customer=request.data.get("stripe_id"),
            )
            order_id = request.data.get("order_id")
            customer = request.data.get("stripe_id")
            return JsonResponse(
                {
                    "message": "Order Created successful",
                    "order_id": order_id,
                    "customer": request.data.get("user"),
                    "payment_id": payment_intent.id,
                    "tital_amount": amount,
                }
            )
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})



