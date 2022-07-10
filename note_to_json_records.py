












import os, re, json

for file in os.listdir():
    # print(file)
    if '.txt' in file:
        with open(file, 'r', encoding = 'utf-8') as f:
            note_content = f.read()
            # print(note_content)
        pattern = re.compile(r'\d{,2}月\d{,2}日[\w\W]+?(?=\d{,2}月\d{,2}日)')
        records = re.findall(pattern, note_content)
        print(records)

        records_list = []
        id_num = 0
        for record in records:
            records_list.append({
                'id': id_num,
                'content':record})
            id_num += 1
        print(records_list)
        
        with open('records_list_json.json','w') as f:
            json.dump(records_list, f, indent= 4)
