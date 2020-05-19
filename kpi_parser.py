import glob
import os
import json

LOG_DIR_NAME = 'logs'
log_dir_path = os.path.join(os.path.dirname(__file__), LOG_DIR_NAME)

directory =r"C:\openwsn\experiments\kpi_monitor\logs"

for filename in os.listdir(directory):
    if ("log-kpis-24GHZ_OQPSK" in filename):
    	print filename
    	file_dir=os.path.join(directory,filename)
    	with open (file_dir) as f:
    		for line in f:
    			data=json.loads(line)
    			print '{},{}'.format(data['timestamp'],data['data']['avg_dutyCycle'])
    		#print data
        continue
    else:
        continue