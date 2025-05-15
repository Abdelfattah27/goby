from django.db.models import Q
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter

import rest_framework.custom_pagination
from authentication.client_auth import ClientJWTAuthentication
from goby.utils import get_translated_field
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .models import Restaurant, SliderItem, MenuItem, MenuCategory, Order, OrderItem
from .serializers import (
    RestaurantReadSerializer,
    RestaurantWriteSerializer,
    SliderItemReadSerializer,
    SliderItemWriteSerializer,
    MenuItemInlineSerializer,
    MenuItemWriteSerializer,
    MenuItemReadSerializer,
    MenuCategoryWriteSerializer,
    MenuCategoryReadSerializer,
    OrderWriteSerializer,
    OrderReadSerializer,
    OrderItemWriteSerializer,
    OrderItemReadSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="List all restaurants",
        description="Retrieve a list of restaurants with optional filters.",
        parameters=[
            OpenApiParameter(
                name="name", type=str, description="Filter by name or description"
            ),
            OpenApiParameter(
                name="recently", type=bool, description="Sort by newest first"
            ),
            OpenApiParameter(
                name="best_sellers",
                type=bool,
                description="Sort by highest total_orders",
            ),
        ],
        responses={200: RestaurantReadSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve a specific restaurant",
        responses={200: RestaurantReadSerializer},
    ),
    create=extend_schema(
        summary="Create a new restaurant",
        request=RestaurantWriteSerializer,
        responses={201: RestaurantReadSerializer},
    ),
    update=extend_schema(
        summary="Update an existing restaurant",
        request=RestaurantWriteSerializer,
        responses={200: RestaurantReadSerializer},
    ),
    partial_update=extend_schema(
        summary="Partially update a restaurant",
        request=RestaurantWriteSerializer,
        responses={200: RestaurantReadSerializer},
    ),
    destroy=extend_schema(summary="Delete a restaurant", responses={204: None}),
)
class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return RestaurantWriteSerializer
        return RestaurantReadSerializer

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get("name")
        recently = self.request.query_params.get("recently")
        best_sellers = self.request.query_params.get("best_sellers")
        merchant_type = self.request.query_params.get("merchant-type")

        if merchant_type is not None:
            queryset = queryset.filter(merchant_type=merchant_type)

        if recently and recently.lower() == "true":
            queryset = queryset.order_by("-id")

        if best_sellers and best_sellers.lower() == "true":
            queryset = queryset.order_by("-total_orders")

        if name:
            queryset = queryset.filter(
                Q(name__icontains=name) | Q(description__icontains=name)
            )

        return queryset

    @action(methods=["GET"], detail=True)
    def detailed(self, request, pk=None):
        restaurant = self.get_object()
        serialized = self.get_serializer(restaurant)

        categories = []
        for category in restaurant.categories.all():
            items = restaurant.items.filter(category=category)
            categories.append(
                {
                    "id": category.id,
                    "name": get_translated_field(
                        request, category.name_ar, category.name_en
                    ),
                    "items": MenuItemInlineSerializer(
                        items, many=True, context={"request": request}
                    ).data,
                }
            )

        response = {**serialized.data, "categories": categories}
        return Response(
            response,
        )


class SliderItemViewSet(ModelViewSet):
    queryset = SliderItem.objects.order_by("order")
    pagination_class = rest_framework.custom_pagination.NoPagination

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return SliderItemWriteSerializer
        return SliderItemReadSerializer

    def get_queryset(self):
        queryset = self.queryset
        active = self.request.query_params.get("active")

        if active is not None and active.lower() == "true":
            queryset = queryset.filter(is_active=True)

        return queryset


class MenuCategoryViewSet(ModelViewSet):
    queryset = MenuCategory.objects.all()
    pagination_class = rest_framework.custom_pagination.NoPagination

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return MenuCategoryWriteSerializer
        return MenuCategoryReadSerializer

    @action(methods=["GET"], detail=True)
    def detailed(self, request, pk=None):
        category: MenuCategory = MenuCategory.objects.filter(pk=pk).first()
        if not category:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serialized_category = self.get_serializer(category)
        restaurants = category.restaurants.all()
        serialized_restaurants = RestaurantReadSerializer(
            restaurants, many=True, context={"request": request}
        )
        return Response(
            {**serialized_category.data, "restaurants": serialized_restaurants.data}
        )


class MenuItemViewSet(ModelViewSet):
    queryset = MenuItem.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return MenuItemWriteSerializer
        return MenuItemReadSerializer

    def get_queryset(self):
        category = self.request.query_params.get("category")
        if category:
            return self.queryset.filter(category__id=category)

        return self.queryset


## this should work, no ?
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    authentication_classes = [ClientJWTAuthentication]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return OrderWriteSerializer
        return OrderReadSerializer

    def get_queryset(self):
        client = self.request.user
        return self.queryset.filter(client=client).order_by("-id")


class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    authentication_classes = [ClientJWTAuthentication]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return OrderItemWriteSerializer
        return OrderItemReadSerializer

    def get_queryset(self):
        client = self.request.user
        return self.queryset.filter(order__client=client).order_by("-id")
