from datetime import datetime
import os

def append_log(msg):
    curr_time = datetime.now()
    msg = '\n[{}] '.format(curr_time) + msg

    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = 'logs/log.txt'
    path = os.path.join(script_dir, rel_path)

    log_file = open(path, 'a')
    log_file.write(msg)
    log_file.close()