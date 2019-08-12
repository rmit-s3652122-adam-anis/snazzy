from django.test import TestCase
from django.contrib.auth.models import User

#create your tests here

class ModelTest(TestCase):

    @classmethod
    def setUpClass(cls):

        #fix AttributeError: type object 'Model Test' has no attribute 'cls_atomics' error
        super(ModelTest, cls).setUpClass()

        # creare and save a User object
        testUser = User(username="testUser", email="test@email.com")
        testUser.set_password("testing321")
        testUser.save()
        print('Added new test user')

    def test_user_models(self):
        findUser = User.objects.get(username="testUser")
        self.assertEqual(findUser.email, 'test@email.com')    