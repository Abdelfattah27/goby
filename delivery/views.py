from clients.models import Client
from delivery.models import Delivery
from delivery.permissions import IsApprovedDeliveryMan
from delivery.serializers import CreditsSerializer, DeliverySerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Credits, Order
from decimal import Decimal
import uuid


class DeliveryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

    @action(
        detail=True,
        methods=["patch"],
        permission_classes=[IsAuthenticated, IsApprovedDeliveryMan],
        url_path="arrive-at-restaurant",
    )
    def arrive_at_restaurant(self, request, pk=None):
        """
        Allows an authenticated and approved delivery man to mark arrival at the restaurant.
        Expects 'latitude' and 'longitude' in the request data.
        Updates Delivery location and sets order status to 'delivering'.
        """
        delivery = self.get_object()
        if delivery.delivery_man != request.user:
            return Response(
                {"error": "You are not authorized to update this delivery."},
                status=status.HTTP_403_FORBIDDEN,
            )

        order = delivery.order
        if order.status != "taken":
            return Response(
                {"error": f"Order status is '{order.status}', expected 'taken'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")
        if latitude is None or longitude is None:
            return Response(
                {"error": "Please provide both 'latitude' and 'longitude'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            latitude = float(latitude)
            longitude = float(longitude)
            if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
                return Response(
                    {"error": "Invalid latitude or longitude values."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ValueError:
            return Response(
                {"error": "Latitude and longitude must be valid numbers."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        delivery.current_latitude = latitude
        delivery.current_longitude = longitude
        order.status = "delivering"
        delivery.save()
        order.save()

        serializer = self.get_serializer(delivery)
        return Response(
            {
                "message": "Arrived at restaurant.",
                "delivery": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["patch"],
        permission_classes=[IsAuthenticated, IsApprovedDeliveryMan],
        url_path="mark-delivered",
    )
    def mark_delivered(self, request, pk=None):
        """
        Allows an authenticated and approved delivery man to mark the order as delivered.
        Updates the order status to 'delivered'.
        """
        delivery = self.get_object()
        if delivery.delivery_man != request.user:
            return Response(
                {"error": "You are not authorized to update this delivery."},
                status=status.HTTP_403_FORBIDDEN,
            )

        order = delivery.order
        if order.status != "delivering":
            return Response(
                {"error": f"Order status is '{order.status}', expected 'delivering'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order.status = "delivered"
        order.save()

        serializer = self.get_serializer(delivery)
        return Response(
            {
                "message": "Order marked as delivered.",
                "delivery": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated, IsApprovedDeliveryMan],
    )
    def take_order(self, request):
        """
        Allows an authenticated and approved delivery man to take an order.
        Expects 'order_id', 'latitude', and 'longitude' in the request data.
        Sets order status to 'taken'.
        """
        user = request.user
        order_id = request.data.get("order_id")
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")

        if not order_id or latitude is None or longitude is None:
            return Response(
                {"error": "Please provide 'order_id', 'latitude', and 'longitude'"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            latitude = float(latitude)
            longitude = float(longitude)
            if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
                return Response(
                    {"error": "Invalid latitude or longitude values."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ValueError:
            return Response(
                {"error": "Latitude and longitude must be valid numbers."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            order = Order.objects.get(pk=order_id)
            client = order.client
            if order.status not in ["pending", "preparing"]:
                return Response(
                    {"error": "This order is not available for delivery."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            credits, created = Credits.objects.get_or_create(
                owner=user, defaults={"amount": 0}
            )
            if order.total_amount() > credits.amount:
                return Response(
                    {
                        "error": f"Insufficient credits. Order amount is {order.total_amount()}, and you have {credits.amount} credits."
                    },
                    status=status.HTTP_402_PAYMENT_REQUIRED,
                )

            tracking_id = str(uuid.uuid4())[:8].upper()
            order.status = "taken"
            order.save()

            delivery = Delivery.objects.create(
                tracking_id=tracking_id,
                delivery_man=user,
                order=order,
                client=client,
                current_latitude=latitude,
                current_longitude=longitude,
            )
            serializer = self.get_serializer(delivery)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Order.DoesNotExist:
            return Response(
                {"error": f"Order with id {order_id} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["get"])
    def details(self, request, pk=None):
        """
        Retrieves detailed information about a specific delivery.
        """
        delivery = self.get_object()
        serializer = self.get_serializer(delivery)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="location")
    def location(self, request, pk=None):
        """
        Retrieves the current location of a specific delivery.
        """
        delivery = self.get_object()
        return Response(
            {
                "tracking_id": delivery.tracking_id,
                "latitude": delivery.current_latitude,
                "longitude": delivery.current_longitude,
                "updated_at": delivery.updated_at,
            }
        )

    @action(
        detail=True,
        methods=["patch"],
        url_path="update-location",
        permission_classes=[IsAuthenticated, IsApprovedDeliveryMan],
    )
    def update_location(self, request, pk=None):
        """
        Allows an authenticated delivery man to update the location of a delivery.
        Expects 'latitude' and 'longitude' in the request data.
        """
        delivery = self.get_object()
        if delivery.delivery_man != request.user:
            return Response(
                {"error": "You are not authorized to update this delivery's location."},
                status=status.HTTP_403_FORBIDDEN,
            )

        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")
        if latitude is None or longitude is None:
            return Response(
                {"error": "Please provide both 'latitude' and 'longitude'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            latitude = float(latitude)
            longitude = float(longitude)
            if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
                return Response(
                    {"error": "Invalid latitude or longitude values."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ValueError:
            return Response(
                {"error": "Latitude and longitude must be valid numbers."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        delivery.current_latitude = latitude
        delivery.current_longitude = longitude
        delivery.save()
        return Response(
            {
                "tracking_id": delivery.tracking_id,
                "latitude": delivery.current_latitude,
                "longitude": delivery.current_longitude,
                "updated_at": delivery.updated_at,
            }
        )


class CreditsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CreditsSerializer
    permission_classes = [IsApprovedDeliveryMan]

    def get_queryset(self):
        return Credits.objects.filter(owner=self.request.user)

    @action(detail=False, methods=["post"], url_path="buy_credits")
    def buy_credits(self, request):
        """
        Allows an authenticated user to buy credits (simulated).
        Expects 'amount' in the request data.
        """
        amount = request.data.get("amount")
        if not amount:
            return Response(
                {"error": "Please provide the 'amount' to buy."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            amount = Decimal(str(amount))
            if amount <= 0 or amount > 1000000:
                return Response(
                    {"error": "Amount must be positive and less than 1,000,000."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ValueError:
            return Response(
                {"error": "Invalid amount."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            credits, created = Credits.objects.get_or_create(
                owner=request.user, defaults={"amount": 0}
            )
            credits.amount += amount
            credits.save()
            serializer = self.get_serializer(credits)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"An error occurred while funding credits: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(
        detail=False,
        methods=["post"],
        url_path="admin/adjust",
        permission_classes=[IsAdminUser],
    )
    def admin_adjust_credits(self, request):
        """
        Allows an admin to adjust the credits of a specific user.
        Expects 'user_id', 'amount', and 'type' ('increment' or 'decrement') in the request data.
        """
        user_id = request.data.get("user_id")
        amount = request.data.get("amount")
        adjustment_type = request.data.get("type")
        if (
            not user_id
            or amount is None
            or adjustment_type not in ["increment", "decrement"]
        ):
            return Response(
                {
                    "error": "Please provide 'user_id', 'amount', and 'type' ('increment' or 'decrement')."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_to_adjust = Client.objects.get(pk=user_id)
        except Client.DoesNotExist:
            return Response(
                {"error": f"User with id {user_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            amount = Decimal(str(amount))
            if amount <= 0 or amount > 1000000:
                return Response(
                    {"error": "Amount must be positive and less than 1,000,000."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ValueError:
            return Response(
                {"error": "Invalid amount."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            credits, created = Credits.objects.get_or_create(
                owner=user_to_adjust, defaults={"amount": 0}
            )
            if adjustment_type == "increment":
                credits.amount += amount
            elif adjustment_type == "decrement":
                if credits.amount >= amount:
                    credits.amount -= amount
                else:
                    return Response(
                        {"error": "Insufficient credits to decrement."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            credits.save()
            serializer = self.get_serializer(credits)
            return Response(
                {
                    "message": f"Credits adjusted successfully for user {user_id}.",
                    "credits": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred while adjusting credits: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
