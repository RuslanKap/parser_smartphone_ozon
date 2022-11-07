import pandas as pn

raw_data = pn.read_csv('data_.csv')
os_os_ver = raw_data['OS_version'].value_counts().rename_axis('OS_version').reset_index(name='Amount')
print(os_os_ver)

