from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from.models import Card

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', f"{username}@example.com")
        if User.objects.filter(username=username).exists():
            return Response({'error': 'User already exists'}, status=400)
        user = User.objects.create_user(username=username, password=password, email=email)
        Card.objects.create(user=user, card_number='4111111111111111', card_holder=username, expiry='12/28', cvv='123', credit_limit=50000, used_limit=15000)
        return Response({'message': 'User created'})

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({'access': str(refresh.access_token), 'refresh': str(refresh)})
        return Response({'error': 'Invalid credentials'}, status=401)

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        cards = Card.objects.filter(user=request.user)
        return Response({'total_cards': cards.count()})

class DashboardSummary(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        cards = Card.objects.filter(user=request.user)
        total = sum(float(c.used_limit) for c in cards)
        total_limit = sum(float(c.credit_limit) for c in cards) or 50000
        return Response({
            'total_cards': cards.count(),
            'total_balance': total,
            'total_spent': total,
            'credit_limit': total_limit,
            'credit_utilization': (total/total_limit*100) if total_limit else 0,
            'cards': [{'id': c.id, 'masked': f"****{c.card_number[-4:]}", 'limit': float(c.credit_limit), 'used': float(c.used_limit), 'blocked': c.is_blocked} for c in cards]
        })