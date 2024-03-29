import os
import uuid

INFLUX_DB_NAME = "vega"
INFLUX_HOST = "192.168.0.123"
INFLUX_PORT = 8086

MYSQL_HOST = os.getenv("MYSQL_HOST") or "localhost"
MYSQL_USER = os.getenv("MYSQL_USER") or "root"
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD") or None
MYSQL_DB_NAME = os.getenv("MYSQL_DB_NAME") or "vega"

PGSQL_HOST = os.getenv("PGSQL_HOST") or "localhost"
PGSQL_PORT = os.getenv("PGSQL_PORT") or "5432"
PGSQL_USER = os.getenv("PGSQL_USER") or "admin"
PGSQL_PASSWORD = os.getenv("PGSQL_PASSWORD") or "iotlab"
PGSQL_DB_NAME = os.getenv("PGSQL_DB_NAME") or "vega"

CLICKHOUSE_DB_NAME = os.getenv("CLICKHOUSE_DB_NAME") or "vega"
CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST") or "localhost"
CLICKHOUSE_PORT = os.getenv("CLICKHOUSE_PORT") or "9000"
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER") or "default"
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD") or None

VEGA_URL = os.getenv("VEGA_URL") or "ws://192.168.0.128:8002"
VEGA_PASS = os.getenv("VEGA_PASS") or "router"
VEGA_LOGIN = os.getenv("VEGA_LOGIN") or "router"
DATA_READ_DELAY = os.getenv("DATA_READ_DELAY") or 15*60
COUNTERS_UPDATE_DELAY = os.getenv("COUNTERS_UPDATE_DELAY") or 60*30

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", f"LoraGateway-{uuid.uuid4()}")
MQTT_TOPICS_TO_SUBSCRIBE = [ topic.strip() for topic in os.getenv("MQTT_TOPICKS_TO_SUBSCRIBE", "gateway/#").split()]

DT_FORMAT = "%Y-%m-%d %H:%M:%S"

DEBUG = False if os.getenv("DEBUG") == "false".lower() else True
