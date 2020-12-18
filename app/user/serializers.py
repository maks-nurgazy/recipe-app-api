from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')

        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """serializer for user authentication object"""
    # create fields to get data for authentication
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    # override validate method and raise exception if invalid
    def validate(self, attrs):
        # attrs contains all the serializer fields defined above
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            # we use gettext to enable language tranlation for this text
            msg = _("Unable to authenticate with credentials provided")
            # pass correct code will raise the relavant http status code
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
