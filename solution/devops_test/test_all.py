import unittest
import boto
import os

class TestDevOpsApp(unittest.TestCase):

   # Init of testcases
   def setUp(self):
      self.s3 = boto.connect_s3()


   # App expects these environment variables to be set
   def test_env(self):
      self.assertIsNotNone(os.environ.get('AWS_ACCESS_KEY_ID'))
      self.assertIsNotNone(os.environ.get('AWS_SECRET_ACCESS_KEY'))

   def test_connection(self):
      connection = boto.connect_s3()
      self.assertIsNotNone(connection)

if __name__ == '__main__':
   unittest.main()
