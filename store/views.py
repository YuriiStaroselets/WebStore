from django.shortcuts import get_object_or_404, redirect, render
from cart.models import CartItem
from cart.views import _cart_id
from category.models import MainCategory, SubCategory, Category, Brand
from orders.models import OrderProduct
from store.forms import ReviewForm
from .models import Product, BestSellers, ProductGallery, ReviewRating
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages


def store(request):

    products = Product.objects.all().filter(is_available=True).order_by('product_name')

    # store pagination
    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    paged_proucts = paginator.get_page(page)

    product_count = products.count()

    bestsellers = BestSellers.objects.all().filter(is_best=True)

    main_categories = MainCategory.objects.all()
    categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()
    brand = Brand.objects.all()

    context = {
        'products': paged_proucts,
        'product_count': product_count,
        'bestsellers': bestsellers,
        'main': main_categories,
        'categories': categories,
        'sub_categories': sub_categories,
        'brands': brand
    }
    return render(request, 'store/store.html', context)


def product_detail(
        request,
        main_category_slug,
        category_slug,
        sub_category_slug,
        product_slug
):
    try:
        single_product = Product.objects.get(
            main_category__slug=main_category_slug,
            category__slug=category_slug,
            sub_category__slug=sub_category_slug,
            product_slug=product_slug
        )
        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request),
            product=single_product
        ).exists
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)
    product_gallery = ProductGallery.objects.filter(product=single_product)
    bestsellers = BestSellers.objects.all().filter(is_best=True)

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'bestsellers': bestsellers,
        'product_gallery': product_gallery,
        'orderproduct': orderproduct,
        'reviews': reviews,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword)
            )
            paginator = Paginator(products, 9)
            page = request.GET.get('page')
            paged_proucts = paginator.get_page(page)

            product_count = products.count()
        else:
            products = Product.objects.all()
            paginator = Paginator(products, 9)
            page = request.GET.get('page')
            paged_proucts = paginator.get_page(page)

            product_count = products.count()
        context = {
            'products': paged_proucts,
            'product_count': product_count,
        }

        return render(request, 'store/store.html', context)
    return redirect('store')


def filter(request):
    filter_brand = request.GET.get('brand')
    filter_main_category = request.GET.get('main_category')
    filter_category = request.GET.get('category')
    filter_sub_category = request.GET.get('sub_category')

    filter_min = request.GET.get('minimum')
    filter_max = request.GET.get('maximum')

    products = Product.objects.all().filter(is_available=True)

    if filter_brand:
        products = products.filter(brand__slug=filter_brand)
    
    if filter_main_category:
        products = products.filter(main_category__slug=filter_main_category)

    if filter_category:
        products = products.filter(category__slug=filter_category)

    if filter_sub_category:
        products = products.filter(sub_category__slug=filter_sub_category)

    if filter_min:
        products = products.filter(price__gte=filter_min)

    if filter_max:
        products = products.filter(price__lte=filter_max)

    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    main_categories = MainCategory.objects.all()
    categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()
    brand = Brand.objects.all()

    context = {
        'products': paged_products,
        'product_count': products.count(),
        'selected_brand': filter_brand,
        'selected_main_category': filter_main_category,
        'selected_category': filter_category,
        'selected_subcategory': filter_sub_category,
        'main': main_categories,
        'categories': categories,
        'sub_categories': sub_categories,
        'brands': brand,

        'selected_min': filter_min,
        'selected_max': filter_max,
    }

    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you... Your Review has been updated !')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                rating = data.ratiing
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you... Your review has been updated..')
                context = {
                    "rating": rating,

                }
                return redirect(url, context)
