from rest_framework import serializers, exceptions
from .models import Experiment
from django.contrib.auth import get_user_model, authenticate

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


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def _validate_username_email(self, username, email, password):
        user = None

        if email and password:
            user = authenticate(email=email, password=password)
        elif username and password:
            user = authenticate(username=username, password=password)
        else:
            msg = _('Must include either "username" or "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        user = self._validate_username_email(username, email, password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # Is the email verified?
        email_address = user.emailaddress_set.get(email=user.email)
        if not email_address.verified:
            raise exceptions.PermissionDenied('not verified')

        attrs['user'] = user
        return attrs