from decimal import Decimal
from django.db import transaction
from django.contrib.auth.models import User
from .models import Order, UserStats

def create_order(user: User, total: str | float | Decimal) -> Order:
    with transaction.atomic():
        order = Order.objects.create(user=user, total=Decimal(str(total)))
        
        stats, _ = UserStats.objects.get_or_create(user=user)
        stats.order_count += 1
        stats.total_spent += Decimal(str(total))
        stats.save()
        
    return order