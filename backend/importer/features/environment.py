import os
from behave_django.testcase import BehaviorDrivenTestCase
from django.test import TransactionTestCase


def before_all(context):
    context._environ = dict(os.environ)
    os.environ['TMDB_API'] = 'test'


def before_scenario(context, scenario):
    context.mocks = []


def after_all(context):
    os.environ.clear()
    os.environ.update(context._environ)


# To force django-behave to rollback the db to initial state, instead of truncating (thus losing the data inserted by migrations)
old_test_case_init = BehaviorDrivenTestCase.__init__

def new_test_case_init(self, *k, **kw):
    old_test_case_init(self, *k, **kw)
    TransactionTestCase.serialized_rollback = True


BehaviorDrivenTestCase.__init__ = new_test_case_init
