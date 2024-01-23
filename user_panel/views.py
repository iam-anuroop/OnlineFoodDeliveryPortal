import json
import stripe
import json, urllib
from decouple import config
from ipware import get_client_ip
from django.db import transaction
from rest_framework import status
from hotel_panel.models import FoodMenu
from rest_framework.views import APIView
from django.contrib.gis.geos import Point
from hotel_panel.models import HotelsAccount
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from user_panel.serializers import UserProfileSerializer
from rest_framework.decorators import permission_classes
from django.contrib.gis.db.models.functions import Distance
from accounts.models import MyUser, UserProfile, SavedLocations
from .models import Shopping, ShoppingDeliveryPerson, ShoppingPayment
from hotel_panel.serializer import (
    HotelAccountSeriallizer,
)
from django.db.models import (
    Q,
    F,
    Sum,
    When,
    IntegerField,
    Case,
    Subquery,
    OuterRef,
)
from .serializers import (
    UserSerilaizer,
    AddressSerializer,
    AllShoppingSerializer,
    ShoppingSerializer,
    ShoppingDeliveryPersonSerializer,
    ShoppingListSerializer,
)


class UserCurrentLocation(APIView):
    @swagger_auto_schema(
        tags=["Current Location"],
        operation_description="Getting location of user using client ip",
        responses={200: "okay", 400: "errors"},
    )
    def post(self, request):
        client_ip, is_routable = get_client_ip(request)
        if is_routable:
            ip_type = "public"
        else:
            ip_type = "private"
        client_ip = "103.42.196.132"
        auth = config("FIND_IP_AUTH")
        url = "https://api.ipfind.com/?auth=" + auth + "&ip=" + client_ip
        resp = urllib.request.urlopen(url)
        data1 = json.loads(resp.read())
        data1["client_ip"] = client_ip
        data1["ip_type"] = ip_type

        if (
            Q(data1["country"])
            & Q(data1["city"])
            & Q(data1["region"])
            & Q(data1["county"])
        ):
            location = Point(data1["longitude"], data1["latitude"], srid=4326)

            if not SavedLocations.objects.filter(
                Q(country=data1["country"])
                & Q(city=data1["city"])
                & Q(state=data1["region"])
                & Q(district=data1["county"])
            ).exists():
                SavedLocations.objects.create(
                    country=data1["country"],
                    state=data1["region"],
                    district=data1["county"],
                    city=data1["city"],
                    location=location,
                )
        return Response(data1, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class ProfileManage(APIView):
    @swagger_auto_schema(
        tags=["User Profile"],
        operation_description="User profile getting",
        responses={200: UserSerilaizer, 400: "errors"},
    )
    def get(self, request):
        currentuser = request.user
        user = MyUser.objects.get(id=currentuser.id)
        serializer = UserSerilaizer(user)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["User Profile"],
        operation_description="User profile Updating",
        responses={200: UserSerilaizer, 400: "errors"},
    )
    def patch(self, request):
        user = request.user
        try:
            profile = UserProfile.objects.get(user=user)
            if profile:
                serializer = UserSerilaizer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {"data": serializer.data}, status=status.HTTP_200_OK
                    )
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"msg": "something wrong..."}, status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        tags=["User Profile"],
        operation_description="User profile Deleting",
        responses={200: "Okay", 400: "errors"},
    )
    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"msg": "Account deleted..."}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class AddToCart(APIView):
    @swagger_auto_schema(
        tags=["User Cart"],
        operation_description="User Cart Managing",
        responses={200: "Okay", 400: "errors"},
    )
    def post(self, request):
        try:
            hotel = str(request.data.get("hotel"))
            item = str(request.data.get("item"))
            count = request.data.get("count")
            cart = request.data.get("cart")
            profile = UserProfile.objects.get(user=request.user)

            if cart is not None:
                x = [{hotel: cart}]
                profile.cart = x
                profile.save()
            else:
                if profile.cart is not None:
                    try:
                        if profile.cart[0][hotel]:
                            try:
                                if profile.cart[0][hotel][0][item]:
                                    profile.cart[0][hotel][0][item] = int(
                                        profile.cart[0][hotel][0][item]
                                    ) + int(count)
                                    if int(profile.cart[0][hotel][0][item]) < 1:
                                        del profile.cart[0][hotel][0][item]
                                    if len(profile.cart[0][hotel][0]) < 1:
                                        profile.cart = None
                            except:
                                profile.cart[0][hotel][0][item] = 1
                        else:
                            if len(profile.cart[0]) > 0:
                                x = [{hotel: [{item: 1}]}]
                                profile.cart = x
                    except:
                        print("iam here")
                        x = [{hotel: [{item: 1}]}]
                        profile.cart = x
                else:
                    x = [{hotel: [{item: 1}]}]
                    profile.cart = x

            profile.save()

            return Response({"msg": "cart updated"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e, "lllll")
            return Response(
                {"msg": "error while add to cart"}, status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        tags=["User Cart"],
        operation_description="Getting details for user cart page",
        responses={200: "Okay", 400: "errors"},
    )
    def get(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile)
            if profile.cart is not None:
                cart_items = profile.cart[0][list(profile.cart[0].keys())[0]][0]
                food_item_ids = list(cart_items.keys())
                food_item_counts = list(cart_items.values())
                cart_food_items = (
                    FoodMenu.objects.filter(id__in=food_item_ids)
                    .annotate(
                        cart_item_count=Case(
                            *[
                                When(id=item_id, then=count)
                                for item_id, count in zip(
                                    food_item_ids, food_item_counts
                                )
                            ],
                            default=0,
                            output_field=IntegerField()
                        )
                    )
                    .values()
                )

                # serializer = FoodmenuSerializer(cart_food_items,many=True)
                return Response(
                    {"cart_food_items": cart_food_items, "profile": serializer.data},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"cart_food_items": [], "profile": serializer.data},
                    status=status.HTTP_200_OK,
                )
        except Exception as e:
            return Response(
                {"msg": "Something wrong"}, status=status.HTTP_400_BAD_REQUEST
            )


