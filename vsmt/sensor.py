import ping
import time
import db
import json

def sensor_ping (host, count = 1, timeout = 1, interval = 0.2, sleep_time = 60, output=False, log_db=False, db_name = None, sensor_id = None):
    conn = None
    while True:
        result = ping.ping(host, count, timeout,  interval)
        if output == True:
            print(result)
        if log_db == True:
            if conn == None:
                conn = db.conn(db_name)
            attributes = {"response": str(result[0]), "reason_code": str(result[1]), "response_time": float(result[2])}
            db.log_sensor(conn, sensor_id, result[0], json.dumps(attributes))
        time.sleep(sleep_time)