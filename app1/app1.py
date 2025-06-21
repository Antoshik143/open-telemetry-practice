import uuid
from flask import Flask, jsonify
import time
import random
import requests
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

app = Flask(__name__)

# Configure OpenTelemetry
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({"service.name": "api1"})
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

# Instrument Flask and Requests
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

@app.route("/api1")
def api():
    delay = random.randint(1, 5)
    time.sleep(delay)
    with trace.get_tracer(__name__).start_as_current_span("api1") as span:
        tracking_id = str(uuid.uuid4())
        span.set_attribute("tracking_id", tracking_id)
        headers = {'tracking_id': tracking_id}
        requests.get('http://api2:5002/api2', headers=headers)
        return jsonify({"result": "You are at the API endpoint.", "tracking_id": tracking_id})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)