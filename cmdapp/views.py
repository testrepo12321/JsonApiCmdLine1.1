
from rest_framework import permissions
from cmdapp.models import todo
from cmdapp.serializers import todoSerializer
from django.contrib.auth.models import User
from cmdapp.serializers import UserSerializer
from cmdapp.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework import status
from rest_framework import serializers
from django.contrib.auth import get_user_model

##Class already exists in serializer file. ATM don't know how to fix this without removing the ability to create users via API commands.
##TODO fix double class names.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        
@api_view(['POST'])
def create_auth(request):
    VALID_USER_FIELDS = [f.name for f in get_user_model()._meta.fields]
    DEFAULTS = {
        # you can define any defaults that you would like for the user, here
    }
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        user_data = {field: data for (field, data) in request.data.items() if field in VALID_USER_FIELDS}
        user_data.update(DEFAULTS)
        user = get_user_model().objects.create_user(
            **user_data
        )
        return Response(UserSerializer(instance=user).data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'cmdapp': reverse('todo-list', request=request, format=format)
    })

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

from rest_framework.decorators import detail_route

class todoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = todo.objects.all()
    serializer_class = todoSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        todo = self.get_object()
        return Response(todo.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)