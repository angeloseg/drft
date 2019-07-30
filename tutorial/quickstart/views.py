from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from tutorial.quickstart.serializer import UserSerializer, GroupSerializer, UsersNameOnlySerializer
from tutorial.quickstart.tasks import conf_email


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('date_joined')
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # async mail task (edw tha mpei to call toy task pou tha ftiaksw gia na stelnei ta e-mail sto
        # creation tou user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            conf_email.delay(serializer.validated_data.get('email'))
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=201, headers=headers)
        return Response(serializer.errors)

    @action(methods=['get'], detail=False, url_path='usernames-only', serializer_class=UsersNameOnlySerializer)
    def usernames_only(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


