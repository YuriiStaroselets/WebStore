import calendar
import time
import re

from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from accounts.models import Account
from cart.models import CartItem
from orders.forms import OrderForm
from .models import Order, OrderProduct, Payment
import datetime
from store.models import Product, Variation
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from category.models import MainCategory
from .wayforpaymodule import WayForPayAPI
from django.db.models import Sum
from django.conf import settings


def payments(request, order_number):
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)

    wayforpay = WayForPayAPI(
        settings.MERCHANT_ACCOUNT,
        settings.MERCHANT_KEY,
        settings.MERCHANT_DOMAIN,
    )
    names = [f"Оплата замовлення: {order.order_number}"]
    cost = [order.order_total]
    amount = [1]
    return_url = 'http://192.168.1.19:8000/orders/payments/status/'
    datatime = calendar.timegm(time.gmtime())
    order_number = f"{request.user.id}00{order_number}"

    data = {
        'orderReference': order_number,
        'orderDate': datatime,
        'amount': str(order.order_total),
        'currency': 'UAH',
        'productName': names,
        'productPrice': cost,
        'productCount': list(map(int, amount)),
    }
    widget = wayforpay.generate_payment_form(data, return_url)
    context = {
        'widget': widget
    }

    return render(request, "payment_account.html", context)


def payments_status(request):
    if request.method == 'POST':
        data = request.POST
        transaction_status = data.get('transactionStatus')
        if transaction_status == 'Approved':
            user_id_match = re.search(r'(\d+)00', data.get('orderReference'))

            if user_id_match:
                try:
                    user_id = user_id_match.group(1)
                    print(user_id)
                    user = Account._default_manager.get(pk=user_id)
                except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
                    user = None

                order_number = re.search(r'00(.+)', data.get('orderReference'))
                order = Order.objects.get(user=user, is_ordered=False, order_number=order_number.group(1))
                payment = Payment(
                    user=user,
                    payment_id=order_number,
                    payment_method=data['paymentSystem'],
                    amount_paid=data['amount'],
                    status=data['transactionStatus'],
                )
                payment.save()

                order.payment = payment
                order.is_ordered = True
                order.save()
                # move the cart items to Order product table
                cart_items = CartItem.objects.filter(user=user)
                for item in cart_items:
                    orderproduct = OrderProduct()
                    orderproduct.order_id = order.id
                    orderproduct.payment = payment
                    orderproduct.user_id = user.id
                    orderproduct.product_id = item.product_id
                    orderproduct.quantity = item.quantity
                    orderproduct.product_price = item.product.price
                    orderproduct.ordered = True
                    orderproduct.save()

                    cart_item = CartItem.objects.get(id=item.id)
                    product_variations = cart_item.variations.first()
                    orderproduct = OrderProduct.objects.get(id=orderproduct.id)
                    orderproduct.variations = product_variations
                    orderproduct.save()

                    # reduce the quantity of the sold products
                    product = Product.objects.get(id=item.product_id)
                    product_variation = cart_item.variations.first()
                    product_variation.variation_stock -= item.quantity

                    if product_variation.variation_stock <= 0:
                        product_variation.is_active = False

                    product_variation.save()

                    product.main_category.count_sold += item.quantity
                    cat = MainCategory.objects.get(id=product.main_category.id)
                    cat.count_sold += item.quantity
                    cat.save()
                    product.save()

                    all_products = Product.objects.all()

                    for product in all_products:
                        variations = Variation.objects.filter(product=product)
                        total_stock = variations.aggregate(Sum('variation_stock'))['variation_stock__sum']
                        if total_stock <= 0:
                            product.is_available = False

                # clear cart
                CartItem.objects.filter(user=user).delete()

                # send order recieved email to customer
                # mail_subject = 'Thank You for your order..'
                # message = render_to_string('orders/order_recieved_email.html', {
                #     'user': user,
                # })
                # to_email = user.email
                # send_email = EmailMessage(mail_subject, message, to=[to_email])
                # send_email.send()

                return redirect('order_complete')
            else:
                return HttpResponse("Payment Fail")
        else:
            return HttpResponse("Payment Fail")
    else:
        return HttpResponseNotFound()


def place_order(request, total=0, quantity=0):
    current_user = request.user
    # if the cart count is less than  or equal to 0 , then redirect back to shop

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # store all the billing information inside order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.city = form.cleaned_data['city']
            data.post_office = form.cleaned_data['post_office']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = total
            data.ip = request.META.get('REMOTE_ADDR')  # this will give the user ip
            data.save()

            # generate the order id
            yr = int(datetime.date.today().strftime('%Y'))
            mt = int(datetime.date.today().strftime('%m'))
            dt = int(datetime.date.today().strftime('%d'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
            }
            return render(request, 'orders/payments.html', context)
    else:
        return redirect('checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)

        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        payment = Payment.objects.get(payment_id=transID)
        order_sub_total = order.order_total - order.tax
        context = {
            'order': order,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'ordered_products': ordered_products,
            'order_sub_total': order_sub_total,
        }

        return render(request, 'orders/order_complete.html', context)
    except(Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
