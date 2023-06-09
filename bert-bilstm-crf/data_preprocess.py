import json
import os
import random

DICT = ["纠纷当事人_被告","纠纷当事人_原告"]
medicine_dict = ['pro', 'dis', 'dru', 'bod', 'sym', 'mic', 'equ', 'ite', 'dep']

def data_process(data_dir,mode):
    for data_files in os.listdir(data_dir):
        label = ''
        data_path = os.path.join(data_dir,data_files)
        print(data_files)
        with open(data_path,'r',encoding="utf-8") as f:
            start,end =0,0
            json_data = json.load(f)
            #legaldata_type = json_data["type"]
            answers = json_data["answer"]
            for answer in answers:
                s_pos = random.randint(5,10)#扩展的长度
                e_pos = random.randint(5,10)

                start = answer["start_pos"]
                end = answer["end_pos"]
                write_data ={}
                if answer["type"] == DICT[1]:
                    label = "plaintiff"
                elif answer["type"] == DICT[0]:
                    label = "defendant"
                else:
                     break
                text = json_data["qwContent_pain"][int(start)-s_pos:int(end)+e_pos]#数据补长
                position = [[s_pos,len(text)-e_pos-1]]

                dict_con = {label:{answer["context"]:position}}
                write_data["text"] = text
                write_data["label"] = dict_con
                output_file = mode + '.json'
                with open(output_file,'a',encoding="utf-8") as w:
                    json.dump(write_data,w,ensure_ascii=False)
                    w.writelines("\n")

def data_process_test(data_dir,mode):
    id = 0
    for data_files in os.listdir(data_dir):
        label = ''
        data_path = os.path.join(data_dir,data_files)
        print(data_files)
        with open(data_path,'r',encoding="utf-8") as f:
            start,end =0,0
            json_data = json.load(f)
            #legaldata_type = json_data["type"]
            answers = json_data["answer"]
            for answer in answers:
                s_pos = random.randint(5,10)#扩展的长度
                e_pos = random.randint(5,10)

                start = answer["start_pos"]
                end = answer["end_pos"]
                write_data ={}
                text = json_data["qwContent_pain"][int(start)-s_pos:int(end)+e_pos]#数据补长
                text = text.replace("\n","").replace("\t","")
                write_data["id"] = id
                id = id +1
                write_data["text"] = text
                output_file = mode + '.json'
                with open(output_file,'a',encoding="utf-8") as w:
                    json.dump(write_data,w,ensure_ascii=False)
                    w.writelines("\n")

def find_types_num(file_path):
    with open(file_path,'r',encoding="utf-8") as f:
        entity_list = []
        json_datas = json.load(f)
        for json_data in json_datas:
            entities = json_data["entities"]
            for entity in entities :
                entity_type = entity["type"]
                #print(entity_type)
                if entity_type not in entity_list:
                    entity_list.append(entity_type)
        print(entity_list)
                
def medicine_preprocess(file_path,mode):
    with open(file_path,'r',encoding="utf-8") as f :
        json_datas = json.load(f)

        for json_data in json_datas:
            text = json_data["text"]
            entities = json_data["entities"]
            content = {}
            type_list = []
            for entity in entities:
                start_pos,end_pos = entity["start_idx"],entity["end_idx"]
                position = [[start_pos,end_pos]]
                entity_type = entity["type"]
                entity_entity = entity["entity"]
                combine = {}
                combine[entity_entity] = position
                if entity_type not in type_list:
                    type_list.append(entity_type)
                    content[entity_type] = combine
                #如果是同一个type,需要将值拼接起来
                else:
                    #取出原有的加上现在
                    for i in range(len(type_list)):
                        if entity_type == type_list[i]:
                            dict_con = content[entity_type]
                            dict_con[entity_entity] = position
                            content[entity_type] = dict_con
                        else:
                            break

            write_data ={}
            write_data["text"] = text
            write_data["label"] = content
            output_file = mode + '.json'
            with open(output_file,'a',encoding="utf-8") as w:
                json.dump(write_data,w,ensure_ascii=False)
                w.writelines("\n")


def medicine_test_preprocess(file_path):
    id = 0
    with open(file_path,"r",encoding="utf-8") as f:
        json_datas = json.load(f)

        for json_data in json_datas:
            text = json_data["text"]
            write_data ={}
            write_data["id"] = id
            id = id +1
            write_data["text"] = text
            output_file ='dev_medicine.json'
            with open(output_file,'a',encoding="utf-8") as w:
                json.dump(write_data,w,ensure_ascii=False)
                w.writelines("\n")

# {"address": {"松坪村": [[30, 32]], "深康村": [[36, 38]]}, "government": {"深圳市人大常委会": [[0, 7]]}}
#{"pro": {"房室结消融": [[3, 7]], "起搏器植入": [[9, 13]]}}
#{"pro": {"房室结消融": [[3, 7]], "起搏器植入": [[9, 13]], "替代疗法": [[35, 38]]}, "dis": {"反复发作或难治性心房内折返性心动过速": [[16, 33]]}}



if __name__ == "__main__":
    #data_process("D:/IDMDownload/Compressed/第五次交付全量数据/第五次交付全量数据/1","train")
    #data_process_test("D:/IDMDownload/Compressed/第五次交付全量数据/第五次交付全量数据/test","test")
    #data_process("D:/IDMDownload/Compressed/第五次交付全量数据/第五次交付全量数据/valid","dev_legal")
    #find_types_num("CMeEE-V2_train.json")
    medicine_preprocess("CMeEE-V2_test.json","test")
    #medicine_test_preprocess("CMeEE-V2_test.json")

