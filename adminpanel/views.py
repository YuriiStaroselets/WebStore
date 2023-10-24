from django.contrib import messages
from django.shortcuts import redirect, render
from accounts.models import Account
from cart.models import Cart, CartItem
from category.forms import MainCategoryForm, CategoryForm, SubCategoryForm, BrandForm
from category.models import MainCategory, SubCategory, Category, Brand
from orders.models import Order, OrderProduct, Payment
from store.forms import ProductForm, VariationForm
from store.models import BestSellers, Carousel, Product, ProductGallery, Variation
from home.models import Awesome
from home.forms import CarouselForm
from slugify import slugify
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncMinute
import datetime
from django.db.models import Q

from django.core.paginator import Paginator


@login_required(login_url="login")
def user_accounts_table(request, id):
    if request.user.is_superadmin:
        active_users = Account.objects.all().filter(is_admin=False, is_active=True)
        banned_users = Account.objects.all().filter(is_admin=False, is_active=False)
        context = {
            'active_users': active_users,
            'banned_users': banned_users,
        }
        if id == 1:
            return render(request, 'adminpanel/admin_accounts/active_users.html', context)
        else:
            return render(request, 'adminpanel/admin_accounts/banned_users.html', context)
    else:
        return redirect('home')


@login_required(login_url="login")
def ban_user(request, id):
    if request.user.is_superadmin:
        user = Account.objects.get(id=id)
        user.is_active = False
        user.save()
        return redirect('user_accounts_table', id=1)
    else:
        return redirect('home')


@login_required(login_url="login")
def unban_user(request, id):
    if request.user.is_superadmin:
        user = Account.objects.get(id=id)
        user.is_active = True
        user.save()
        return redirect('user_accounts_table', id=2)
    else:
        return redirect('home')


@login_required(login_url="login")
def cart_table(request, id):
    if request.user.is_superadmin:
        carts = Cart.objects.all()
        cart_items = CartItem.objects.all().filter(is_active=True)
        context = {
            'carts': carts,
            'cart_items': cart_items,
        }
        if id == 1:
            return render(request, 'adminpanel/cart_table/cart.html', context)
        else:
            return render(request, 'adminpanel/cart_table/cart_items.html', context)
    else:
        return redirect('home')


@login_required(login_url="login")
def category_table(request, id):
    if request.user.is_superadmin:
        main_category = MainCategory.objects.all()
        category = Category.objects.all()
        sub_category = SubCategory.objects.all()
        brand = Brand.objects.all()
        context = {
            'main_category': main_category,
            'category': category,
            'sub_category': sub_category,
            'brands': brand
        }
        if id == 1:
            return render(request, 'adminpanel/category_table/main_category.html', context)
        if id == 2:
            return render(request, 'adminpanel/category_table/category.html', context)
        if id == 3:
            return render(request, 'adminpanel/category_table/sub_category.html', context)
        if id == 4:
            return render(request, 'adminpanel/category_table/brand.html', context)
    else:
        return redirect('home')


# main category


@login_required(login_url="login")
def add_main_category(request):
    if request.user.is_superadmin:
        form = MainCategoryForm()
        if request.method == 'POST':
            form = MainCategoryForm(request.POST)
            if form.is_valid():
                main_category = form.save()
                main_category_name = form.cleaned_data['main_category_name']
                slug = slugify(main_category_name)
                main_category.slug = slug
                main_category.save()
                messages.success(request, 'New Main-category added successfully')
                return redirect('category_table', id=1)
        context = {
            'form': form,
        }
        return render(request, 'adminpanel/category_table/add_main_category.html', context)
    else:
        return redirect('home')


@login_required(login_url="login")
def edit_main_category(request, id):
    if request.user.is_superadmin:
        main_category = MainCategory.objects.get(id=id)
        if request.method == 'POST':
            form = MainCategoryForm(request.POST, request.FILES, instance=main_category)
            if form.is_valid():
                main_category_name = form.cleaned_data['main_category_name']
                slug = slugify(main_category_name)
                main_category = form.save()
                main_category.slug = slug
                main_category.save()
                messages.success(request, 'Main-category editted successfully')
                return redirect('category_table', id=1)
        else:
            form = MainCategoryForm(instance=main_category)
        context = {
            'form': form,
        }
        return render(request, 'adminpanel/category_table/add_main_category.html', context)
    else:
        return redirect('home')


@login_required(login_url="login")
def delete_main_category(request, id):
    if request.user.is_superadmin:
        main_category = MainCategory.objects.get(id=id)
        main_category.delete()
        return redirect('category_table', id=1)
    else:
        return redirect('home')


# main category end

# category start

