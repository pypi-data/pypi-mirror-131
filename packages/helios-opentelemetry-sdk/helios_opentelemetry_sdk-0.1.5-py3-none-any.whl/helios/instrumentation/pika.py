import json
from helios.instrumentation.base import HeliosBaseInstrumentor
from opentelemetry.trace import Span
from opentelemetry.semconv.trace import SpanAttributes


class PikaSpanAttributes:
    MESSAGING_PAYLOAD = 'messaging.payload'
    RABBIT_MQ_HEADERS = 'rabbitmq.headers'


class HeliosPikaInstrumentor(HeliosBaseInstrumentor):
    MODULE_NAME = 'opentelemetry.instrumentation.pika'
    INSTRUMENTOR_NAME = 'PikaInstrumentor'

    def __init__(self):
        super().__init__(self.MODULE_NAME, self.INSTRUMENTOR_NAME)

    def instrument(self, tracer_provider=None):
        if self.get_instrumentor() is None:
            return

        self.get_instrumentor().instrument(tracer_provider=tracer_provider, publish_hook=self.publish_hook,
                                           consume_hook=self.consume_hook)

    def publish_hook(self, span: Span, body: bytes, properties: dict):
        span.set_attribute(PikaSpanAttributes.MESSAGING_PAYLOAD, body.decode())
        span.set_attribute(PikaSpanAttributes.RABBIT_MQ_HEADERS, json.dumps(properties.headers))
        span.set_attribute(SpanAttributes.MESSAGING_URL, span.attributes.get(SpanAttributes.NET_PEER_NAME, None))

    def consume_hook(self, span: Span, body: bytes, properties):
        span.set_attribute(PikaSpanAttributes.MESSAGING_PAYLOAD, body.decode())
        span.set_attribute(PikaSpanAttributes.RABBIT_MQ_HEADERS, json.dumps(properties.headers))
        span.set_attribute(SpanAttributes.MESSAGING_URL, span.attributes.get(SpanAttributes.NET_PEER_NAME, None))
