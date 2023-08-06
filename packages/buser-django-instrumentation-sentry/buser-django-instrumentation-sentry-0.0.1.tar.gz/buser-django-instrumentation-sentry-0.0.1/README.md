# buser-django-instrumentation-sentry

Projeto com alguns utilitários para ajudar no envio de erros para o Sentry.

O que tem aqui que pode ajudar no seu projeto?

* Rate-limiting de envio de erros usando REDIS
* Sanitizadores padrões para ajudar não enviar PII para o Sentry

## Como usar?

```shellscript
pip install buser-django-instrumentation-sentry
# coloca no seu requirements.in!
```

E então no projeto inicializa o Sentry usando os utilitários disponíveis aqui.

```python
import sentry_sdk
import redis
from buser_django_instrumentation_sentry.redis_dedup_integration import RedisDedupIntegration
from buser_django_instrumentation_sentry.sanitize import create_event_sanitizer

redis_client = redis.StrictRedis()

sentry_sdk.init(
    before_send=create_event_sanitizer(),
    integrations=[
        RedisDedupIntegration(redis_client)
    ]
)
```