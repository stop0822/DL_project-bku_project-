from sqlite3 import Time
from django.test import TestCase

# Create your tests here.
import time

print(type(time.localtime().tm_year) , time.localtime().tm_mon , time.localtime().tm_mday )
