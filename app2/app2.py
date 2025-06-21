import uuid
from flask import Flask, jsonify, request
import time
import random
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor

app = Flask(__name__)

# Configure OpenTelemetry
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({"service.name": "api2"})
    )
)

# Use OTLP Exporter to send to Collector
otlp_exporter = OTLPSpanExporter(
    #endpoint="otel-collector:4317" # Address of your OpenTelemetry Collector Deployment collector
    endpoint="127.0.0.1:4317",  # Address of your OpenTelemetry Collector sidecar container!
    insecure=True  # For testing only, in production use proper security
)

# Configure the trace processor
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Instrument Flask
FlaskInstrumentor().instrument_app(app)

@app.route("/api2")
def api():
    delay = random.randint(1, 5)
    time.sleep(delay)
    with trace.get_tracer(__name__).start_as_current_span("api2") as span:
        tracking_id = request.headers.get('tracking_id')
        span.set_attribute("tracking_id", tracking_id)
        return jsonify({"result": "You are at the API endpoint.", "tracking_id": tracking_id})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)