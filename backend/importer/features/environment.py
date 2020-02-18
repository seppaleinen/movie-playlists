"""
behave environment module for testing behave-django
"""

def before_scenario(context, scenario):
	context.mocks = []
