from flask import Flask, jsonify
import redis
import os

app = Flask(__name__)

redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_port = int(os.environ.get("REDIS_PORT", 6379))


try:
    r = redis.Redis(
        host=redis_host,
        port=redis_port,
        db=0,
        socket_connect_timeout=1,
        decode_responses=True,
    )
    r.ping()
    print("Successful connection to Redis!")
except redis.exceptions.ConnectionError as e:
    print(f"Could not connect to Redis: {e}")
    r = None


@app.route("/")
def hello():
    return "Welcome to my DevOps app!"


@app.route("/visit")
def visit():
    if r:
        try:
            visits = r.incr("visits_counter")
            return jsonify({"visits": visits})
        except redis.exceptions.ConnectionError as e:
            return jsonify(
                {"error": f"Could not connect to Redis to update counter: {str(e)}"}
            ), 500
    else:
        return jsonify({"error": "Redis connection not available."}), 500


@app.route("/health")
def health_check():
    if r:
        try:
            r.ping()
            return jsonify({"status": "ok"}), 200
        except redis.exceptions.ConnectionError as e:
            return jsonify({"error": f"Could not connect to Redis: {str(e)}"}), 500
    else:
        return jsonify({"status": "error", "details": "Redis connection not available."}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
