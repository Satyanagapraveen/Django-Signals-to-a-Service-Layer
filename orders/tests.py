from django.test import TestCase
from django.contrib.auth.models import User
from orders.models import Order, UserStats

class SignalBypassTest(TestCase):
    def test_bulk_update_bypasses_signal(self):
        user1 = User.objects.create_user(username='user1', password='pw')
        user2 = User.objects.create_user(username='user2', password='pw')
        
        Order.objects.create(user=user1, total=50.00)
        Order.objects.create(user=user1, total=50.00)
        
        stats1 = UserStats.objects.get(user=user1)
        self.assertEqual(stats1.order_count, 2)
        self.assertEqual(stats1.total_spent, 100.00)
        
        Order.objects.create(user=user1, total=10.00)
        
        bulk_orders = [
            Order(user=user2, total=20.00),
            Order(user=user2, total=30.00)
        ]
        Order.objects.bulk_create(bulk_orders)
        
        Order.objects.filter(user=user2).update(user=user1)
        
        stats1.refresh_from_db()
        self.assertEqual(stats1.order_count, 3) 
        self.assertEqual(stats1.total_spent, 110.00)