# -*- coding: utf-8 -*-
import psutil,time   # pip install psutil

def cpu_info():
  per = psutil.cpu_percent(interval=1)
  print per
  return per


def mem_info():
  mem = psutil.virtual_memory()
  #print mem
  return {
    "total":mem[0]/1024/1024/1024,
    "used":mem[3]/1024/1024/1024,
    "free":mem[4]/1024/1024/1024,
    "percent":mem[2],
  }

def disk_info():
  partitions = psutil.disk_partitions()
  disk = {"total":0,"used":0,"free":0,"percent":0}
  for p in partitions :
    if p[0].find('/dev/') > -1 :
      usage = psutil.disk_usage(p[1])
      disk['total'] += usage[0]
      disk['used'] += usage[1]
      disk['free'] += usage[2]
  if disk['total'] > 0 :
    disk['percent'] = round((float(disk['used'])/float(disk['total']))*100,2)
  print disk
  return disk

def net_info(name):
  net_io_old = psutil.net_io_counters(pernic=True)
  time.sleep(1)
  net_io_now = psutil.net_io_counters(pernic=True)
  print net_io_old[name],net_io_now[name]
  return {
    "sent":net_io_old[name][0]-net_io_old[name][0],
    "recv":net_io_now[name][1]-net_io_now[name][1],
  }

cpu_per = cpu_info()
mem = mem_info()
info = '''
=====cpu-info======
percent:%s%%
=====memory-info======
total:%sG
used:%sG
free:%sG
percent:%s%%
===================
''' % (cpu_per,mem['total'],mem['used'],mem['free'],mem['percent'])
#print(info)
#disk_info()
#print net_info("en0")

filename = '/tmp/server-status.log'
fo = open(filename,'w')
fo.write("%s" % (cpu_per))
fo.close()
