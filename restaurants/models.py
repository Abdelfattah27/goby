from django.db import models


class MenuCategory(models.Model):
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="images/categories/")

    def __str__(self):
        return f"{self.name_ar}"


class Restaurant(models.Model):
    MERCHANT_CHOICES = (
        ("restaurant", "Restaurant"),
        ("hand-made", "Hand-Made"),
        ("grocery", "Grocery"),
    )

    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="images/restaurants/images", null=True)
    cover = models.ImageField(upload_to="images/restaurants/covers", null=True)
    description_ar = models.TextField(blank=True, null=True)
    description_en = models.TextField(blank=True, null=True)
    total_orders = models.IntegerField(default=0)
    rating = models.FloatField(default=0)
    categories = models.ManyToManyField(
        MenuCategory, related_name="restaurants", blank=True
    )
    merchant_type = models.CharField(
        max_length=100, default="restaurant", choices=MERCHANT_CHOICES
    )

    def __str__(self):
        return self.name_ar


# models.py
class SliderItem(models.Model):
    title_ar = models.CharField(max_length=100, blank=True, null=True)
    title_en = models.CharField(max_length=100, blank=True, null=True)
    description_ar = models.TextField(blank=True, null=True)
    description_en = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="images/sliders/")
    link = models.URLField(
        blank=True, null=True, help_text="Optional link or deep link"
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title_ar or f"Slider #{self.pk}"


class MenuItem(models.Model):
    category = models.ForeignKey(
        MenuCategory, on_delete=models.CASCADE, related_name="items"
    )
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="items"
    )
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100, blank=True, null=True)
    description_ar = models.TextField(blank=True, null=True)
    description_en = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to="images/menu_items/", blank=True, null=True)

    def __str__(self):
        return f"{self.name_ar} - {self.price} EGP"


class Order(models.Model):
    restaurant = models.ForeignKey(
        "Restaurant", on_delete=models.CASCADE, related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(
        "clients.Client", on_delete=models.CASCADE, related_name="orders"
    )
    address = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("preparing", "Preparing"),
            ("delivering", "Delivering"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        default="pending",
    )

    def __str__(self):
        return f"Order #{self.pk} - {self.restaurant.name_ar}"

    ## this is bad for transactions it should be returning as a float
    def total_price(self):
        return sum(item.get_total() for item in self.items.all())

    ## this should be called something diffrent this is so confusingggg
    def total_amount(self):
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey("MenuItem", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total(self):
        return self.menu_item.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name_ar} for Order #{self.order_id}"
