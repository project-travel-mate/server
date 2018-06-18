from rest_framework import serializers
from api.modules.city.model import City, CityImage, CityFact


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'city_name', 'description', 'latitude', 'longitude', 'image')


class CityAutocompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'city_name')


class CityImageSerializer(serializers.ModelSerializer):
    city_id = serializers.RelatedField(source='city.city_id', read_only=True)

    class Meta:
        model = CityImage
        fields = ('id', 'city_id', 'image_url')


class CityFactSerializer(serializers.ModelSerializer):
    city_id = serializers.RelatedField(source='city.city_id', read_only=True)

    class Meta:
        model = CityFact
        fields = ('id', 'city_id', 'fact')
