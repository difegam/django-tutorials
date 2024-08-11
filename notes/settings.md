# Generating a new SECRET_KEY

```python
poetry run python -c 'from django.core.management.utils import get_random_secret_key; import secrets; print(secrets.token_hex(5) + get_random_secret_key() + secrets.token_urlsafe(5))'
```

