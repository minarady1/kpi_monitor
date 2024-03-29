import paho.mqtt.client as mqttClient
import time
import datetime
import os
import sys
import datetime
import utils
import click
import json
import winsound
EXPERIMENT_ID = "hybrid_test_cjoin"
run_id = "run_17"
LOG_DIR_NAME = 'logs'
log_file_path = ''
first_record = True
def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")

        global Connected                #Use global variable
        Connected = True                #Signal connection
        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 500  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)
        winsound.Beep(frequency, duration)
 
    else:
 
        print("Connection failed")
 
def on_message(client, userdata, message):
    print "Message received: "  + message.payload
    log_data(message.payload)

def prepare_log_file():
    log_dir_path = os.path.join(os.path.dirname(__file__), LOG_DIR_NAME,run_id)

    # make sure we have the log directory
    if os.path.isdir(log_dir_path):
        # log directory is ready :-)
        pass
    else:
        try:
            os.mkdir(log_dir_path)
        except OSError as err:
            sys.exit('Failed to make the log directory: {}'.format(err))

    # decide a log file name and create it
    log_file_name = 'log-kpis-{}_{}-{}.jsonl'.format(EXPERIMENT_ID, run_id,
        time.strftime('%Y%m%d-%H%M%S')
    )
    log_file_path = os.path.join(log_dir_path, log_file_name)
    if os.path.exists(log_file_path):
        msg = (
            'Failed to crate a log file.\n' +
            'Log file already exits: {}'.format(log_file_path)
        )
        sys.exit(msg)
    else:
        # create an empty file with the log file name
        try:
            open(log_file_path, 'w').close()
        except OSError as err:
            sys.exit('Failed to create a log file: {}'.format(err))

    return log_file_path

def log_data (data):
    global log_file_path
    ts = datetime.datetime.now()
    with open(log_file_path, 'a') as f:
        log = {
            'name': EXPERIMENT_ID,
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            'data':json.loads(data)
        }
        f.write('{}\n'.format(json.dumps(log)))


EXPERIMENT_ID = sys.argv[1]

Connected = False   #global variable for the state of the connection
 
broker_address= "argus.paris.inria.fr"  #Broker address
port = 1883                          #Broker port
#user = "yourUser"                    #Connection username
#password = "yourPassword"            #Connection password

client = mqttClient.Client("Python")               #create new instance
#client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback

log_file_path = prepare_log_file() 
print log_file_path
client.connect(broker_address, port=port,keepalive=60)          #connect to broker
 
client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)
 
client.subscribe("opentestbed/uinject/arrived/")
 
try:
    while True:
        time.sleep(1)
 
except KeyboardInterrupt:
    print "exiting"
    client.disconnect()
    client.loop_stop()