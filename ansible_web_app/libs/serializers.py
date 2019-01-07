from rest_framework import serializers
from ansible_web_app.models import Group, IP


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "group_name")


class IPSerializer(serializers.ModelSerializer):
    class Meta:
        model = IP
        fields = ("id", "ip_address", "group")
