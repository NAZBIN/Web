from rest_framework import serializers
from .forms import User

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid','telephone','username','email','is_active','is_staff')