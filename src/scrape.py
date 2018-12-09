import urllib2
import json
from bs4 import BeautifulSoup

def safe_float(value):
  return float(value.replace(',',''))

def get_cpu(obj):
  if obj.get('vCPU'):
    return safe_float(obj.get('vCPU'))
  elif obj.get('vCPU*'):
    return safe_float(obj.get('vCPU*').replace('*',''))
  elif obj.get('Logical Proc*'):
    return safe_float(obj.get('Logical Proc*').replace('*',''))
  else:
    raise Exception('Could not get cpu')

def get_memory(obj):
  if obj.get('Mem (GiB)'):
    return safe_float(obj.get('Mem (GiB)'))
  elif obj.get('Mem (TiB)'):
    return safe_float(obj.get('Mem (TiB)')) * 1024
  elif obj.get('Memory (GiB)'):
    return safe_float(obj.get('Memory (GiB)'))
  else:
    raise Exception('Could not get memory')

def get_storage(obj):
  if obj.get("Storage"):
    return obj.get("Storage")
  elif obj.get("Storage (GiB)"):
    return obj.get("Storage (GiB)") + 'GiB'
  elif obj.get("Storage (GB)"):
    return obj.get("Storage (GB)") + 'GB'
  elif obj.get("Storage (TB)"):
    return obj.get("Storage (TB)") + 'TB'
  elif obj.get("SSD Storage (GB)"):
    return obj.get("SSD Storage (GB)") + 'SSD GB'
  else:
    return None

def get_network(obj):
  if obj.get("Networking Performance (Gbps)"):
    return obj.get("Networking Performance (Gbps)") + 'Gbps'
  elif obj.get("Network Performance"):
    return obj.get("Network Performance")
  elif obj.get("Network Performance (Gbps)"):
    return obj.get("Network Performance (Gbps)") + 'Gbps'
  elif obj.get("Networking Performance"):
    return obj.get("Networking Performance")
  else:
    return None
  

instances = {}

url = "https://aws.amazon.com/ec2/instance-types/?nc1=h_ls"
page = urllib2.urlopen(url).read()
soup = BeautifulSoup(page)
for table in soup.find_all('table'):
  trs = table.find_all('tr')
  header = trs[0].find_all('td')
  for tr in trs[1:]:
    tds = tr.find_all('td')
    obj = {header[i].text.strip(): tds[i].text.strip() for (i,v) in enumerate(tds)}
    if 'Model' in obj:
      try:
        ec2 = {
          'cpu': get_cpu(obj),
          'memoryGiB': get_memory(obj),
          'storage':  get_storage(obj),
          'network': get_network(obj)
        }
        instances.update({obj['Model'] : ec2})
      except Exception as e:
        print('Could not process', obj['Model'], e)

url = "https://aws.amazon.com/ec2/previous-generation/?nc1=h_ls"
page = urllib2.urlopen(url).read()
soup = BeautifulSoup(page)
for table in soup.find_all('table'):
  trs = table.find_all('tr')
  header = trs[0].find_all('td')
  for tr in trs[1:]:
    tds = tr.find_all('td')
    obj = {header[i].text.strip(): tds[i].text.strip() for (i,v) in enumerate(tds)}
    if 'Instance Type' in obj:
      try:
        ec2 = {
          'cpu': get_cpu(obj),
          'memoryGiB': get_memory(obj),
          'storage':  get_storage(obj),
          'network': get_network(obj)
        }
        instances.update({obj['Instance Type'] : ec2})
      except Exception as e:
        print('Could not process', obj['Instance Type'], e)


print(json.dumps(instances))