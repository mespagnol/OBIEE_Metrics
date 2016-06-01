# Author: Mariano Espagnol
# Python Script to read WLS performance metrics and store them

import sys
import calendar, time, datetime
import os 

# Get parameter values 
wls_user = sys.argv[1]
wls_pwd = sys.argv[2]
url = sys.argv[3]

# Timestamp variable
ts = time.time()
start_date = str(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d'))
start_time = str(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H%M%S'))
root_folder = '/app/oracle/biee/oracle_common/common/bin/'
output_filename = root_folder + start_date + "_dms_metrics_dump.txt"

# Connect to WLS
connect(wls_user, wls_pwd, url);

# This is where we define the metrics we'd like to report on

# new dict to store the values we want to report on
metrics_obi = {'oracle_bi_instance:obis_domain_rollup':['Avg._query_elapsed_time.value','Queries_sec.value','Total_sessions.value'],'oracle_bi_instance:obips_domain_rollup':['Active_Sessions.value','Current_Requests.value','GETPOST_Requests.value','SOAP_Requests.value'],'oracle_bi_instance:wls_app_rollup':['service.throughput','service.time','session.active']}

# open file
file = open(output_filename,'a')

len_dict = len(metrics_obi)
for key, items in metrics_obi.iteritems():
	results = displayMetricTables(key)
	for table in results:
        	name = table.get('Table')
        	rows = table.get('Rows')
    	rowCollection = rows.values()
    	iter = rowCollection.iterator()
    	while iter.hasNext():
        	row = iter.next()
		if (key == 'oracle_bi_instance:wls_app_rollup' and row.containsValue("analytics")) or not key == 'oracle_bi_instance:wls_app_rollup':
			    rowType = row.getCompositeType()
			    keys = rowType.keySet()
			    keyIter = keys.iterator()
			    while keyIter.hasNext():
				columnName = keyIter.next()
				value = row.get(columnName)
				if columnName in items:
				    print >>file, start_time + "," + key + "," + columnName + ',' + str(value)
file.close()
disconnect()
