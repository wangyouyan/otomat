#_*_ coding: UTF-8 _*_
import sys,time,os
reload(sys)
sys.setdefaultencoding('utf8')
import rrdtool
import random
from otomat.conf import conf
class graph_rrdtool:
    """
    rrdtool 绘图过程一共有四步：
    1.创建rrdtool数据库
    2.插入rrdtool所需的数据
    3.更新rrdtool数据库
    4.进行rrdtool绘图。
    """
    def __init__(self,filename="/etc/otomat/otomat.cnf",graph=None,title="北京壹號車 系統報告"):
        self.filename = filename
	cnf = conf.files_conf_check(self.filename)
	# rrdtool
	self.rrdtool_cpu = cnf.rrdtool_cpu()
	self.rrdtool_mem = cnf.rrdtool_mem()
	self.rrdtool_disk = cnf.rrdtool_disk()
	self.rrdtool_host = cnf.rrdtool_host()
	self.rrdtool_dir = cnf.rrdtool_dir()
	self.rrdtool_nic = cnf.rrdtool_nic()
	# graph
	self.graph_cpu = cnf.graph_cpu()
	self.graph_mem = cnf.graph_mem()
	self.graph_disk = cnf.graph_disk()
	self.graph_network = cnf.graph_network()
        self.insert = insert
        self.graph = graph
        self.title = title
        #self.time = str(int(time.time()))
    def rrdb(self):
        """
        1.创建rrdtool的数据库.
        """
        cur_time = str(int(time.time())) 

        

	
	host = self.rrdtool_host
	#print host
	report_dir = self.rrdtool_dir
	#print report_dir
	report_rrd = [self.rrdtool_cpu,self.rrdtool_mem,self.rrdtool_disk,self.rrdtool_nic]
	#print report_rrd
	if not os.path.exists(report_dir):
		os.mkdir(report_dir)
	for i in list(host.split(',')):
		os.chdir(report_dir)
		if not os.path.exists(i):
			os.mkdir(i)
		os.chdir(i)
		for j in report_rrd:
		#	if not os.path.exists(j):
		#		os.mknod(j)
			if not os.path.exists('nic.rrd'):
				# network_db
				rrdtool.create('nic.rrd','--step','300','--start',cur_time,
        				'DS:input:GAUGE:600:U:U',
        				'DS:output:GAUGE:600:U:U',
       					'RRA:LAST:0.5:1:600',
        				'RRA:AVERAGE:0.5:5:600',
       					'RRA:MAX:0.5:5:600',
        				'RRA:MIN:0.5:5:600')
			if not os.path.exists('cpu.rrd'):
				# cpu_db
				rrdtool.create('cpu.rrd','--step','300','--start',cur_time,
					'DS:cpu_percent:GAUGE:600:U:U',
					'RRA:LAST:0.5:1:600',
					'RRA:AVERAGE:0.5:5:600',
					'RRA:MAX:0.5:5:600',
					'RRA:MIN:0.5:5:600')
			if not os.path.exists('mem.rrd'):
				# mem_db
				rrdtool.create('mem.rrd','--step','300','--start',cur_time,
					'DS:mem_total:GAUGE:600:U:U',
					'DS:mem_free:GAUGE:600:U:U',
					'DS:mem_used:GAUGE:600:U:U',
					'DS:mem_percent:GAUGE:600:U:U',
					'DS:swap_total:GAUGE:600:U:U',
					'DS:swap_free:GAUGE:600:U:U',
					'DS:swap_used:GAUGE:600:U:U',
					'DS:swap_percnet:GAUGE:600:U:U',
					'RRA:LAST:0.5:1:600',
					'RRA:AVERAGE:0.5:5:600',
					'RRA:MAX:0.5:5:600',
					'RRA:MIN:0.5:5:600')
			if not os.path.exists('disk.rrd'):
				# disk_db
				rrdtool.create('disk.rrd','--step','300','--start',cur_time,
					'DS:disk_total:GAUGE:600:U:U',
					'DS:disk_free:GAUGE:600:U:U',
					'DS:disk_used:GAUGE:600:U:U',
					'DS:disk_percnet:GAUGE:600:U:U',
					'RRA:LAST:0.5:1:600',
					'RRA:AVERAGE:0.5:5:600',
					'RRA:MAX:0.5:5:600',
					'RRA:MIN:0.5:5:600')
    def rrdb_insert(self):
	"""
	2.插入rrdtool所需的数据
	3.更新rrdtool数据库

	"""
	import MySQLdb
	sql_cpu = "select Host_ip,Time,Cpu_Utilization from report_list \
		where Time > date_format(date_sub(now(),interval 1 HOUR),'%Y-%m-%d %H:00:00') \
		and Time< date_format(now(),'%Y-%m-%d %H:00:00')"
	sql_disk = "select Host_ip,Time,Mem_total,Mem_free,Mem_used,Mem_percent,Swap_total, \
		Swap_free,Swap_used,Swap_percent from report_list \
		where Time > date_format(date_sub(now(),interval 1 HOUR),'%Y-%m-%d %H:00:00')  \
		and Time< date_format(now(),'%Y-%m-%d %H:00:00')"
	sql_mem = "select Host_ip,Time,Disk_total,Disk_free,Disk_used,Disk_percent from report_list \
		where Time > date_format(date_sub(now(),interval 1 HOUR),'%Y-%m-%d %H:00:00') \
		and Time< date_format(now(),'%Y-%m-%d %H:00:00')"
	sql_nic = "select Host_ip,Time,Network_traffic_recv,Network_traffic_sent from report_list \
		where Time > date_format(date_sub(now(),interval 1 HOUR),'%Y-%m-%d %H:00:00') \
		and Time< date_format(now(),'%Y-%m-%d %H:00:00')"
	while True:
		conn = MySQLdb.connect(host,user,password,defaultdb)
		cur = conn.cursor()
		
	
    def rrdtool_graph(self):
         rrdtool.graph(self.graph,'--start',self.time,
            '--title',self.title,
            '--vertical-label','bits',
            'DEF:input=rest.rrd:input:LAST',
            'DEF:output=rest.rrd:output:LAST',
            'LINE1:input#0000FF:In traffic',
            'LINE1:output#00FF00:Out traffic\\r',
            'CDEF:bytes_in=input,8,*',
            'CDEF:bytes_out=output,8,*',
            'COMMENT:\\n',
            'GPRINT:bytes_in:LAST:LAST in traffic\: %6.2lf %Sbps',
            'COMMENT:  ',
            'GPRINT:bytes_out:LAST:LAST out traffic\: %6.2lf %Sbps')  

