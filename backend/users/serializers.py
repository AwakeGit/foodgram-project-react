# from django.contrib.auth import get_user_model
# from rest_framework import serializers
# from rest_framework.validators import UniqueValidator
#
# from users.models import Subscription
# from recipes.serializers import RecipeInfoSerializer
#
# User = get_user_model()
#
#
# class UserSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(
#         max_length=150,
#         validators=(UniqueValidator(queryset=User.objects.all()),)
#     )
#     email = serializers.EmailField(
#         max_length=50,
#         validators=(UniqueValidator(queryset=User.objects.all()),)
#     )
#     is_subscribed = serializers.SerializerMethodField()
#
#     class Meta:
#         model = User
#         fields = ('id', 'email', 'username', 'first_name',
#                   'last_name', 'is_subscribed')
#
#     def get_is_subscribed(self, obj):
#         if self.context.get('request').user.is_authenticated:
#             user = self.context.get('request').user
#             return Subscription.objects.filter(user=user,
#                                                following=obj).exists()
#         return False
#
#
# class SubscribeResponseSerializer(serializers.ModelSerializer):
#     recipes_count = serializers.SerializerMethodField()
#     recipes = serializers.SerializerMethodField()
#     is_subscribed = serializers.SerializerMethodField()
#
#     class Meta:
#         model = User
#         fields = ('email', 'id', 'username', 'first_name',
#                   'last_name', 'is_subscribed', 'recipes', 'recipes_count')
#
#     def get_recipes_count(self, obj):
#         return obj.recipes.count()
#
#     def get_recipes(self, obj):
#         request = self.context.get('request')
#         recipes_limit = request.query_params.get('recipes_limit')
#         recipes = obj.recipes.all()
#         if recipes_limit:
#             recipes = obj.recipes.order_by('id')[:int(recipes_limit)]
#         return RecipeInfoSerializer(recipes, many=True).data
#
#     def get_is_subscribed(self, obj):
#         if self.context.get('request').user.is_authenticated:
#             user = self.context.get('request').user
#             return Subscription.objects.filter(user=user,
#                                                following=obj).exists()
#         return False
