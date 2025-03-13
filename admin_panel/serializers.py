from rest_framework import serializers
from . import models
from users.serializers import UserSerializer

class AdminSerializer(serializers.ModelSerializer):
    # UserSerializer er field gula use korar jonno UserSerializer include korlam
    user = UserSerializer()

    class Meta:
        model = models.Admin
        fields = ['user', 'profile_picture_url', 'address', 'is_admin']
        # fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'is_staff', 'is_superuser', 'is_admin']
        read_only_fields = ['is_admin']


    def update(self, instance, validated_data):
        # pop method ta deye validated_data theke user field ke remove korlam. jehetu user ek ta nasted object.Jokhon user data thake na, tokhon None return korbe, ar error raise korbe na.
        user_data = validated_data.pop('user', None)
        # print(user_data)

        # User instance update hobe jodi user_data provide kora hoi.
        if user_data:
            user = instance.user
            # print(user)
            for key, value in user_data.items():
                print(key,value)
                setattr(user, key, value) #update user serializer er fields
            user.save()

            # admin model er field gula update kora hocca
        for key,value in validated_data.items():
            setattr(instance, key, value) # update customer serializer er fields
            # print(key,value)

        instance.save()
        return instance

 