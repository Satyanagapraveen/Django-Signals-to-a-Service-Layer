from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from orders.models import Order, UserStats
from orders import services

class ServiceLayerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='service_user', password='pw')

    def test_signal_is_dead(self):
        Order.objects.create(user=self.user, total=Decimal('50.00'))
        
        stats_exist = UserStats.objects.filter(user=self.user).exists()
        self.assertFalse(stats_exist)

    def test_service_creates_order_and_updates_stats(self):
        order = services.create_order(user=self.user, total=Decimal('100.00'))
        
        self.assertIsNotNone(order.id)
        self.assertEqual(order.total, Decimal('100.00'))
        
        stats = UserStats.objects.get(user=self.user)
        self.assertEqual(stats.order_count, 1)
        self.assertEqual(stats.total_spent, Decimal('100.00'))