# stripe configuring
stripe.api_key = config("STRIPE_CLIENT_SECRET")


@permission_classes([IsAuthenticated])
class PaymentView(APIView):
    def get(self, request):
        print("blaaaaaaaah")
        print(request.user)
        profile = UserProfile.objects.get(user=request.user)
        if profile.cart is not None:
            cart_items = profile.cart[0][list(profile.cart[0].keys())[0]][0]
            food_item_ids = list(cart_items.keys())
            food_item_counts = list(cart_items.values())
            cart_food_summery = (
                FoodMenu.objects.filter(id__in=food_item_ids)
                .annotate(
                    cart_item_count=Case(
                        *[
                            When(id=item_id, then=count)
                            for item_id, count in zip(food_item_ids, food_item_counts)
                        ],
                        default=0,
                        output_field=IntegerField()
                    )
                )
                .aggregate(total_price=Sum(F("cart_item_count") * F("food_price")))
            )

            hotel_det = HotelsAccount.objects.get(id=list(profile.cart[0].keys())[0])
            serializer = HotelAccountSeriallizer(hotel_det)

            return Response(
                {"hotel": serializer.data, "total": cart_food_summery},
                status=status.HTTP_200_OK,
            )

    def post(self, request):
        profile = UserProfile.objects.get(user=request.user)
        if profile.cart is not None:
            cart_items = profile.cart[0][list(profile.cart[0].keys())[0]][0]
            food_item_ids = list(cart_items.keys())
            food_item_counts = list(cart_items.values())
            cart_food_summery = (
                FoodMenu.objects.filter(id__in=food_item_ids)
                .annotate(
                    cart_item_count=Case(
                        *[
                            When(id=item_id, then=count)
                            for item_id, count in zip(food_item_ids, food_item_counts)
                        ],
                        default=0,
                        output_field=IntegerField()
                    )
                )
                .aggregate(total_price=Sum(F("cart_item_count") * F("food_price")))
            )
            print(cart_food_summery["total_price"], "kkkkkkkkkkkk")

            data = stripe.Product.create(
                name="Total amount",
                default_price_data={
                    "unit_amount": int(cart_food_summery["total_price"] * 100),
                    "currency": "inr",
                },
                expand=["default_price"],
            )

            customer = stripe.Customer.create(
                email=request.user.email, phone=request.user.phone
            )

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price": data["default_price"]["id"],
                        "quantity": 1,
                    },
                ],
                mode="payment",
                customer=customer.id,
                success_url="http://localhost:5173"
                + "/success/?success=true&session_id={CHECKOUT_SESSION_ID}",
                cancel_url="http://localhost:5173" + "/canceled/?canceled=true",
            )

            location = request.GET.get("address")
            address = request.GET.get("address")
            profile = UserProfile.objects.get(user=request.user)
            if address == "home":
                location = profile.address_loc
                address = profile.user_address
            if address == "office":
                location = profile.office_loc
                address = profile.office_address

            food = FoodMenu.objects.filter(id=food_item_ids[0]).first()
            hotel_loc = food.hotel.location

            shopping_payment = ShoppingPayment.objects.create(
                stripe_id=checkout_session.id,
                total_amount=cart_food_summery["total_price"],
                del_location=location,
                address=address,
                hotel_loc=hotel_loc,
            )

            with transaction.atomic():
                for item_id, count in zip(food_item_ids, food_item_counts):
                    food_item = FoodMenu.objects.get(id=item_id)
                    # total_amount = food_item.food_price * count
                    print("1")
                    Shopping.objects.create(
                        user=request.user,
                        item=food_item,
                        payment_id=shopping_payment,
                        quantity=count,
                    )
            return Response({"url": checkout_session.url}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(
                {"msg": "somthing went wrong on stripe"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@permission_classes([IsAuthenticated])
class PaymentSuccessView(APIView):
    def post(self, request):
        session_id = request.GET.get("session_id")
        payment_instance = ShoppingPayment.objects.get(stripe_id=session_id)
        payment_instance.status = "success"
        payment_instance.is_completed = True
        payment_instance.save()

        return Response({"msg": "Completed Success fully"}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class AddressManage(APIView):
    def post(self, request):
        params = request.GET.get("address")

        serializer = AddressSerializer(data=request.data)

        if serializer.is_valid():
            profile = UserProfile.objects.get(user=request.user)
            address = serializer.validated_data.get("address")
            coords = serializer.validated_data.get("coords")
            location = Point(coords[1], coords[0])

            if params == "home":
                profile.user_address = address
                profile.address_loc = location

            if params == "office":
                profile.office_address = address
                profile.office_loc = location

            profile.save()
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class AllOrdersOfUser(APIView):
    def get(self, request):
        user = request.user

        shoppings = ShoppingPayment.objects.filter(shopping__user=user).distinct()

        shoppings = shoppings.annotate(
            hotel_name=Subquery(
                Shopping.objects.filter(payment_id=OuterRef("pk"))
                .order_by("date")
                .values("item__hotel__hotel_name")[:1]
            ),
            hotel_image=Subquery(
                Shopping.objects.filter(payment_id=OuterRef("pk"))
                .order_by("date")
                .values("item__hotel__profile_photo")[:1]
            ),
        )

        serializer = ShoppingListSerializer(shoppings, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class OrderDetails(APIView):
    def get(self, request):
        try:
            pay_id = request.GET.get("pay_id")
            payment = ShoppingPayment.objects.get(id=pay_id)
            order_det = Shopping.objects.filter(payment_id=pay_id)
            delivery_det = ShoppingDeliveryPerson.objects.get(
                shopping_payment__id=pay_id
            )
            deliverySerializer = ShoppingDeliveryPersonSerializer(delivery_det)
            paymentSerializer = AllShoppingSerializer(payment)
            orderSerializer = ShoppingSerializer(order_det, many=True)
            return Response(
                {
                    "payment": paymentSerializer.data,
                    "orders": orderSerializer.data,
                    "delivery": deliverySerializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"msg": e}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class OrderTrackingUpdation(APIView):
    def get(self, request):
        pay_id = request.GET.get("pay_id")
        delivery_det = ShoppingDeliveryPerson.objects.get(shopping_payment__id=pay_id)
        shopping = Shopping.objects.filter(payment_id=pay_id).first()
        hotel_location = shopping.item.hotel.location
        total_dist = (
            ShoppingPayment.objects.filter(id=pay_id)
            .annotate(
                distance_to_delivery_person=Distance("del_location", hotel_location)
            )
            .values("distance_to_delivery_person")
            .first()
        )

        delivery_person_location = (
            UserProfile.objects.filter(user=delivery_det.delivery_person.user)
            .values("location")
            .first()
        )
        if delivery_person_location:
            delivery_person_point = delivery_person_location["location"]

            current_dist = (
                ShoppingPayment.objects.filter(id=pay_id)
                .annotate(
                    distance_total=Distance("del_location", delivery_person_point)
                )
                .values("distance_total")
                .first()
            )

            distance_percentage = (
                current_dist["distance_total"]
                / total_dist["distance_to_delivery_person"]
                * 100
            )
            distance_percentage = 80
            if distance_percentage < 100:
                delivery_det.status = "ordered"
            if distance_percentage < 100 and distance_percentage > 70:
                delivery_det.status = "purchasing"
            if distance_percentage < 70:
                delivery_det.status = "on_the_way"
            delivery_det.save()

            serializer = ShoppingDeliveryPersonSerializer(delivery_det)

            return Response(serializer.data)
        else:
            return Response(
                {"error": "Delivery person location not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# Create your views here.
