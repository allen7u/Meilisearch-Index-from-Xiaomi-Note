












import os, re, json
import meilisearch
import html

daily_index_id = 'daily'
linely_index_id = 'linely'
daily_id_num = 0
linely_id_num = 0
daily_list = []
lines_list = []
path = 'F:\\Anaconda_Play\\小米便签批量导出\\2022-7-29-2\\sub'
path = 'F:\\Anaconda_Play\\小米便签批量导出\\2022-7-29-2\\'
for file in os.listdir(path):
    # print(file)
    if not '.txt' in file:
        continue
    with open(path + '\\' + file, 'r', encoding='utf-8') as f:
        note_content = f.read()
    # Convert all named and numeric character references (e.g. &gt;, &#62;, &#x3e;) in the string s to the corresponding Unicode characters
    note_content = html.unescape(note_content)

    note_content = re.sub(r'(\d{1,2}月\d{1,2}日)','$$$\n'+r'\1',note_content)
    
    for day in note_content.split('$$$\n'):
        # print(day)
        pattern = re.compile(r'\d{,2}月\d{,2}日')
        date = re.findall(pattern, day)
        if not date:
            continue # 如果没有日期，则跳过
        date = re.findall(pattern, day)[0] # 取出日期
        day = re.sub(r'\n','__LINEBREAK__', day) # 替换换行符

        daily_list.append({
            'id': daily_id_num,
            'date':date,
            'file_name': file,
            'content':day})
            # 'content':'<div>' + day + '</div>'})
        daily_id_num += 1

        for line in day.split('__LINEBREAK__'): 
            lines_list.append({     
                'id': linely_id_num,        
                'day_index': daily_id_num - 1,          
                'date':date,            
                'file_name': file,  
                'content':line})    
            linely_id_num += 1  

# print(daily_list) 
client = meilisearch.Client('http://127.0.0.1:7700')      

with open( daily_index_id + '.json','w', encoding = 'utf-8') as f:            
    json.dump(daily_list, f, indent= 4, ensure_ascii=False)     

with open( daily_index_id + '.json', encoding = 'utf-8')  as f:     
    data = json.load(f)     
    client.index( daily_index_id ).add_documents(data)  

with open( linely_index_id + '.json','w', encoding = 'utf-8') as f:     
    json.dump(lines_list, f, indent= 4, ensure_ascii=False)     

with open( linely_index_id + '.json', encoding = 'utf-8')  as f:        
    data = json.load(f)         
    client.index( linely_index_id ).add_documents(data)     





#参考，备用：
# client.index('movies').add_documents([{
# 'id': 287947,
# 'title': 'Shazam',
# 'poster': 'https://image.tmdb.org/t/p/w1280/xnopI5Xtky18MPhK40cZAGAOVeV.jpg',
# 'overview': 'A boy is given the ability to become an adult superhero in times of need with a single magic word.',
# 'release_date': '2019-03-23'
# }])