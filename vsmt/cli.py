import argparse
import ping
import sys
import sensor
import core
import db

DB_FILENAME = 'vsmt.sqlite'

parser = argparse.ArgumentParser(description='Very Simple Monitoring Tool (VSMT).')

def print_exit(message):
    global parser
    print('Error: '+message)
    parser.print_help()
    sys.exit(1)

def cli():
    global parser
    global DB_FILENAME
    parser.add_argument('--db-file', dest='db_file', action='store', default=DB_FILENAME, help='Specify SQLite DB file to be used (default: vsmt.sqlite) ')    

    operation = parser.add_argument_group('Operations')
    operation.add_argument('-o', "--operation", dest='operation', action='store', help='Use operations to configure vsmt. Availabe operations: add_sensor/remove_sensor/modify_sensor/list_sensors')    
    operation.add_argument('-Sn', "--sensor-name", dest='sensor_name', action='store', help='Sensor name')   
    operation.add_argument('-St', "--sensor-type", dest='sensor_type', action='store', help='Sensor type. Possible values: [ping]')   
    operation.add_argument('-Sh', "--sensor-hostname", dest='sensor_hostname', action='store', help='Sensor hostname.')
    operation.add_argument('-Sp', "--sensor-parameters", dest='sensor_paramneters', action='store', help='Sensor parameters in JSON format YYYY . Example: XXXXX')
    #TODO: move parameters name
    debug = parser.add_argument_group('Alternative working modes')
    debug.add_argument("-a", "--action", action="store",  dest='action', help='Instead of runing daemon run just single action. Available actions: ping, sensor_ping')
    debug.add_argument("-H", "--hostname", action="store",  dest='hostname', help='Host name')
    debug.add_argument("-st", "--sleep-time", action="store",  default=1, dest='sleep_time', help='Sleep time between actions')

    #debug = parser.add_argument_group('Debugging arguments')
    #debug.add_argument("-d", "--debug", action="count", default=0,  help="Turn on debug mode")

    args = parser.parse_args()    

    #Handle operations
    if args.operation == 'add_sensor':
        if (args.sensor_name == None or args.sensor_type == None  or args.sensor_hostname == None):
            print_exit("To add sensor you need to specify following attributes: sensor-name, sensor-type, sensor-hostname")
        elif args.sensor_type != 'ping':
            print_exit("Incorrect sensor type")
        else:
            db.add_sensor(args.db_file, args.sensor_name,args.sensor_type,args.sensor_hostname,args.sensor_paramneters)
    elif args.operation == 'remove_sensor':
        if (args.sensor_name == None):
            print_exit("To remove sensor you need to specify following attributes: sensor-name")
        else:
            db.remove_sensor(args.db_file, args.sensor_name)
    elif args.operation == 'list_sensors':            
         db.list_sensors(args.db_file)
    #Handle actions
    elif args.action == 'ping':
        if args.hostname == None:
            print_exit("For 'ping' action 'hostname' is mandatory.")
        else:
            print(ping.ping(args.hostname))
    elif args.action == 'sensor_ping':
        if args.hostname == None:
            print_exit("For 'ping' action 'hostname' is mandatory.")
        else:
            print(sensor.sensor_ping(args.hostname, output=True, sleep_time=float(args.sleep_time)))
    else:
        core.run(args.db_file)