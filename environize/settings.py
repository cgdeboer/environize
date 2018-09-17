from django.conf import settings

defaults = ("dev", "test", "ci", "qa", "staging", "production")
ENVS = getattr(settings, "ENVIRONIZE_ENVS", defaults)
DEFAULT_ENV = getattr(settings, "ENVIRONIZE_DEFAULT_ENV", "dev")
