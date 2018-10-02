from rest_framework import serializers
from .models import Experiment


class ExperimentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Experiment
        fields = ("author",
                  "content",
                  "created",
        )

    def create(self, validated_data):
        """
        Create and return a new `Experiment` instance, given the validated data.
        """
        return Experiment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Experiment` instance, given the validated data.
        """
        instance.author = validated_data.get('author', instance.author)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)

        instance.save()
        return instance