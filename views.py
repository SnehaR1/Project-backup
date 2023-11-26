from .models import ProductVariant  
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from userauth.models import CustomUser
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.utils import timezone
from django.db.models import Count  
from .models import Category,Brand, Product,ProductVariant,ProductImages,Color,Quantity,Order,OrderItem,Coupon
from adminapp.forms import UserEditForm,AddProduct,ProductVariantForm,ProductImagesForm,OrderItemForm,CouponForm


def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if user.is_staff:
                login(request, user)
             
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'This account does not have admin privileges.')
                return render(request, 'admin/admin_login.html')
        else:
            messages.error(request, 'Incorrect Username or Password')
            return render(request, 'admin/admin_login.html')
    return render(request, 'admin/admin_login.html')

@login_required(login_url='/admin/')
def admin_dashboard(request):
    user=request.user

    return render(request, "admin/admin_dashboard.html",{"user":user})




@login_required(login_url='/admin/')
def admin_users(request):
    users = CustomUser.objects.all()

    if request.method == 'POST':
        form = UserEditForm(request.POST)
        if form.is_valid():
            user_id_to_block = form.cleaned_data.get('user_id_to_block')
            user_to_block = get_object_or_404(CustomUser, pk=user_id_to_block)
            user_to_block.is_active = not user_to_block.is_active
            user_to_block.save()
    else:
        form = UserEditForm()

    return render(request, "admin/admin_users.html", {'users': users, 'form': form})







