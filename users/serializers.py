from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField
from .models import *


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    url = HyperlinkedIdentityField(view_name='user-detail', lookup_field='pk')

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'phone', 'national_id', 'is_superuser', 'is_moderator', 'password',
                  'password2', 'url', 'is_root']

    def validate(self, data):
        if 'password' in data and 'password2' in data:
            if data['password'] != data['password2']:
                raise serializers.ValidationError(
                    {'password': 'passwords do not match', 'password2': 'passwords do not match'})

        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        password2 = validated_data.pop('password2')
        is_superuser = validated_data.pop('is_superuser', False)

        user = super().create(validated_data)

        if is_superuser:
            user.is_superuser = is_superuser
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        password2 = validated_data.pop('password2', None)
        user = super().update(instance, validated_data)

        user.set_password(password)
        user.save()
        return user


class NationalitySerializer(serializers.ModelSerializer):
    url = HyperlinkedIdentityField(view_name='nationality-detail', lookup_field='pk')

    class Meta:
        model = Nationality
        fields = '__all__'


class MaritalStatusSerializer(serializers.ModelSerializer):
    url = HyperlinkedIdentityField(view_name='marital-status-detail', lookup_field='pk')

    class Meta:
        model = MaritalStatus
        fields = '__all__'


class EmployeeTypeSerializer(serializers.ModelSerializer):
    url = HyperlinkedIdentityField(view_name='employee-type-detail', lookup_field='pk')

    class Meta:
        model = EmployeeType
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    url = HyperlinkedIdentityField(view_name='city-detail', lookup_field='pk')

    class Meta:
        model = City
        fields = '__all__'


class CityDistrictReadSerializer(serializers.ModelSerializer):
    url = HyperlinkedIdentityField(view_name='city-district-detail', lookup_field='pk')
    city = CitySerializer(read_only=True)

    class Meta:
        model = CityDistrict
        fields = '__all__'


class CityDistrictWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityDistrict
        fields = '__all__'


class EmployeeReadSerializer(serializers.ModelSerializer):
    nationality = NationalitySerializer()
    marital_status = MaritalStatusSerializer()
    city = CitySerializer()
    district = CityDistrictReadSerializer()
    added_by = UserSerializer()
    emp_type = EmployeeTypeSerializer()
    url = HyperlinkedIdentityField(view_name='employee-detail', lookup_field='pk')

    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

    def create(self, validated_data):
        employee = super().create(validated_data)
        user = self.context['request'].user
        employee.added_by = user
        employee.save()
        return employee


class ModeratorWriteSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Moderator
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data["name"] = validated_data.get('employee').name
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        moderator = Moderator.objects.create(user=user, **validated_data)
        return moderator

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        instance.save()
        return instance


class ModeratorReadSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    employee = EmployeeReadSerializer()
    url = HyperlinkedIdentityField(view_name='moderator-detail', lookup_field='pk')

    class Meta:
        model = Moderator
        fields = '__all__'
