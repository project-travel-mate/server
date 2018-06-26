from rest_framework import serializers
from api.models import City, CityImage, CityFact


class CitySerializer(serializers.ModelSerializer):
    facts_count = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ('id', 'city_name', 'description', 'latitude', 'longitude', 'image', 'facts_count')

    def get_facts_count(self, obj):
        return obj.facts.count()


class CityImageSerializer(serializers.ModelSerializer):
    city_id = serializers.RelatedField(source='city.city_id', read_only=True)

    class Meta:
        model = CityImage
        fields = ('id', 'city_id', 'image_url')


class CityFactSerializer(serializers.ModelSerializer):
    city_id = serializers.RelatedField(source='city.city_id', read_only=True)

    class Meta:
        model = CityFact
        fields = ('id', 'city_id', 'fact', 'source_text', 'source_url')
