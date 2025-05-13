from delivery.models import Delivery
from delivery.permissions import IsApprovedDeliveryMan
from delivery.serializers import CreditsSerializer, DeliverySerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from users.models import User
from .models import Credits, Order
# from django.shortcuts import get_object_or_404


class DeliveryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def take_order(self, request):
        """
        Allows an authenticated and approved delivery man to take an order.
        Expects 'order_id', 'latitude', and 'longitude' in the request data.
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
        except ValueError:
            return Response(
                {"error": "Latitude and longitude must be valid numbers."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            order = Order.objects.get(pk=order_id)
            client = order.client
            credits = Credits.objects.get(owner=user)

            if order.total_amount() > credits.amount:
                return Response(
                    {
                        "error": f"Insufficient credits.  Order amount is {order.total_amount()}, and you have {credits.amount} credits."
                    },
                    status=status.HTTP_402_PAYMENT_REQUIRED,
                )

            import uuid

            ## just a uuid that I can use to identify each delivery request -> can be a code or some hash depends how they want it

            tracking_id = str(uuid.uuid4())[:8].upper()

            delivery = Delivery.objects.create(
                tracking_id=tracking_id,
                delivery_man=user,
                order=order,
                client=client,
                latitude=latitude,
                longitude=longitude,
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
        data = {
            "tracking_id": delivery.tracking_id,
            "delivery_man": delivery.delivery_man.id,  # Or serializer if needed
            "delivery_man_name": delivery.delivery_man.username,
            "client": delivery.client.id,  # Or serializer
            "client_name": delivery.client.username,
            "order": delivery.order.id,  # Or serializer
            # Add more order details if required
            "latitude": delivery.current_latitude,
            "longitude": delivery.current_longitude,
            "updated_at": delivery.updated_at,
        }
        return Response(data)

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
        permission_classes=[IsApprovedDeliveryMan],
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

        if latitude is not None and longitude is not None:
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
        else:
            return Response(
                {"error": "Please provide both 'latitude' and 'longitude'."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CreditsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CreditsSerializer
    permission_classes = [IsApprovedDeliveryMan]

    def get_queryset(self):
        return Credits.objects.filter(owner=self.request.user)

    # this is just a generic view it should be pointing to the stripe endpoints to actually make a transaction here
    @action(detail=False, methods=["post"], url_path="buy_credits")
    def buy_credits(self, request):
        """
        Allows an authenticated user to buy credits (simulated cause you don't have nothign now).
        Expects 'amount' in the request data.
        Will need to know what other stuff that will come from whatever provider that they use
        """
        amount = request.data.get("amount")
        if not amount:
            return Response(
                {"error": "Please provide the 'amount' to buy."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            amount = float(amount)
            ## Or maybe it should return 0 with the error
            if amount <= 0:
                return Response(
                    {"error": "Amount must be a positive value."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ValueError:
            return Response(
                {"error": "Invalid amount."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            credits = Credits.objects.get(owner=request.user)
            credits.amount += amount
            credits.save()
            serializer = self.get_serializer(credits)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"An error occurred while funding credits: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    ## this shouldn't be here but I won't be reading like 12k lines of code not today or ever.
    @action(
        detail=False,
        methods=["post"],
        url_path="admin/adjust",
        permission_classes=[IsApprovedDeliveryMan],
    )  # Adjust permissions as needed
    def admin_adjust_credits(self, request):
        """
        Allows an admin to adjust the credits of a specific user.
        Expects 'user_id', 'amount', and 'type' ('increment' or 'decrement') in the request data.
        """
        ## can then be extended to normal users not only delivery
        user_id = request.data.get("user_id")
        amount = request.data.get("amount")
        ## expects you to give me -> ["increment", "decrement"]
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
            user_to_adjust = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": f"User with id {user_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            amount = float(amount)
            if amount <= 0:
                return Response(
                    {"error": "Amount must be a positive value for adjustment."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ValueError:
            return Response(
                {"error": "Invalid amount."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            credits = Credits.objects.get(owner=user_to_adjust, defaults={"amount": 0})
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
