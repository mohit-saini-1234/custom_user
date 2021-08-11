from rest_framework import serializers
from Accounts.models import MyUser

class UserSerializered(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        
        fields = '__all__'
     
        def create(self, validated_data):
            return MyUser.objects.create(**validated_data)
        
        def update(self, instance, validated_data):
            instance.username = validated_data.get('username', instance.username)
            instance.email = validated_data.get('eamil', instance.email)
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.phone = validated_data.get('phone', instance.phone)
            instance.address = validated_data.get('address', instance.address)
            instance.save()
            return instance
class ChangePasswordSerializer(serializers.Serializer):
    model = MyUser

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)
    
class AssignRoleSerializer(serializers.Serializer):
    model = MyUser
    role = serializers.CharField(required=True)
    def update(self, instance, validated_data):
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance
        
        
