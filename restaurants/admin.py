from django.contrib import admin
from django.utils.html import format_html
from .models import (MenuCategory, Restaurant, SliderItem, 
                    MenuItem, Order, OrderItem)


from goby.admin import  CustomModelAdmin

@admin.register(MenuCategory)
class MenuCategoryAdmin(CustomModelAdmin):
    list_display = ('name_ar', 'name_en', 'image_preview')
    search_fields = ('name_ar', 'name_en')
    list_per_page = 20

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />'.format(obj.image.url))
        return "-"
    image_preview.short_description = 'Image'
    
from django.contrib.admin import SimpleListFilter
class RestaurantFilter(SimpleListFilter):
    title = 'restaurant'
    parameter_name = 'restaurant'

    def lookups(self, request, model_admin):
        
        if hasattr(request , "user") and  request.user.is_superuser:
            restaurants = [(r.id, r.name_ar) for r in Restaurant.objects.all()]
            return restaurants
        
        elif hasattr(request , "user") and hasattr(request.user , "restaurant" ) : 
            res =  request.user.restaurant
            return [(res.id, res.name_ar) ]
        return []

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(restaurant_id=self.value())
        return queryset
    
from django import forms
# Custom Form for Restaurant
# 
            
@admin.register(Restaurant)
class RestaurantAdmin(CustomModelAdmin):
    list_display = ('id', 'status', 'client', 'created_at', 'total_price_display')
    list_filter = (RestaurantFilter, 'merchant_type', 'rating')
    readonly_fields = ( 'total_price_display' , "total_orders" , "image_preview" , "cover_preview")
    actions = ['mark_as_completed', 'mark_as_preparing']
    list_display = ('name_ar', 'merchant_type', 'rating', 'total_orders', 'image_preview', 'cover_preview')
    search_fields = ('name_ar', 'name_en')
    filter_horizontal = ('categories',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request, "user") and request.user.is_restaurant:
            return qs.filter(user=request.user)
        return qs
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name_ar', 'name_en', 'merchant_type')
        }),
        ('Content', {
            'fields': ('description_ar', 'description_en')
        }),
        ('Media', {
            'fields': ('image', 'image_preview', 'cover', 'cover_preview')
        }),
        ('Statistics', {
            'fields': ('rating', 'total_orders')
        }),
        ('Categories', {
            'fields': ('categories',)
        }),
    )
    
    def get_status_choices(self, request):
        if request.user.is_superuser:
            return [
                ("pending", "Pending"),
                ("preparing", "Preparing"),
                ("taken", "Taken"),
                ("delivering", "Delivering"),
                ("completed", "Completed"),
                ("cancelled", "Cancelled"),
            ]
        return [
            ("pending", "Pending"),
            ("preparing", "Preparing"),
            ("taken", "Taken"),
            ("cancelled", "Cancelled"),
        ]
        
    def get_form(self, request, obj=None, **kwargs):
        print("get form")
        form = super().get_form(request, obj, **kwargs)
        
        # Modify status choices based on user type
        if not request.user.is_superuser and 'status' in form.base_fields:
            form.base_fields['status'].choices = [
                ("pending", "Pending"),
                ("preparing", "Preparing"),
                ("taken", "Taken"),
                ("cancelled", "Cancelled"),
            ]
        return form
    
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        print("get ther")
        if db_field.name == "status":
            kwargs['choices'] = self.get_status_choices(request)
        return super().formfield_for_choice_field(db_field, request, **kwargs)
    def get_fieldsets(self, request, obj = None): 
        if request.user.is_superuser : 
            return [
                *self.fieldsets, 
                ('User', {
                    'fields': ('user',)
                }),
            ]
        
        return super().get_fieldsets(request, obj)
    
    def get_readonly_fields(self, request, obj = None): 
        if request.user.is_restaurant :
            return (*self.readonly_fields, 'rating') 
  
        return super().get_readonly_fields(request, obj)
    list_per_page = 20

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />'.format(obj.image.url))
        return "-"
    image_preview.short_description = 'Logo'

    def cover_preview(self, obj):
        if obj.cover:
            return format_html('<img src="{}" width="100" height="50" style="object-fit: cover;" />'.format(obj.cover.url))
        return "-"
    cover_preview.short_description = 'Cover'
    
    def total_price_display(self, obj):
        return f"{obj.total_price()} EGP"
    total_price_display.short_description = 'Total Price'

    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_as_completed.short_description = "Mark as completed"

    def mark_as_preparing(self, request, queryset):
        queryset.update(status='preparing')
    mark_as_preparing.short_description = "Mark as preparing"
        