@login_required(login_url="login")
def add_category(request):
    if request.user.is_superadmin:
        form = CategoryForm()
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                category = form.save()
                category_name = form.cleaned_data['category_name']
                slug = slugify(category_name)
                category.slug = slug
                category.save()
                messages.success(request, 'New category added successfully')
                return redirect('category_table', id=2)
        context = {
            'form': form,
        }
        return render(request, 'adminpanel/category_table/add_category.html', context)
    else:
        return redirect('home')


@login_required(login_url="login")
def edit_category(request, id):
    if request.user.is_superadmin:
        category = Category.objects.get(id=id)
        if request.method == 'POST':
            form = CategoryForm(request.POST, request.FILES, instance=category)
            if form.is_valid():
                category_name = form.cleaned_data['category_name']
                slug = slugify(category_name)
                category = form.save()
                category.slug = slug
                category.save()
                messages.success(request, 'category editted successfully')
                return redirect('category_table', id=2)
        else:
            form = CategoryForm(instance=category)
        context = {
            'form': form,
        }
        return render(request, 'adminpanel/category_table/add_category.html', context)
    else:
        return redirect('home')


@login_required(login_url="login")
def delete_category(request, id):
    if request.user.is_superadmin:
        category = Category.objects.get(id=id)
        category.delete()
        return redirect('category_table', id=2)
    else:
        return redirect('home')


# category end

# sub Category star

@login_required(login_url="login")
def add_sub_category(request):
    if request.user.is_superadmin:
        form = SubCategoryForm()
        if request.method == 'POST':
            form = SubCategoryForm(request.POST)
            if form.is_valid():
                sub_category = form.save()
                sub_category_name = form.cleaned_data['sub_category_name']
                slug = slugify(sub_category_name)
                sub_category.slug = slug
                sub_category.save()
                messages.success(request, 'New sub-category added successfully')
                return redirect('category_table', id=3)

        context = {
            'form': form,
        }
        return render(request, 'adminpanel/category_table/add_sub_category.html', context)
    else:
        return redirect('home')


@login_required(login_url="login")
def edit_sub_category(request, id):
    if request.user.is_superadmin:
        sub_category = SubCategory.objects.get(id=id)
        if request.method == 'POST':
            form = SubCategoryForm(request.POST, request.FILES, instance=sub_category)
            if form.is_valid():
                sub_category_name = form.cleaned_data['sub_category_name']
                slug = slugify(sub_category_name)
                sub_category = form.save()
                sub_category.slug = slug
                sub_category.save()
                messages.success(request, 'Sub-category editted successfully')
                return redirect('category_table', id=3)
        else:
            form = SubCategoryForm(instance=sub_category)
        context = {
            'form': form,
        }
        return render(request, 'adminpanel/category_table/add_sub_category.html', context)
    else:
        return redirect('home')


@login_required(login_url="login")
def delete_sub_category(request, id):
    if request.user.is_superadmin:
        sub_category = SubCategory.objects.get(id=id)
        sub_category.delete()
        return redirect('category_table', id=3)
    else:
        return redirect('home')


@login_required(login_url="login")
def add_brand(request):
    if request.user.is_superadmin:
        form = BrandForm()
        if request.method == 'POST':
            form = BrandForm(request.POST)
            if form.is_valid():
                brand = form.save()
                brand_name = form.cleaned_data['brand_name']
                slug = slugify(brand_name)
                brand.slug = slug
                brand.save()
                messages.success(request, 'New Brand added successfully')
                return redirect('category_table', id=4)
        context = {
            'form': form,
        }
        return render(request, 'adminpanel/category_table/add_brand.html', context)
    else:
        return redirect('home')


@login_required(login_url="login")
def edit_brand(request, id):
    if request.user.is_superadmin:
        brand = Brand.objects.get(id=id)
        if request.method == 'POST':
            form = BrandForm(request.POST, request.FILES, instance=brand)
            if form.is_valid():
                brand_name = form.cleaned_data['brand_name']
                slug = slugify(brand_name)
                brand = form.save()
                brand.slug = slug
                brand.save()
                messages.success(request, 'Brand editted successfully')
                return redirect('category_table', id=4)
        else:
            form = BrandForm(instance=brand)
        context = {
            'form': form,
        }
        return render(request, 'adminpanel/category_table/add_brand.html', context)
    else:
        return redirect('home')


@login_required(login_url="login")
def delete_brand(request, id):
    if request.user.is_superadmin:
        main_category = Brand.objects.get(id=id)
        main_category.delete()
        return redirect('category_table', id=4)
    else:
        return redirect('home')


