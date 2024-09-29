from django.shortcuts import render, redirect
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse
import json

# Razorpay client initialization
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def index(request):
    if request.method == 'GET':
        amount = 1 * 100  # Set the amount in paisa (e.g., 10000 for 100 INR)

        # Create a Razorpay order
        payment_order = razorpay_client.order.create({
            'amount': amount,
            'currency': 'INR',
            'payment_capture': '1'  # Auto capture after successful payment
        })

        context = {
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,  # Razorpay key id
            'order_id': payment_order['id'],  # The Razorpay order id
            'amount': amount
        }

        # Render the index.html and pass context
        return render(request, 'index.html', context)

    return HttpResponseBadRequest("Invalid Request")


@csrf_exempt
def payment_callback(request):
    if request.method == "POST":
        # Parse the JSON body
        data = json.loads(request.body)

        params_dict = {
            'razorpay_payment_id': data.get('razorpay_payment_id', ''),
            'razorpay_order_id': data.get('razorpay_order_id', ''),
            'razorpay_signature': data.get('razorpay_signature', ''),
        }

        try:
            # Verify the payment signature
            razorpay_client.utility.verify_payment_signature(params_dict)
            # Payment is successful
            return JsonResponse({'status': 'success'})
        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({'status': 'failure'}, status=400)

    return HttpResponseBadRequest("Invalid Request")

@csrf_exempt
def payment_success(request):
    return render(request, 'payment_success.html')
