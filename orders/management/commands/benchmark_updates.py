import time
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import F
from orders.models import Order, UserStats

class Command(BaseCommand):
    help = 'Benchmarks signal vs service layer approaches for Contract Specs 9 and 10'

    def handle(self, *args, **kwargs):
        User.objects.filter(username__in=['signal_user', 'service_user']).delete()
        signal_user = User.objects.create_user(username='signal_user')
        service_user = User.objects.create_user(username='service_user')

        # --- 1. Signal Simulation (N+1 Problem) ---
        start_time_signal = time.time()
        for _ in range(1000):
            Order.objects.create(user=signal_user, total=Decimal('10.00'))
            stats, _ = UserStats.objects.get_or_create(user=signal_user)
            stats.order_count += 1
            stats.total_spent += Decimal('10.00')
            stats.save()
        signal_time = time.time() - start_time_signal

        # --- 2. Optimized Service Approach ---
        start_time_service = time.time()
        
        orders = [Order(user=service_user, total=Decimal('10.00')) for _ in range(1000)]
        Order.objects.bulk_create(orders)
        
        UserStats.objects.get_or_create(user=service_user)
        UserStats.objects.filter(user=service_user).update(
            order_count=F('order_count') + 1000,
            total_spent=F('total_spent') + Decimal('10000.00')
        )
        service_time = time.time() - start_time_service

        # --- 3. Output Formatting ---
        speedup = signal_time / service_time if service_time > 0 else 0
        
        self.stdout.write(f"Signal approach time: {signal_time:.4f}s")
        self.stdout.write(f"Optimized service time: {service_time:.4f}s")
        self.stdout.write(f"Speedup factor: {speedup:.2f}x")