@admin.register(SliderItem)
class SliderItemAdmin(CustomModelAdmin):
    list_display = ('title_ar', 'is_active', 'order', 'image_preview', 'created_at')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title_ar', 'title_en')
    readonly_fields = ('created_at', 'image_preview')
    fieldsets = (
        ('Content', {
            'fields': ('title_ar', 'title_en', 'description_ar', 'description_en')
        }),
        ('Media & Link', {
            'fields': ('image', 'image_preview', 'link')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
        ('Date', {
            'fields': ('created_at',)
        }),
    )
    list_per_page = 20

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="50" style="object-fit: cover;" />'.format(obj.image.url))
        return "-"
    image_preview.short_description = 'Preview'

@admin.register(MenuItem)
class MenuItemAdmin(CustomModelAdmin):
    list_display = ('name_ar', 'restaurant', 'category', 'price', 'image_preview')
    list_filter = (RestaurantFilter, 'category')
    search_fields = ('name_ar', 'name_en')
    readonly_fields = ('image_preview',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_restaurant:
            return qs.filter(restaurant=request.user.restaurant)
        return qs
    
    def get_readonly_fields(self, request, obj = None ):
        if request.user.is_restaurant:
            return (*self.readonly_fields, 'restaurant')
        return super().get_readonly_fields(request, obj)

    # def get_exclude(self, request, obj=None):
    #     if request.user.is_restaurant:
    #         return ['restaurant']
    #     return []
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('restaurant', 'category')
        }),
        ('Content', {
            'fields': ('name_ar', 'name_en', 'description_ar', 'description_en')
        }),
        ('Pricing', {
            'fields': ('price',)
        }),
        ('Media', {
            'fields': ('image', 'image_preview')
        }),
    )
    list_per_page = 20

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />'.format(obj.image.url))
        return "-"
    image_preview.short_description = 'Image'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('get_total',)
    fields = ('menu_item', 'quantity', 'get_total')
    
    def get_total(self, instance):
        return instance.get_total()
    get_total.short_description = 'Total'

@admin.register(Order)
class OrderAdmin(CustomModelAdmin):
    list_display = ('id', 'restaurant', 'client', 'status', 'created_at', 'total_price', 'total_items')
    list_filter = ('status', 'restaurant', 'created_at')
    search_fields = ('id', 'client__name', 'restaurant__name_ar')
    readonly_fields = ('created_at', 'total_price', 'total_items', 'map_preview')
    inlines = [OrderItemInline]
    
    def get_status_choices(self, request):
        if request.user.is_superuser:
            return [
                ("pending", "Pending"),
                ("preparing", "Preparing"),
                ("taken", "Taken"),
                ("delivering", "Delivering"),
                ("completed", "Completed"),
                ("cancelled", "Cancelled"),
            ]
        return [
            ("pending", "Pending"),
            ("preparing", "Preparing"),
            ("taken", "Taken"),
            ("cancelled", "Cancelled"),
        ]

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "status":
            kwargs['choices'] = self.get_status_choices(request)
        return super().formfield_for_choice_field(db_field, request, **kwargs)
    
    def get_readonly_fields(self, request, obj = None): 
        if request.user.is_restaurant:
            return (*self.readonly_fields, 'restaurant', 'client')
        return super().get_readonly_fields(request, obj)
    fieldsets = (
        ('Order Information', {
            'fields': ('restaurant', 'client', 'status')
        }),
        ('Delivery Information', {
            'fields': ('address_current', 'address_latitude', 'address_longitude', 'map_preview')
        }),
        ('Totals', {
            'fields': ('total_price', 'total_items')
        }),
        ('Date', {
            'fields': ('created_at',)
        }),
    )
    list_per_page = 20

    def total_price(self, obj):
        return f"{obj.total_price()} EGP"
    total_price.short_description = 'Total Price'

    def total_items(self, obj):
        return obj.total_amount()
    total_items.short_description = 'Total Items'

    def map_preview(self, obj):
        if obj.address_latitude and obj.address_longitude:
            return format_html(
                '<iframe width="300" height="200" frameborder="0" style="border:0" '
                'src="https://www.google.com/maps/embed/v1/view?key={#TODO}&center={},{}&zoom=15" '
                'allowfullscreen></iframe>',
                obj.address_latitude,
                obj.address_longitude
            )
        return "No location data"
    map_preview.short_description = 'Map Preview'

@admin.register(OrderItem)
class OrderItemAdmin(CustomModelAdmin):
    list_display = ('id', 'order', 'menu_item', 'quantity', 'get_total')
    list_filter = ('order__restaurant',)
    search_fields = ('order__id', 'menu_item__name_ar')
    readonly_fields = ('get_total',)
    list_per_page = 20

    def get_total(self, obj):
        return f"{obj.get_total()} EGP"
    get_total.short_description = 'Total'