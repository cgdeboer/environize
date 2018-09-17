from .settings import ENVS, DEFAULT_ENV, settings


def only_in(envs=[]):

    assert all([e in ENVS for e in envs]) is True

    def decorator(func):

        def handle(*args, **kwargs):
            env = getattr(settings, "ENVIRONMENT", DEFAULT_ENV)
            exclude_tests = ('test' not in envs and
                             'testserver' in settings.ALLOWED_HOSTS)
            if env not in envs or exclude_tests:
                return lambda x, y: None
            func(*args, **kwargs)
        return handle

    return decorator


def except_in(envs=[]):

    assert all([e in ENVS for e in envs]) is True

    def decorator(func):

        def handle(*args, **kwargs):
            env = getattr(settings, "ENVIRONMENT", DEFAULT_ENV)
            exclude_tests = ('test' in envs and
                             'testserver' in settings.ALLOWED_HOSTS)
            if env in envs or exclude_tests:
                return lambda x, y: None
            func(*args, **kwargs)
        return handle

    return decorator
