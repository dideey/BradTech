from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.decorators import action

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch', 'post', 'delete']

    def get_object(self):
        """overides the get_object method to return the profile of the user making the request
           Ensuring that a user can only view and edit their own profile
        """
        try:
            return self.queryset.get(user=self.request.user)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['put'], url_path='update-profile')
    def update_profile(self, request):
        """Overides the update_profile method to allow updates without explicitly specifying the profile id
        """
        user = request.user
        profile = Profile.objects.get(user=user)
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['patch'], url_path='partial-update-profile')
    def partial_update_profile(self, request):
        """Overides the partial_update_profile method to allow partial updates without explicitly specifying the profile id
        """
        user = request.user
        profile = Profile.objects.get(user=user)
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['delete'], url_path='delete-account')
    def delete_profile(self, request):
        """Overides the delete_profile method to allow deletion without explicitly specifying the profile id
        """
        user = request.user
        profile = Profile.objects.get(user=user)
        user.delete()
        return Response("Account deleted!!!", status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['post'], url_path='change-password')
    def update_password(self, request):
        """Endpoint to allow users to change their password
        """
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if not user.check_password(old_password):
            return Response({'old_password': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_password(new_password)
        except ValidationError as e:
            return Response({'new_password': list(e.messages)}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response("Password updated successfully", status=status.HTTP_200_OK)


    def get_queryset(self):
        # Only return the profile of the user making the request
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        #Set user to the current user making the request
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        #Ensure the user field is set to the current user making the request
        serializer.save(user=self.request.user)

class LeadersViewSet(viewsets.ModelViewSet):
    queryset = Leaders.objects.all()
    serializer_class = LeadersSerializer
    lookup_field = 'id'
    
    def get_permissions(self):
        """Set the right permissions for the different actions
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]
    
    @action(detail=False, methods=['get'], url_path='governors')
    def list_governors(self, request):
        """Endpoint to get all governors
        """
        queryset = Leaders.objects.filter(position='governor')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='senators')
    def list_senators(self, request):
        """Endpoint to get all senators
        """
        queryset = Leaders.objects.filter(position='senator')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='women-reps')
    def list_women_reps(self, request):
        """Endpoint to get all women-reps"""
        queryset = Leaders.objects.filter(position='women rep')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='mps')
    def list_mps(self, request):
        """Endpoint to get all mps
        """
        queryset = Leaders.objects.filter(position='mp')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='mca')
    def list_mca(self, request):
        """Endpoint to get all mca
        """
        queryset = Leaders.objects.filter(position='mca')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='search')
    def search_leaders(self, request):
        """Custom action to search for leaders based on their name
        """
        name = request.query_params.get('name')
            
        if not name:
            return Response({"error": "Name query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = Leaders.objects.filter(name__icontains=name)
        
        if not queryset.exists():
            return Response({"error": "No leaders found with the given name."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)  


class CountyView(APIView):
    """ county view
    """
    def get(self, request):
        queryset = County.objects.all()
        serializer = CountySerializer(queryset, many=True)
        return Response(serializer.data)

class ConstituencyView(APIView):
    """ constituency views
    """
    def get(self, request):
        queryset = Constituency.objects.all()
        serializer = ConstituencySerializer(queryset, many=True)
        return Response(serializer.data)


class WardView(APIView):
    """ ward view
    """
    def get(self, request):
        queryset = Ward.objects.all()
        serializer = WardSerializer(queryset, many=True)
        return Response(serializer.data)
   
class PostViewSet(viewsets.ModelViewSet):
    """ post viewset
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Overides the create method to save the post with the author set to the current user making the request
        """
        post_data = request.data
        post_serializer = self.get_serializer(data=post_data)
        post_serializer.is_valid(raise_exception=True)

        # Extract leader_id from URL parameters
        leader_id = self.kwargs.get('leader_id')
        if not leader_id:
            return Response({'error': 'Leader ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            leader = Leaders.objects.get(id=leader_id)
        except Leaders.DoesNotExist:
            return Response({'error': 'Leader not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Save the post with author set to the current user making the request and leader set to the leader in the URL parameters
        post = post_serializer.save(author=self.request.user, leader=leader)   

        # Save the post contents
        output_serializer = self.get_serializer(post)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Overrides the update method to ensure that a user can only update their own posts
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.author != request.user:
            return Response({'error': 'You are not allowed to update this post'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        """Overrides the partial_update method to ensure that a user can only update their own posts
        """
        kwargs['partial'] = True
        instance = self.get_object()

        if instance.author != request.user:
            return Response({'error': 'You are not allowed to update this post'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """Overrides the destroy method to ensure that a user can only delete their own posts or an admin can delete any post
        """
        instance = self.get_object()

        if instance.author != request.user and not request.user.is_staff:
            return Response({'error': 'You are not allowed to delete this post'}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response("Post deleted", status=status.HTTP_204_NO_CONTENT)

class PostCommentViewSet(viewsets.ModelViewSet):
    queryset = PostComment.objects.all()
    serializer_class = PostCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        #Set author to the current user making the request and the post to the post in the request data
        post_id = self.kwargs.get('post_pk')
        print(post_id)
        if post_id is None:
            raise NotFound("Post ID is required")
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise NotFound(f"Post with id {post_id} does not exist")
        serializer.save(author=self.request.user, post=post)

    def destroy(self, request, *args, **kwargs):
        """Overrides the destroy method to ensure that a user can only delete their own comments or an admin can delete any comment
        """
        instance = self.get_object()

        if instance.author != request.user and not request.user.is_staff:
            return Response({'error': 'You are not allowed to delete this comment'}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response("Comment deleted", status=status.HTTP_204_NO_CONTENT)
        

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """performs custom validation on the password field
        """
        password = serializer.validated_data.get('password')
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        serializer.save()

    def create(self, request, *args, **kwargs):
        """overides the create method to return a custom response
        """
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "message": "User signed up successfully",
                "user": response.data
            },
            status=status.HTTP_201_CREATED
        )

    
class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

class Logout(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    def post(self, request, *args, **kwargs):
        """ Endpoint to logout a user by blacklisting the refresh token
        """
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response('Sucessfuly logged out, see you soon!', status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
