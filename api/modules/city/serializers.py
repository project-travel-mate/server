from rest_framework import serializers
from api.models import City, CityImage, CityFact, CityVisitLog


class AllCitiesSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    facts_count = serializers.SerializerMethodField()
    visit_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = City
        fields = ('id', 'city_name', 'facts_count', 'image', 'visit_count')

    def get_image(self, obj):
        if obj.images.count() == 0:
            return None
        return obj.images.first().image_url

    def get_facts_count(self, obj):
        return obj.facts.count()


class CitySerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    facts_count = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ('id', 'city_name', 'description', 'latitude', 'longitude', 'facts_count', 'images')

    def get_images(self, obj):
        if obj.images.count() == 0:
            return []
        return [x.image_url for x in obj.images.all()]

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


class CityVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityVisitLog
        fields = ['city', 'visit_count']

