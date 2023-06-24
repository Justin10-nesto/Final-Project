from django.test import TestCase
# from schools.models import UserLog
# from django.contrib.auth.models import User

# class UserLogsTesting(TestCase):
#     def setUp(self):
#         user = User.objects.all()
#         UserLog.objects.create(task = 'testing logs', user = user.first())

#     def test_animals_can_speak(self):
#         """Animals that can speak are correctly identified"""
#         lion = UserLog.objects.get(task = 'testing logs')
#         self.assertEqual(lion.speak(), 'The lion says "roar"')
#         self.assertEqual(cat.speak(), 'The cat says "meow"')