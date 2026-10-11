from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib.auth.models import User
from.models import Card, Transaction
from django.db.models import Sum
import csv

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({"error": "Username password required da!"}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({"error": "User exists da!"}, status=400)
    User.objects.create_user(username=username, password=password)
    return Response({"message": "User created da!"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    cards = Card.objects.filter(user=request.user)
    total_cards = cards.count()
    total_used = sum([float(c.used_limit) for c in cards])
    total_limit = sum([float(c.credit_limit) for c in cards]) or 1
    utilization = (total_used / total_limit * 100) if total_limit > 0 else 0
    return Response({
        "total_cards": total_cards,
        "total_balance": total_used,
        "total_limit": total_limit,
        "credit_utilization": utilization,
        "cards": [{
            "id": str(c.id),
            "masked": f"**** **** **** {c.card_number[-4:]}",
            "limit": float(c.credit_limit),
            "used": float(c.used_limit),
            "blocked": c.is_blocked
        } for c in cards]
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def card_list(request):
    cards = Card.objects.filter(user=request.user)
    return Response([{
        "id": str(c.id),
        "masked": f"**** **** **** {c.card_number[-4:]}",
        "limit": float(c.credit_limit),
        "used": float(c.used_limit),
        "blocked": c.is_blocked
    } for c in cards])

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transaction_create(request):
    card_id = request.data.get('card_id') or request.data.get('card')
    amount = request.data.get('amount')
    merchant = request.data.get('merchant', 'Test Payment')
    if not card_id or not amount:
        return Response({"error": "card_id and amount required da!"}, status=400)
    try:
        amount = float(amount)
        if amount <= 0:
            return Response({"error": "Amount positive ah irukanum da!"}, status=400)
    except:
        return Response({"error": "Invalid amount da!"}, status=400)
    try:
        card = Card.objects.get(id=card_id, user=request.user)
    except Card.DoesNotExist:
        return Response({"error": "Card not found da!"}, status=404)
    if card.is_blocked:
        return Response({"error": "Card blocked da!"}, status=400)
    if float(card.used_limit) + amount > float(card.credit_limit):
        return Response({"error": f"Limit exceeded da! Available: {float(card.credit_limit)-float(card.used_limit)}"}, status=400)
    fraud_status = 'FLAGGED' if amount > 40000 else 'SAFE'
    fraud_reason = f'High amount: {amount}' if amount > 40000 else ''
    txn = Transaction.objects.create(
        user=request.user, card=card, card_last4=card.card_number[-4:],
        amount=amount, merchant=merchant, status='SUCCESS',
        fraud_status=fraud_status, fraud_reason=fraud_reason
    )
    card.used_limit = float(card.used_limit) + amount
    card.save()
    return Response({
        "id": str(txn.id), "amount": float(txn.amount), "merchant": txn.merchant,
        "status": txn.status, "fraud_status": txn.fraud_status, "message": "Payment successful da! 🎉"
    }, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_list(request):
    txns = Transaction.objects.filter(user=request.user).order_by('-date')[:50]
    return Response([{
        "id": str(t.id), "card": f"**** {t.card_last4}", "card_last4": t.card_last4,
        "amount": float(t.amount), "merchant": t.merchant, "status": t.status,
        "fraud_status": t.fraud_status, "date": t.date.strftime("%Y-%m-%d %H:%M")
    } for t in txns])

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_search(request):
    txns = Transaction.objects.filter(user=request.user).order_by('-date')
    min_amt = request.GET.get('min_amount')
    max_amt = request.GET.get('max_amount')
    status_filter = request.GET.get('status')
    if min_amt:
        try: txns = txns.filter(amount__gte=float(min_amt))
        except: pass
    if max_amt:
        try: txns = txns.filter(amount__lte=float(max_amt))
        except: pass
    if status_filter:
        txns = txns.filter(fraud_status=status_filter)
    return Response({
        "results": [{
            "id": str(t.id), "card": f"**** {t.card_last4}", "card_last4": t.card_last4,
            "amount": float(t.amount), "merchant": t.merchant,
            "fraud_status": t.fraud_status, "date": t.date.strftime("%Y-%m-%d %H:%M")
        } for t in txns[:100]]
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analytics_view(request):
    txns = Transaction.objects.filter(user=request.user)
    cards = Card.objects.filter(user=request.user)
    total_spent = txns.aggregate(Sum('amount'))['amount__sum'] or 0
    total_limit = sum([float(c.credit_limit) for c in cards]) or 1
    total_used = sum([float(c.used_limit) for c in cards])
    utilization = (total_used / total_limit * 100) if total_limit > 0 else 0
    merchant_data = txns.values('merchant').annotate(total=Sum('amount')).order_by('-total')[:6]
    category_wise = [{"category": m['merchant'], "total": float(m['total'])} for m in merchant_data]
    if not category_wise:
        category_wise = [{"category": "No Transactions", "total": 1}]
    monthly = []
    for i in range(1, 7):
        month_total = txns.filter(date__month=i).aggregate(Sum('amount'))['amount__sum'] or 0
        monthly.append({"month": i, "total": float(month_total)})
    return Response({
        "total_spent": float(total_spent),
        "credit_utilization": utilization,
        "category_wise": category_wise,
        "monthly_spending": monthly
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analytics_export(request):
    format_type = request.GET.get('format', 'csv')
    txns = Transaction.objects.filter(user=request.user).order_by('-date')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="transactions.{format_type}"'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Card', 'Merchant', 'Amount', 'Status'])
    for t in txns:
        writer.writerow([t.date.strftime("%Y-%m-%d %H:%M"), t.card_last4, t.merchant, t.amount, t.fraud_status])
    return response