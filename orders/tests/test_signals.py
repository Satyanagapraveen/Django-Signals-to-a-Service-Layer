from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from orders.models import Order, UserStats
from decimal import Decimal

# --- THE MOCK SIGNAL ---
def dummy_stats_updater(sender, instance, created, **kwargs):
    """A fake signal used only to prove framework vulnerabilities."""
    if created:
        stats, _ = UserStats.objects.get_or_create(user=instance.user)
        stats.order_count += 1
        stats.total_spent += Decimal(instance.total)
        stats.save()

class SignalBypassTest(TestCase):
    def setUp(self):
        post_save.connect(dummy_stats_updater, sender=Order)
        
    def tearDown(self):
        post_save.disconnect(dummy_stats_updater, sender=Order)

    def test_bulk_update_bypasses_signal(self):
        user1 = User.objects.create_user(username='user1', password='pw')
        user2 = User.objects.create_user(username='user2', password='pw')
        
        Order.objects.create(user=user1, total='50.00')
        Order.objects.create(user=user1, total='50.00')
        
        stats1 = UserStats.objects.get(user=user1)
        self.assertEqual(stats1.order_count, 2)
        self.assertEqual(stats1.total_spent, 100.00)
        
        Order.objects.create(user=user1, total='10.00')
        
        bulk_orders = [
            Order(user=user2, total='20.00'),
            Order(user=user2, total='30.00')
        ]
        Order.objects.bulk_create(bulk_orders)
        
        Order.objects.filter(user=user2).update(user=user1)
        
        stats1.refresh_from_db()
        self.assertEqual(stats1.order_count, 3) 
        self.assertEqual(stats1.total_spent, 110.00)