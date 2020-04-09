from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.modules.city.model import City, CityImage


@api_view(['POST'])
@permission_classes([IsAdminUser, ])
def add_city_image(request):
    """
    Add image URL to a city
    :param request:
    :return: 400 Invalid City ID or Incorrect Image URL
    :return: 200 successful
    """
    city_id = request.POST.get('city_id', None)
    image_url = request.POST.get('image_url', None)

    url_validator = URLValidator()

    if not city_id or not image_url:
        # incorrect request received
        error_message = "Missing parameters in request. Send city_id, image_url"
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    try:
        url_validator(image_url)
        city = City.objects.get(pk=city_id)
        city_image = CityImage(city=city, image_url=image_url)
        city_image.save()
    except ValidationError as e:
        # e is a list of error messages
        error_message = "\n".join(e)
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error_message = str(e)
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    success_message = "Successfully added new city image."
    return Response(success_message, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAdminUser, ])
def remove_city_image(request, image_id):
    """
    Removes City Image URL from a city
    :param request:
    :param image_id:
    :return: 404 if invalid city image ID is sent
    :return: 200 successful
    """
    try:
        city_image = CityImage.objects.get(pk=image_id)
        city_image.delete()
    except CityImage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    message = "City Image successfully deleted."
    return Response(message, status=status.HTTP_200_OK)
