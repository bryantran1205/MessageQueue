from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from confluent_kafka import Producer, Consumer
import threading
from kafka_utils import clear_kafka_topic

# Kafka configurations
BROKER = "localhost:9092"
TOPIC = "my_topic"

# Flask app and SocketIO
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)

# Kafka Producer
producer_conf = {"bootstrap.servers": BROKER}
producer = Producer(producer_conf)

# Kafka Consumer
consumer_conf = {
    "bootstrap.servers": BROKER,
    "group.id": "web_group",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": True,
}
consumer = Consumer(consumer_conf)

# Store messages for web display
messages = []


@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html", messages=messages)


@app.route("/send", methods=["POST"])
def send_message():
    """Handle message sending."""
    message = request.form.get("message")
    if message:
        try:
            producer.produce(TOPIC, value=message, callback=delivery_report)
            producer.flush()
            return jsonify(
                {"status": "success", "message": "Message sent successfully!"}
            )
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    return jsonify({"status": "error", "message": "Message cannot be empty!"})


def delivery_report(err, msg):
    """Callback for message delivery."""
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def consume_messages():
    """Consume messages from Kafka and emit them to the web."""
    consumer.subscribe([TOPIC])
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        message = msg.value().decode("utf-8")
        print(f"Received Kafka message: {message}")  # Log thông điệp để kiểm tra
        messages.append(message)
        socketio.emit(
            "new_message", {"message": message}
        )  # Emit message through WebSocket


# Run the Kafka consumer in a separate thread
thread = threading.Thread(target=consume_messages)
thread.daemon = True
thread.start()


@app.route("/clear_topic", methods=["POST"])
def clear_topic():
    """Clear Kafka topic by resetting retention time and consumer offsets."""
    try:
        # Xóa nội dung trong topic
        clear_kafka_topic(BROKER, TOPIC, retention_time_ms=1000)

        # Xóa bảng hiển thị trên client (clear messages list)
        messages.clear()

        return jsonify(
            {
                "status": "success",
                "message": "Topic cleared and displayed messages reset successfully!",
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == "__main__":
    socketio.run(app, debug=True)
