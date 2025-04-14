from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers import UserSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated, AllowAny

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self,request, *args, **kwargs):
        try:
            user_data = request.data
            is_cpf_valid = User.objects.filter(cpf=user_data['cpf']).exists()
            is_email_valid = User.objects.filter(email=user_data['email']).exists()
            if is_cpf_valid:
                return Response({'error': 'CPF already exists'}, status=status.HTTP_409_CONFLICT)
            if is_email_valid:
                return Response({'error': 'Email already exists'}, status=status.HTTP_409_CONFLICT)
            serializer = self.get_serializer(data=user_data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response({'error': f'Missing required field: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            role = self._verify_user_role(user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'user_role': role,
            }, status=status.HTTP_200_OK)

        except KeyError as e:
            return Response({'error': f'Missing required field: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except AuthenticationFailed as e:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _verify_user_role(self, user):
        if user.is_student:
            return 'student'
        elif user.is_teacher:
            return 'teacher'
        elif user.is_manager:
            return 'manager'
        return None

class LogoutView(generics.GenericAPIView):

    def get_serializer_class(self):
        return None

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response("Logout com sucesso.", status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail" : str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RefreshView(generics.GenericAPIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            return Response({
                'access': str(token.access_token),
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail" : str(e)}, status=status.HTTP_400_BAD_REQUEST)


class VerifyRoleView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        required_role = request.data.get('role')
        
        if not required_role:
            return Response(
                {"detail": "Role parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        
        has_access = False
        
        if required_role == 'student':
            has_access = user.is_student or user.is_teacher or user.is_manager
            
        elif required_role == 'teacher':
            has_access = user.is_teacher or user.is_manager
            
        elif required_role == 'manager':
            has_access = user.is_manager
            
        else:
            return Response(
                {"detail": "Invalid role specified"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not has_access:
            return Response(
                {"detail": f"You don't have {required_role} privileges"},
                status=status.HTTP_403_FORBIDDEN
            )

        return Response(
            {
                "detail": "Permission granted",
                "user_id": user.id,
                "require_role": required_role,
                "actual_role": self._get_user_role(user)
            },
            status=status.HTTP_200_OK
        )
    
    def _get_user_role(self, user):
        if user.is_manager:
            return 'manager'
        elif user.is_teacher:
            return 'teacher'
        elif user.is_student:
            return 'student'
        return 'unknown'

class VerifyTokenView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        if not token:
            auth_header = request.headers.get('Authorization')
            if auth_header:
                token = auth_header.split(' ')[-1]
        
        if not token:
            return Response(
                {"detail": "Token is required either in body (token) or header (Authorization)"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = User.objects.get(id=user_id)

            return Response(
                {
                    "detail": "Token is valid",
                    "user_id": user.id,
                    "email": user.email,
                    "is_student": user.is_student,
                    "is_teacher": user.is_teacher,
                    "is_manager": user.is_manager
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )