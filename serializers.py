from rest_framework import serializers

# Example serializer class
class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = None  # Specify your model here
        fields = '__all__'  # Specify fields to include or exclude
