from django.shortcuts import get_object_or_404
from recipes.models import Recipe
from users.models import Subscription


def create_object(request, pk, serializer_in, serializer_out, model):
    """Функция создания объекта."""
    user = request.user.id
    obj = get_object_or_404(model, id=pk)

    data = {'user': user, 'recipe': obj.id} if model is Recipe else {
        'user': user, 'author': obj.id}
    serializer = serializer_in(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer_out(obj, context={'request': request})


def delete_object(request, pk, model_object, model_for_delete_object):
    """Функция удаления объекта."""
    user = request.user
    obj = get_object_or_404(model_object, id=pk)

    if model_for_delete_object is Subscription:
        field = 'author'
    else:
        field = 'recipe'

    object = get_object_or_404(
        model_for_delete_object, user=user,
        **{field: obj}
    )

    object.delete()
