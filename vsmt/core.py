import db
import sensor
import time
import threading


conn = None

def run(db_filename):
    #connect to the DB or create emtpy
    global conn 
    x = []
    conn = db.conn(db_filename)
    sensors = db.get_sensors(conn)
    for s in sensors:
        x.append(threading.Thread(target=sensor.sensor_ping ,  kwargs={'host': s[3], 'count': 1, 'timeout': 1, 'interval': 0.2, 'sleep_time': 1, 'output': False, 'log_db':True, 'db_name': db_filename, 'sensor_id': s[0]}))    
    for i in x:
        i.start()
    for i in x:
        i.join()
    conn.close()

