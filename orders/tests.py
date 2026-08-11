from django.test import TestCase
from django.contrib.auth.models import User
from orders.models import Order, UserStats
from orders import services

class ServiceLayerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='service_user', password='pw')

    def test_signal_is_dead(self):
        Order.objects.create(user=self.user, total='50.00')
        
        stats_exist = UserStats.objects.filter(user=self.user).exists()
        self.assertFalse(stats_exist)

    def test_service_creates_order_and_updates_stats(self):
        order = services.create_order(user=self.user, total='100.00')
        
        self.assertIsNotNone(order.id)
        self.assertEqual(order.total, 100.00)
        
        stats = UserStats.objects.get(user=self.user)
        self.assertEqual(stats.order_count, 1)
        self.assertEqual(stats.total_spent, 100.00)


# from django.test import TestCase
# from django.contrib.auth.models import User
# from orders.models import Order, UserStats
# from orders.signals import update_user_stats_on_order_save
# from django.db.models.signals import post_save
# class SignalBypassTest(TestCase):
#     def test_bulk_update_bypasses_signal(self):
#         user1 = User.objects.create_user(username='user1', password='pw')
#         user2 = User.objects.create_user(username='user2', password='pw')
        
#         Order.objects.create(user=user1, total=50.00)
#         Order.objects.create(user=user1, total=50.00)
        
#         stats1 = UserStats.objects.get(user=user1)
#         self.assertEqual(stats1.order_count, 2)
#         self.assertEqual(stats1.total_spent, 100.00)
        
#         Order.objects.create(user=user1, total=10.00)
        
#         bulk_orders = [
#             Order(user=user2, total=20.00),
#             Order(user=user2, total=30.00)
#         ]
#         Order.objects.bulk_create(bulk_orders)
        
#         Order.objects.filter(user=user2).update(user=user1)
        
#         stats1.refresh_from_db()
#         self.assertEqual(stats1.order_count, 3) 
#         self.assertEqual(stats1.total_spent, 110.00)

# class SignalIsolationTest(TestCase):
#     def setUp(self):
#         post_save.connect(update_user_stats_on_order_save, sender=Order)
#         self.user = User.objects.create_user(username='iso_user', password='pw')

#     def tearDown(self):
#         post_save.disconnect(update_user_stats_on_order_save, sender=Order)

#     def test_signal_fires_when_connected(self):
#         Order.objects.create(user=self.user, total='100.00')
#         stats = UserStats.objects.get(user=self.user)
#         self.assertEqual(stats.total_spent, 100.00)

