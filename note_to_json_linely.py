












import os, re, json
import meilisearch

index_id = 'linely'

for file in os.listdir():
    # print(file)
    if '.txt' in file:
        with open(file, 'r', encoding = 'utf-8') as f:
            note_content = f.read()
            # print(note_content)
        pattern = re.compile(r'\d{,2}月\d{,2}日[\w\W]+?(?=\d{,2}月\d{,2}日)')
        records = re.findall(pattern, note_content)
        # print(records)

        records_list = []
        id_num = 0
        for record in records:
            pattern = re.compile(r'\d{,2}月\d{,2}日')
            date = re.findall(pattern, record)[0]
            lines = record.split('\n')
            for line in lines:
                records_list.append({
                'id': id_num,
                'date':date,
                'content':line})
                id_num += 1
            
        print(records_list)
        
        with open( index_id + '.json','w',encoding = 'utf-8') as f:
            json.dump(records_list, f, indent= 4, ensure_ascii=False)

        client = meilisearch.Client('http://127.0.0.1:5000')
        json_file = open( index_id + '.json', encoding = 'utf-8')
        data = json.load(json_file)
        print(data)
        client.index( index_id ).add_documents(data)
