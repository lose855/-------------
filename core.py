import folium
import json
import pandas as pd
import warnings
import os
import xml.etree.ElementTree as elemTree

warnings.filterwarnings('ignore')

options = elemTree.parse('./users.xml')
user = options.find('./user')
state_dir = user.find('state_dir').text
data_dir = user.find('data_dir').text
image_dir = user.find('image_dir').text
column_names = user.find('column_names').text.split(',')
zoom_scale = int(user.find('zoom_scale').text)
tiles = user.find('tiles').text
fill_opacity = float(user.find('fill_opacity').text)
line_opacity = float(user.find('line_opacity').text)
bins = list(map(int, user.find('bins').text.split(',')))
legend_name = user.find('legend_name').text
color_type = user.find('color_type').text
data_list = os.listdir(r'./data/')
state_list = json.load(open(state_dir))
state_list_converted = {"type":"FeatureCollection","features":[]}

print('총 {}개의 파일이 감지되었습니다.'.format(len(data_list)))
print('성능 지표: {}'.format(column_names[-1]))
print('확대 비율: {}'.format(zoom_scale))
print('컬러 색상: {}'.format(color_type))
print('생성을 시작합니다.')

for data in data_list:
    result = pd.read_csv(data_dir.format(data))
    result = pd.DataFrame(columns=column_names, data=result.iloc[:, [0, 6]].values.tolist())
    result_state_list = [result[['State']].iloc[i].values[0] for i in range(result[['State']].shape[0])]

    for state_data in state_list['features']:
        if state_data['properties']['name'] in result_state_list:
            state_list_converted['features'].append(state_data)

    map = folium.Map(location=[40, -102], tiles=tiles, zoom_start=zoom_scale)
    map.choropleth(geo_data=state_list_converted, data=result,
                 columns=column_names,
                 key_on='feature.properties.name',
                 fill_color=color_type, fill_opacity=fill_opacity, line_opacity=line_opacity, bins=bins,
                 legend_name=legend_name)

    map.save(image_dir.format(data.replace('.csv', '')))
    print('{} 저장되었습니다.'.format(data))

print('완료되었습니다.\n')
print('Build by Choi young woo')
print('Version: {}'.format('2023-03-17'))

os.system("pause")