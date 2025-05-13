from rest_framework import serializers
from .models import Restaurant, SliderItem, MenuCategory, MenuItem, Order, OrderItem
from goby.utils import get_translated_field


class RestaurantReadSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='restaurant-detail')
    total_orders = serializers.IntegerField(read_only=True)
    rating = serializers.FloatField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    categories = serializers.SerializerMethodField(read_only=True)
    merchant_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Restaurant
        fields = ["id", "url", "name", "image", "cover", "description", "total_orders", "rating", "categories",
                  "merchant_type"]

    def get_name(self, obj: Restaurant):
        return get_translated_field(self.context["request"], obj.name_ar, obj.name_en)

    def get_description(self, obj: Restaurant):
        return get_translated_field(self.context["request"], obj.description_ar, obj.description_en)

    def get_categories(self, obj: Restaurant):
        categories = MenuCategoryReadSerializer(obj.categories, many=True, context=self.context).data
        return [{"id": category["id"], "name": category["name"]} for category in categories]

    def get_merchant_type(self, obj: Restaurant):
        types = {"grocery": "بقالة", "hand-made": "انتاج منزلي", "restaurant": "مطعم"}
        if self.context["request"].lang == "en":
            return obj.merchant_type
        return types[obj.merchant_type]


class RestaurantWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class SliderItemReadSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='slider-detail')
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = SliderItem
        fields = ['id', "url", 'title', 'description', 'image', 'link', 'url']

    def get_title(self, obj: SliderItem):
        return get_translated_field(self.context["request"], obj.title_ar, obj.title_en)

    def get_description(self, obj: SliderItem):
        return get_translated_field(self.context["request"], obj.description_ar, obj.description_en)


class SliderItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SliderItem
        fields = '__all__'


class MenuCategoryReadSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = MenuCategory
        fields = ["id", "name", "image"]

    def get_name(self, obj: MenuCategory):
        return get_translated_field(self.context["request"], obj.name_ar, obj.name_en)


class MenuCategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = '__all__'


class MenuItemBaseSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    def get_name(self, obj):
        return get_translated_field(self.context.get("request"), obj.name_ar, obj.name_en)

    def get_description(self, obj):
        return get_translated_field(self.context.get("request"), obj.description_ar, obj.description_en)

    def get_category(self, obj: MenuItem) -> dict:
        category = MenuCategoryReadSerializer(obj.category, context=self.context).data
        return {"id": category["id"], "name": category["name"]}


class MenuItemReadSerializer(MenuItemBaseSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='menu-item-detail')
    restaurant = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = ["id", "url", "name", "description", "category", "restaurant", "image", "price"]

    def get_restaurant(self, obj: MenuItem):
        restaurant = RestaurantReadSerializer(obj.restaurant, context=self.context).data
        return {"id": restaurant["id"], "name": restaurant["name"]}


class MenuItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class MenuItemInlineSerializer(MenuItemBaseSerializer):
    class Meta:
        model = MenuItem
        fields = ["id", "name", "description", "image", "price"]


class OrderItemReadSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='order-item-detail')
    menu_item = serializers.SerializerMethodField(read_only=True)
    price = serializers.DecimalField(source='menu_item.price', max_digits=10, decimal_places=2, read_only=True)
    total = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'url', 'menu_item', 'price', 'quantity', 'total']

    def get_total(self, obj):
        return obj.get_total()

    def get_menu_item(self, obj: OrderItem):
        return {"id": obj.menu_item.id,
                "name": get_translated_field(self.context["request"], obj.menu_item.name_ar, obj.menu_item.name_en)}


class OrderItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity']


class OrderReadSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='order-detail')
    client = serializers.SerializerMethodField()
    restaurant = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    items = OrderItemReadSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'url', 'client', 'restaurant', 'total_amount', 'total_price', 'status',
                  'created_at', 'address', 'items']

    def get_client_name(self, obj: Order):
        return obj.client.name

    def get_client(self, obj: Order):
        return {"id": obj.client.id, "name": obj.client.name}

    def get_restaurant(self, obj: Order):
        return {"id": obj.restaurant.id,
                "name": get_translated_field(self.context["request"], obj.restaurant.name_ar, obj.restaurant.name_en)}

    def get_status(self, obj: Order):
        status_labels = {
            'pending': {'en': 'Pending', 'ar': 'قيد الانتظار'},
            'preparing': {'en': 'Preparing', 'ar': 'قيد التحضير'},
            'delivering': {'en': 'Delivering', 'ar': 'قيد التوصيل'},
            'completed': {'en': 'Completed', 'ar': 'مكتمل'},
            'cancelled': {'en': 'Cancelled', 'ar': 'أُلغي'},
        }
        request = self.context.get('request')

        return status_labels[obj.status][request.lang]

    def get_total_amount(self, obj: Order):
        return obj.total_amount()

    def get_total_price(self, obj: Order):
        return obj.total_price()


class OrderWriteSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='order-detail')
    items = OrderItemWriteSerializer(many=True)
    total_price = serializers.SerializerMethodField(read_only=True)
    total_amount = serializers.SerializerMethodField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    restaurant_name = serializers.CharField(source='restaurant.name_ar', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'url', 'restaurant', 'restaurant_name', 'created_at',
            'address', 'status', 'status_display', 'items',
            'total_price', 'total_amount'
        ]
        read_only_fields = ['created_at', 'total_price', 'total_amount', 'status_display']

    def validate_items(self, value):
        if not value or len(value) == 0:
            raise serializers.ValidationError("Order cannot be empty.")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        client = self.context["request"].user

        # Ensure client exists
        if not client:
            raise serializers.ValidationError({"client": "Client does not exist."})

        address = validated_data.get("address")
        if not address or address.strip() == "":
            address = client.address
            if not address or address.strip() == "":
                raise serializers.ValidationError({"address": "No address provided and client has no address."})
            validated_data["address"] = address

        # Create order
        order = Order.objects.create(client=client, **validated_data)

        # Create order items
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order

    def get_total_price(self, obj):
        return obj.total_price()

    def get_total_amount(self, obj):
        return obj.total_amount()

    def update(self, instance, validated_data):
        client = self.context["request"].user
        if instance.client != client:
            raise serializers.ValidationError("Unauthorized")
        super(OrderWriteSerializer, self).update(instance, validated_data)
        return instance