@login_required(login_url="login")
def order_table(request, id):
    if request.user.is_superadmin:
        orders = Order.objects.filter(is_ordered=True, status='New')
        accepted_orders = Order.objects.filter(is_ordered=True, status='Accepted')
        completed_orders = Order.objects.filter(is_ordered=True, status="Completed")
        cancelled_orders = Order.objects.filter(is_ordered=True, status="Cancelled")
        order_products = OrderProduct.objects.all()
        payments = Payment.objects.all()
        context = {
            'orders': orders,
            'order_products': order_products,
            'payments': payments,
            'accepted_orders': accepted_orders,
            'completed_orders': completed_orders,
            'cancelled_orders': cancelled_orders,
        }

        if id == 1:
            return render(request, 'adminpanel/order_table/orders.html', context)
        elif id == 2:
            return render(request, 'adminpanel/order_table/accepted_orders.html', context)
        elif id == 3:
            return render(request, 'adminpanel/order_table/completed_orders.html', context)
        elif id == 4:
            return render(request, 'adminpanel/order_table/cancelled_orders.html', context)
        else:
            return render(request, 'adminpanel/order_table/payments.html', context)
    else:
        return redirect('home')


@login_required(login_url="login")
def order_accepted(request, order_id):
    if request.user.is_superadmin:
        order = Order.objects.get(id=order_id)
        order.status = 'Accepted'
        order.save()
        return redirect('order_table', id=1)
    else:
        return redirect('home')


@login_required(login_url="login")
def order_completed(request, order_id):
    if request.user.is_superadmin:
        order = Order.objects.get(id=order_id)
        order.status = 'Completed'
        order.save()
        return redirect('order_table', id=2)
    else:
        return redirect('home')


@login_required(login_url="login")
def order_cancelled(request, order_id):
    if request.user.is_superadmin:
        order = Order.objects.get(id=order_id)
        order.status = 'Cancelled'
        order.save()
        return redirect('order_table', id=1)
    else:
        return render(request, 'adminpanel/order_table/order_cancelled.html')


@login_required(login_url="login")
def order_items(request, order_id):
    if request.user.is_superadmin:
        order = Order.objects.get(order_number=order_id)
        order_products = OrderProduct.objects.filter(order=order)
        print(order_products)
        context = {
            'order_products': order_products,
        }
        return render(request, 'adminpanel/order_table/order_products.html', context)
    else:
        return redirect('home')


@login_required(login_url="login")
def store_table(request, id):
    if request.user.is_superadmin:
        products = Product.objects.all()
        variations = Variation.objects.all()

        context = {
            'products': products,
            'variations': variations,
        }
        if id == 1:
            return render(request, 'adminpanel/store_table/products.html', context)
        else:
            return render(request, 'adminpanel/store_table/variations.html', context)
    else:
        return redirect('home')


@login_required(login_url="login")
def add_product(request):
    if request.user.is_superadmin:
        form = ProductForm()
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product_name = form.cleaned_data['product_name']
                slug = slugify(product_name)
                product.product_slug = slug
                product.save()

                images = request.FILES.getlist('images')
                for image in images:
                    ProductGallery.objects.create(
                        image=image,
                        product=product,
                    )
                return redirect('store_table', id=1)
        else:
            form = ProductForm()
        context = {
            'form': form,
        }
        return render(request, 'adminpanel/store_table/add_product.html', context)
    else:
        return redirect('home')


@login_required(login_url="login")
def edit_product(request, id):
    if request.user.is_superadmin:
        product = Product.objects.get(id=id)
        more_images = ProductGallery.objects.filter(product=product)
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                product_name = form.cleaned_data['product_name']
                slug = slugify(product_name)
                product = form.save()
                product.product_slug = slug
                product.save()

                images = request.FILES.getlist('images')
                ProductGallery.objects.filter(product=product).delete()

                for image in images:
                    ProductGallery.objects.create(
                        image=image,
                        product=product,
                    )

                return redirect('store_table', id=1)
        else:
            form = ProductForm(instance=product)
        context = {
            'form': form,
            'more_images': more_images,

        }
        return render(request, 'adminpanel/store_table/add_product.html', context)
    else:
        return redirect('home')


@login_required(login_url="login")
def delete_product(request, id):
    if request.user.is_superadmin:
        product = Product.objects.get(id=id)
        product.delete()
        return redirect('store_table', id=1)
    else:
        return redirect('home')


@login_required(login_url="login")
def add_variations(request):
    if request.user.is_superadmin:
        form = VariationForm()
        if request.method == 'POST':
            form = VariationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('store_table', id=2)
        else:
            form = VariationForm()
        context = {
            'form': form,
        }
        return render(request, 'adminpanel/store_table/add_variations.html', context)
    else:
        return redirect('home')


