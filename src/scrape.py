import requests
from bs4 import BeautifulSoup
import json

def safe_float(value):
  return float(value.replace(',',''))

def get_cpu(obj):
  if obj.get('vCPU'):
    return safe_float(obj.get('vCPU').replace('*',''))
  elif obj.get('vCPU*'):
    return safe_float(obj.get('vCPU*').replace('*',''))
  elif obj.get('Logical Proc*'):
    return safe_float(obj.get('Logical Proc*').replace('*',''))
  else:
    raise Exception('Could not get cpu')

def get_table_row_elements_content(row):
	return [e.text.strip() for e in row.find_all('td') + row.find_all('th')]

def parse_table(table,skip_tr=0):
	trs = table.find_all('tr')
	header_row = trs[skip_tr]
	content_rows = trs[(skip_tr+1):]
	header = get_table_row_elements_content(header_row)
	for c in content_rows:
		row = get_table_row_elements_content(c)
		yield { k:v for (k,v) in zip(header,row)}


def get_ec2_data(row):
	return {
		'cpu': get_cpu(row)
	}

def fetch_ec2_data(url, instance_column):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	tables = soup.find_all('table')
	rows = [table_row for table in tables for table_row in list(parse_table(table))]
	for row in rows:
		if instance_column in row and row[instance_column]:
			try:
				yield (row[instance_column], get_ec2_data(row))
			except Exception as e:
				print('Could not process', row[instance_column], e)

def parse_emr_hadoop_task_config_section(section):
	instance = section.find('div',class_='title').text
	try:
		rows = list(parse_table(section,skip_tr=1))
		values = { row['Configuration Option']: row['Default Value'] for row in rows }
		return (instance, values)
	except Exception as e:
		print('Could not process', instance, e)

def fetch_emr_data(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	sections = soup.find_all('div', class_='table-container')
	for section in sections:
		yield parse_emr_hadoop_task_config_section(section)

def merge_dictionaries(dict_a, dict_b):
	keys_a = set(dict_a.keys())
	keys_b = set(dict_b.keys())
	intersection = keys_a & keys_b
	return { i: {**dict_a[i], **dict_b[i]} for i in intersection}

curr_gen_ec2_it = fetch_ec2_data("https://aws.amazon.com/ec2/instance-types","Instance")
prev_gen_ec2_it = fetch_ec2_data("https://aws.amazon.com/ec2/previous-generation","Instance Type")
emr_it = fetch_emr_data("https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-hadoop-task-config.html")
ec2 = dict(list(curr_gen_ec2_it) + list(prev_gen_ec2_it))
emr = dict(list(emr_it))
state = merge_dictionaries(ec2,emr)

with open('state.json', 'w') as f:
    json.dump(state, f)