@user_passes_test(lambda u: u.is_superuser)  
def dlt_user(request, user_id): 
    user= get_object_or_404(CustomUser, id=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully!')
    return redirect('admin_users')

@login_required(login_url='/admin/')
def admin_category(request):
    if request.method == "POST":
        category_name = request.POST.get('category_name')
        if category_name:  
            Category.objects.create(title=category_name)
        return redirect('admin_category') 

    categories = Category.objects.annotate(product_count=Count('product_set'))
    return render(request, "admin/admin_category.html", {"categories":categories})



@user_passes_test(lambda u: u.is_superuser)
def dlt_category(request, cid):
    if request.method=="POST":
        print("Attempt to delete brand with ID:", cid)  
        category = get_object_or_404(Category,id=cid) 
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('admin_category')


@login_required(login_url='/admin/')
def admin_brand(request):
    if request.method == "POST":
        brand_name = request.POST.get('brand_name')
        if brand_name:  
            Brand.objects.create(title=brand_name)
        return redirect('admin_brand')  

    brands = Brand.objects.annotate(product_count=Count('product_set'))
    return render(request, "admin/admin_brand.html", {"brands":brands})


def dlt_brand(request, bid): 
    if request.method=="POST":
        print("Attempt to delete brand with ID:", bid)  
        brand = get_object_or_404(Brand, id=bid)
        brand.delete()
        messages.success(request, 'Brand deleted successfully!')
        return redirect('admin_brand')

@login_required(login_url='/admin/')
def admin_products(request):
    products = Product.objects.all()
    return render(request, "admin/admin_products.html", {"products": products})


@login_required(login_url='/admin/')
def add_product(request, pid=None):
    if pid:
        product = get_object_or_404(Product, pk=pid)
        operation = "Edit"
    else:
        product = Product()
        operation = "Add"

    if request.method == 'POST':
        form = AddProduct(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()

            messages.success(request, f'Product {operation}ed successfully!')
            return redirect('admin_products')
    else:
        form = AddProduct(instance=product)

    context = {
        "form": form,
        "product": product
    }

    return render(request, "admin/add_product.html", context)

@login_required(login_url='/admin/')
def admin_variant(request, pid=None):
    products = Product.objects.all()
 
    context = {
        "products": products,
       
    }
    return render(request, "admin/admin_variants.html", context)

@login_required(login_url='/admin/')
def add_variant(request):
    if request.method == 'POST':
        form = ProductVariantForm(request.POST, request.FILES)
        img_form = ProductImagesForm(request.POST, request.FILES)

        if form.is_valid() and img_form.is_valid():
            product_variant = form.save(commit=False)

            new_color_name = request.POST.get('new_color')
            if new_color_name:
                color, created = Color.objects.get_or_create(name=new_color_name)
                product_variant.color = color

            new_quantity_name = request.POST.get('new_quantity')
            if new_quantity_name:
                quantity, created = Quantity.objects.get_or_create(name=new_quantity_name)
                product_variant.quantity = quantity

            product_variant.save()

        
            images = request.FILES.getlist('images')

            for image in images:
                ProductImages.objects.create(images=image, productvariant=product_variant)

            messages.success(request, 'Product and images added successfully!')
            return redirect('admin_variant')
        else:
            messages.error(request, 'Something went wrong')
    else:
        form = ProductVariantForm()
        img_form = ProductImagesForm()

    context = {
        'form': form,
        'img_form': img_form,
    }
    return render(request, 'admin/add_variant.html', context)




@user_passes_test(lambda u: u.is_superuser)  
def dlt_product(request, product_id): 
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('admin_products')

@user_passes_test(lambda u: u.is_superuser)  
def dlt_variant(request, pv_id): 
    product_variant = get_object_or_404(ProductVariant, id=pv_id)
    product_variant.delete()
    messages.success(request, 'Product Variant deleted successfully!')
    return redirect('admin_variant')

@login_required(login_url='/admin/')
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('admin_login')


def edit_user(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)  
            user.save()
            return redirect('admin_users')
    else:
        return redirect('admin_users')
    
@login_required(login_url='/admin/')
def admin_orders(request):
    orders = Order.objects.all()
    orderitems = OrderItem.objects.all()
    productvariants=Product.objects.select_related('productvariant').all()
    return render(request, 'admin/admin_orders.html', {"orders": orders, "productvairants":productvariants,"orderitems":orderitems})


def update_status(request, order_item_id):
    # Retrieve the specific order item
    order_item = get_object_or_404(OrderItem, id=order_item_id)

    # Log a message indicating that the view is processing a specific order item
    print(f"Processing order item with ID: {order_item_id}")

    # Check if the request method is POST
    if request.method == 'POST':
        # Create an instance of the OrderItemForm for the current order item
        order_item_form = OrderItemForm(request.POST, instance=order_item)
        
        # Check if the form is valid
        if order_item_form.is_valid():
            # Retrieve the new status from the form data
            new_status = order_item_form.cleaned_data['status']
            
            # Update the delivery date if the new status is "delivered"
            if new_status == "delivered":
                order_item.delivery_date = timezone.now()
            
            # Update the status in the OrderItem model
            order_item.status = new_status
            
            # Try to save the changes to the database
            try:
                order_item.save()
                # Log a success message if the order item is saved successfully
                print(f"Order item {order_item.id} saved successfully with status {new_status}")
            except Exception as e:
                # Log an error message if there is an exception while saving
                print(f"Error saving order item {order_item.id}: {e}")
        else:
            # Log an error message if the form is not valid
            print(f"Form for order item {order_item.id} is not valid. Errors: {order_item_form.errors}")

    else:
        # If the request method is not POST, create a form for the current order item
        order_item_form = OrderItemForm(instance=order_item)

    # Prepare the context to be passed to the template
    context = {'order_item_form': order_item_form, 'order_item': order_item}
    
    # Render the 'admin/update_status.html' template with the provided context
    return render(request, 'admin/admin_orders.html', context)





def toggle_listing(request, pv_id):
    product_variant = get_object_or_404(ProductVariant, id=pv_id)

    if request.method == 'POST':
        is_listed = request.POST.get('listing_status') == 'listed'
        product_variant.is_listed = is_listed
        product_variant.save()

    return render(request, 'admin/admin_variants.html', {'product_variant': product_variant})

def unlist_category(request,category_id):
    category=get_object_or_404(Category,id=category_id)
    if request.method=="POST":
        is_listed=request.POST.get('listing_status')=='listed'
        category.is_listed=is_listed
        category.save()
        return render(request,'admin/admin_category.html',{'category':category})

def unlist_brand(request,brand_id):
    brand=get_object_or_404(Brand,id=brand_id)
    if request.method=="POST":
        is_listed=request.POST.get('listing_status')=='listed'
        brand.is_listed=is_listed
        brand.save()
        return render(request,'admin/admin_brand.html',{'brand':brand})
    
@login_required(login_url='/admin/')   
def product_listing(request,product_id):
    product=get_object_or_404(Product,id=product_id)
    if request.method=="POST":
        is_listed=request.POST.get('listing_status')=='listed'
        product.is_listed=is_listed
        product.save()
        return render(request,'admin/admin_brand.html',{'product':product})

@login_required(login_url='/admin/')
def edit_variant(request, pv_id):
    product_variant = get_object_or_404(ProductVariant, id=pv_id)

    if request.method == 'POST':
        form = ProductVariantForm(request.POST, request.FILES, instance=product_variant)
        img_form = ProductImagesForm(request.POST, request.FILES, instance=product_variant)

        if form.is_valid() and img_form.is_valid():
            product_variant = form.save(commit=False)

            new_color_name = request.POST.get('new_color')
            if new_color_name:
                color, created = Color.objects.get_or_create(name=new_color_name)
                product_variant.color = color

            new_quantity_name = request.POST.get('new_quantity')
            if new_quantity_name:
                quantity, created = Quantity.objects.get_or_create(name=new_quantity_name)
                product_variant.quantity = quantity

            product_variant.save()

            images = request.FILES.getlist('images')
            if images:
                ProductImages.objects.filter(productvariant=product_variant).delete()

            
            for image in images:
                ProductImages.objects.create(images=image, productvariant=product_variant)

            messages.success(request, 'Product variant updated successfully!')
            return redirect('admin_variant')
        else:
            messages.error(request, 'Something went wrong')
    else:
        form = ProductVariantForm(instance=product_variant)
        img_form = ProductImagesForm(instance=product_variant)

    context = {
        'form': form,
        'img_form': img_form,
        'product_variant': product_variant,
    }

    return render(request, 'admin/edit_variant.html', context)

@login_required(login_url='/admin/')
def admin_coupon(request):
    coupons=Coupon.objects.all()
    return render(request,'admin/admin_coupon.html',{'coupons':coupons})

@login_required(login_url='/admin/')
def add_coupon(request):
    if request.method == "POST":
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Coupon added Successfully!!!")
            return redirect('admin_coupon')
        else:
            error_message = "Failed to add the Coupon! Please correct the following errors: {}".format(form.errors)
            messages.error(request, error_message)
    else:
        form = CouponForm()

    return render(request, 'admin/add_coupon.html', {"form": form})