from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from ..repository import MemberRepository, AuthTokenRepository


class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        member = MemberRepository.get_by_username(username)
        if not member or not member.check_password(password):
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        token = AuthTokenRepository.create_token(member.id)
        
        return Response({
            'token': token.token,
            'user_id': member.id,
            'username': member.username,
            'is_staff': member.is_staff
        })

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        phone_number = request.data.get('phone_number', '')
        
        if not username or not password:
            return Response(
                {'error': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        existing_member = MemberRepository.get_by_username(username)
        if existing_member:
            return Response(
                {'error': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            member = MemberRepository.create(username, password, phone_number, is_staff=False)
            token = AuthTokenRepository.create_token(member.id)
            
            return Response({
                'token': token.token,
                'user_id': member.id,
                'username': member.username,
                'is_staff': member.is_staff
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class LogoutView(APIView):
    def post(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('Token '):
            return Response(
                {'error': 'Token not provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        token_str = auth_header.replace('Token ', '')
        success = AuthTokenRepository.delete_token(token_str)
        
        if success:
            return Response({'message': 'Successfully logged out'})
        else:
            return Response(
                {'error': 'Logout failed'},
                status=status.HTTP_400_BAD_REQUEST
            )