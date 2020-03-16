import cmd
import re

def ping(host, count = 1, timeout = 1, interval = 0.2):
    result = cmd.run("ping "+host+" -c "+str(count)+" -i "+str(interval)+" -W "+str(timeout), float(count*timeout)+5)    
    # 1. check for  srvice not known - domain doesn't exist
    if re.search('ping: (.*): Name or service not known', result):
        return 'NOK', 'DNS_NOT_EXISTS', None
    # 2. check if there is reply
    if re.search('100% packet loss', result):
        return 'NOK', 'NOT_RESPONSE', None        
    # 3. find average response time        
    rtt_avg = float(re.search(r'rtt min/avg/max/mdev = \d{1,10}.\d{1,10}/(.*?)/\d{1,10}.\d{1,10}/\d{1,10}.\d{1,10} ms', result).group(1))
    return 'OK', None, rtt_avg
