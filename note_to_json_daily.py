












import os, re, json
import meilisearch

index_id = 'daily'
index_id = 'all'
index_id = 'all_line_break'
id_num = 0
records_list = []
path = 'F:\\Anaconda_Play\\小米便签批量导出\\2022-7-29-2\\sub'
path = 'F:\\Anaconda_Play\\小米便签批量导出\\2022-7-29-2\\'
for file in os.listdir(path):
    # print(file)
    if not '.txt' in file:
        continue
    with open(path + '\\' + file, 'r', encoding='utf-8') as f:
        note_content = f.read()
        # print(note_content)
    content_ = re.sub(r'(\d{1,2}月\d{1,2}日)','$$$\n'+r'\1',note_content)
    # print(content_)
    # segments = re.split('$$$','123 $$$ 456')
    records = content_.split('$$$\n')

    # pattern = re.compile(r'\d{,2}月\d{,2}日[\w\W]+?(?=\d{,2}月\d{,2}日)')
    # records = re.findall(pattern, note_content)
    # print(records)

    for record in records:
        # print(record)
        pattern = re.compile(r'\d{,2}月\d{,2}日')
        date = re.findall(pattern, record)
        if not date:
            continue
        date = re.findall(pattern, record)[0]
        record = re.sub(r'\n','__LINEBREAK__', record)

        records_list.append({
            'id': id_num,
            'date':date,
            'file_name': file,
            'content':record})
            # 'content':'<div>' + record + '</div>'})
        id_num += 1

# print(records_list)
    
with open( index_id + '.json','w', encoding = 'utf-8') as f:
    json.dump(records_list, f, indent= 4, ensure_ascii=False)

client = meilisearch.Client('http://127.0.0.1:7700')
json_file = open( index_id + '.json', encoding = 'utf-8')
data = json.load(json_file)
# print(data)
client.index( index_id ).add_documents(data)


#参考，备用：
# client.index('movies').add_documents([{
# 'id': 287947,
# 'title': 'Shazam',
# 'poster': 'https://image.tmdb.org/t/p/w1280/xnopI5Xtky18MPhK40cZAGAOVeV.jpg',
# 'overview': 'A boy is given the ability to become an adult superhero in times of need with a single magic word.',
# 'release_date': '2019-03-23'
# }])