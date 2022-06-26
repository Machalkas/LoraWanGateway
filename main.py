import queue
import time
from threading import Thread
import config
from utils.dataClass import CounterData
from vegaClient import Vega
from clickhouse_driver import Client
from database_clients.clickHouseClient import ClickHouseWriter
from database_clients.pgsqlClient import Counters
from utils import logger

from config import CLICKHOUSE_HOST, CLICKHOUSE_PORT, CLICKHOUSE_USER, CLICKHOUSE_DB_NAME, CLICKHOUSE_PASSWORD, PGSQL_DB_NAME, PGSQL_HOST, PGSQL_PASSWORD, PGSQL_USER

power_table_query = f"CREATE TABLE IF NOT EXISTS {CLICKHOUSE_DB_NAME}.power (`datetime` DateTime, `counter` UInt32, `phase_a` Nullable(Float64), `phase_b` Nullable(Float64), `phase_c` Nullable(Float64), `total` Nullable(Float64)) ENGINE = Log()"
traffic_table_query =  f"CREATE TABLE IF NOT EXISTS {CLICKHOUSE_DB_NAME}.traffic (`datetime` DateTime, `counter` UInt32, `traffic_plan_1` Nullable(Float64), `traffic_plan_2` Nullable(Float64), `traffic_plan_3` Nullable(Float64), `traffic_plan_4` Nullable(Float64), `total` Nullable(Float64), `current_traffic` Nullable(Int32)) ENGINE = Log()"
history_table_query = f"CREATE TABLE IF NOT EXISTS {CLICKHOUSE_DB_NAME}.history (`datetime` DateTime, `tags` String, `fields` String) ENGINE=Log()"

if __name__ == "__main__":

    logger.header("iot vega broker")

    vega_queue = queue.Queue()
    ws = None
    pgsql_client = Counters(PGSQL_HOST, PGSQL_USER, PGSQL_PASSWORD, PGSQL_DB_NAME, "create table if not exists counters (devEui text, devName text)")
    
    clickhouse_client = Client(host=CLICKHOUSE_HOST,
                           port=CLICKHOUSE_PORT,
                           user=CLICKHOUSE_USER,
                           password=CLICKHOUSE_PASSWORD)

    clickhouse_client.execute(f"CREATE DATABASE IF NOT EXISTS {CLICKHOUSE_DB_NAME}")
    power_writer = ClickHouseWriter(clickhouse_client, power_table_query, max_inserts_count=1000, timeout_sec=30)
    traffic_writer = ClickHouseWriter(clickhouse_client, traffic_table_query, max_inserts_count=1000, timeout_sec=30)
    # history_writer = ClickHouseWriter(clickhouse_client, history_table_query, timeout_sec=30, min_inserts_count=10, max_inserts_count=2000)
    while True:
        if ws is None:
            logger.success("vega start")
            ws = Thread(target=Vega,
                        args=(config.VEGA_URL,
                              config.VEGA_LOGIN,
                              config.VEGA_PASS,
                              config.DELAY,
                              config.DEV_UPDATE_DELAY,
                              vega_queue),
                        daemon=True,
                        name="VegaThread")
            ws.start()
        if not ws.is_alive():
            logger.warning("vega stop")
            ws = None
            time.sleep(5)
        
        if not vega_queue.empty():
            counters_data: CounterData = vega_queue.get()
            if counters_data.action == counters_data.GET_DEVICES:
                pgsql_client.save(counters_data.devices)
            for counter_data in counters_data.get():
                if counter_data.get("measurement") == "power":
                    values = {
                        "datetime": counter_data.get("time"),
                        "counter": counter_data.get("tags").get("counter"),
                        "total": counter_data.get("fields").get("total"),
                        "phase_a": counter_data.get("fields").get("phase_a"),
                        "phase_b": counter_data.get("fields").get("phase_b"),
                        "phase_c": counter_data.get("fields").get("phase_c")
                    }
                    power_writer.add_values(values)
                if counter_data.get("measurement") == "traffic":
                    values = {
                        "datetime": counter_data.get("time"),
                        "counter": counter_data.get("tags").get("counter"),
                        "total": counter_data.get("fields").get("total"),
                        "traffic_plan_1": counter_data.get("fields").get("traffic_plan_1"),
                        "traffic_plan_2": counter_data.get("fields").get("traffic_plan_2"),
                        "traffic_plan_3": counter_data.get("fields").get("traffic_plan_3"),
                        "traffic_plan_4": counter_data.get("fields").get("traffic_plan_4"),
                        "current_traffic": counter_data.get("fields").get("current_traffic")
                    }
                    traffic_writer.add_values(values)

                # history_writer.add_values({
                #     "datetime": datetime.now(),
                #     "tags": str(counters_data.action),
                #     "fields": str(counters_data)
                # })


                

