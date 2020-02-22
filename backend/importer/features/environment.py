import os


def before_all(context):
    context._environ = dict(os.environ)
    print(os.environ.get('TMDB_API'))
    os.environ['TMDB_API'] = 'test'
    print(os.environ.get('TMDB_API'))


def before_scenario(context, scenario):
    context.mocks = []


def after_all(context):
    os.environ.clear()
    os.environ.update(context._environ)
