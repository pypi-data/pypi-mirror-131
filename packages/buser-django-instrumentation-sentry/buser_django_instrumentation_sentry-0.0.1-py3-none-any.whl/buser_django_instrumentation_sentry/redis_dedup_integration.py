import time
import redis
from sentry_sdk.hub import Hub
from sentry_sdk.integrations import Integration
from sentry_sdk.scope import add_global_event_processor


class RedisDedupIntegration(Integration):

    identifier = "redisdedup"

    def __init__(self, redis_client : redis.StrictRedis, max_events_per_minute : int=10):
        self.redis_client = redis_client
        self.max_events_per_minute = max_events_per_minute

    @staticmethod
    def setup_once():
        @add_global_event_processor
        def processor(event, hint):
            if hint is None:
                return event

            integration = Hub.current.get_integration(RedisDedupIntegration)

            exc_info = hint.get('exc_info')
            if exc_info is None:
                return event

            if integration.should_send(exc_info):
                return event
            else:
                return None

    def should_send(self, exc_info):
        key = self.build_key(exc_info)

        try:
            pipeline = self.redis_client.pipeline()
            pipeline.incr(key)
            pipeline.expire(key, 60)
            count, _ = pipeline.execute()

            if int(count) > RedisDedupIntegration.MAX_EVENTS_PER_MINUTE:
                return False

            return True
        except:
            return True

    @staticmethod
    def build_key(exc_info):
        lines = _get_exc_filenames_and_lines(exc_info)
        key = '|'.join(f'{fname}:{lineno}' for fname, lineno in lines)
        key = f'{key}:{int(time.time() // 60)}'
        return key


def _get_exc_filenames_and_lines(exc_info):
    _, _, exc_tb = exc_info
    lines = []
    while exc_tb is not None:
        lines.append((exc_tb.tb_frame.f_code.co_filename, exc_tb.tb_lineno))
        exc_tb = exc_tb.tb_next
    return lines