@login_required(login_url="login")
def edit_variations(request, id):
    if request.user.is_superadmin:
        variation = Variation.objects.get(id=id)
        if request.method == 'POST':
            form = VariationForm(request.POST, instance=variation)
            if form.is_valid():
                form.save()
                return redirect('store_table', id=2)
        else:
            form = VariationForm(instance=variation)
        context = {
            'form': form,
        }
        return render(request, 'adminpanel/store_table/add_variations.html', context)
    else:
        return redirect('home')


@login_required(login_url="login")
def delete_variatons(request, id):
    if request.user.is_superadmin:
        variation = Variation.objects.get(id=id)
        variation.delete()
        return redirect('store_table', id=2)
    else:
        return redirect('home')


@login_required(login_url="login")
def home_table(request, id):
    if request.user.is_superadmin:
        carousels = Carousel.objects.all()
        best_sellers = BestSellers.objects.all()
        awesomes = Awesome.objects.all()

        context = {
            'carousels': carousels,
            'best_sellers': best_sellers,
            'awesomes': awesomes,
        }
        if id == 1:
            return render(request, 'adminpanel/home_table/carousel.html', context)
        elif id == 2:
            return render(request, 'adminpanel/home_table/awesomes.html', context)
        elif id == 3:
            return render(request, 'adminpanel/home_table/best_sellers.html', context)
    else:
        return redirect('home')


@login_required(login_url="login")
def add_carousels(request):
    if request.user.is_superadmin:
        form = CarouselForm()
        if request.method == 'POST':
            form = CarouselForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('home_table', id=1)
        else:
            form = CarouselForm()
        context = {
            'form': form,
        }
        return render(request, 'adminpanel/home_table/add_carousel.html', context)
    else:
        return redirect('home')


@login_required(login_url="login")
def edit_carousel(request, id):
    if request.user.is_superadmin:
        carousel = Carousel.objects.get(id=id)
        if request.method == 'POST':
            form = CarouselForm(request.POST, instance=carousel)
            if form.is_valid():
                form.save()
                return redirect('home_table', id=1)
        else:
            form = CarouselForm(instance=carousel)
        context = {
            'form': form,
        }
        return render(request, 'adminpanel/home_table/add_carousel.html', context)
    else:
        return redirect('home')


@login_required(login_url="login")
def carousel_not_available(request, id):
    if request.user.is_superadmin:
        carousel = Carousel.objects.get(id=id)
        carousel.is_available = False
        carousel.save()
        return redirect('home_table', id=1)
    else:
        return redirect('home')


@login_required(login_url="login")
def caraousel_available(request, id):
    if request.user.is_superadmin:
        carousel = Carousel.objects.get(id=id)
        carousel.is_available = True
        carousel.save()
        return redirect('home_table', id=1)
    else:
        return redirect('home')


@login_required(login_url="login")
def delete_carousel(request, id):
    if request.user.is_superadmin:
        carousel = Carousel.objects.get(id=id)
        carousel.delete()
        return redirect('home_table', id=1)
    else:
        return redirect('home')


@login_required(login_url="login")
def adminpanel(request):
    if request.user.is_superadmin:
        try:
            total_revenue = round(Order.objects.filter(is_ordered=True).aggregate(sum=Sum('order_total'))['sum'])

            chart_year = datetime.date.today().year
            chart_month = datetime.date.today().month

            # getting daily revenue
            daily_revenue = Order.objects.filter(
                created_at__year=chart_year, created_at__month=chart_month
            ).order_by('created_at').annotate(day=TruncMinute('created_at')).values('day').annotate(
                sum=Sum('order_total')).values('day', 'sum')

            day = []
            revenue = []
            for i in daily_revenue:
                day.append(i['day'].minute)
                revenue.append(int(i['sum']))

            all_main_categories = MainCategory.objects.all()

            main_categories_list = []

            for main_category in all_main_categories:
                main_category_data = {
                    'main_category_name': main_category.main_category_name,
                    'count_sold': main_category.count_sold
                }
                main_categories_list.append(main_category_data)

            product_count = OrderProduct.objects.all().count()

            context = {
                'total_revenue': total_revenue,
                'main_categories': main_categories_list,
                'product_count': product_count,
                'day': day,
                'revenue': revenue,
            }

        except:
            context = {
            }

        return render(request, 'adminpanel/adminpanel.html', context)
    else:
        return redirect('home')


def admin_search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword)
            )
            product_ids = [product.id for product in products]

            variations = Variation.objects.filter(
                product_id__in=product_ids
            ).order_by('-created_date')
            context = {
                'products': products,
                'variations': variations,
            }
    else:
        context = {
        }

    return render(request, 'adminpanel/search.html', context)
