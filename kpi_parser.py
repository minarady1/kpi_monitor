import glob
import os

LOG_DIR_NAME = 'logs'
log_dir_path = os.path.join(os.path.dirname(__file__), LOG_DIR_NAME)

print (log_dir_path)
directory =r"C:\openwsn\experiments\KPI analysis\logs"
for filename in os.listdir(directory):
    if ("log-kpis-24GHZ_OQPSK" in filename) : 
        print(os.path.join(directory, filename))
        continue
    else:
        continue