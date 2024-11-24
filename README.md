# Prepare

pip install flask flask-socketio confluent-kafka

# MessageQueue

Step 1: docker-compose up -d
Step 2:python app.py
step 3: open browser and run http://localhost:5000

# Note

Có thể check các nội dung bằng câu lệnh sau trong phần exec của kafka trên docker
kafka-console-consumer --bootstrap-server localhost:9092 --topic my_topic --from-beginning
