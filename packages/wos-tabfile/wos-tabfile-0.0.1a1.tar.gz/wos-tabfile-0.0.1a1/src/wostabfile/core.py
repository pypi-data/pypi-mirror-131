# Tags: https://images.webofknowledge.com/images/help/WOS/hs_wos_fieldtags.html
import csv
import os
import numpy as np

class WosTabFile:
    def __init__(self,file_path):
        self.file_path=file_path

    def generate_table(self,wos_fields,specific_file=None,keyword_func=None):
        # print('\t'.join(headers))
        list_row=[]
        current_path=self.file_path
        if specific_file!=None:
            current_path=specific_file
        with open(current_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t')
            for row in reader:
                list_value=[]
                for wf in wos_fields:
                    list_value.append(row[wf])
                if keyword_func!=None:
                    keyword_func(list_value)
                list_row.append(list_value)
                # print('\t'.join(list_value))
        return list_row

    def generate_table_by_folder(self,wos_field,func=None):
        list_all_row=[]
        for file in os.listdir(self.file_path):
            if file.endswith(".txt"):
                full_filepath = os.path.join(self.file_path, file)
                list_row = self.generate_table(wos_field, full_filepath)
                list_all_row = list_all_row + list_row
                if func!=None:
                    func(list_row)
        return list_all_row

    def group_by(self,table,key_index,value_index,method,remove_empty=True):
        dict_table= {}
        for row in table:
            key=row[key_index]
            if remove_empty:
                if str(key).strip()=="":
                    continue
            if key in dict_table.keys():
                dict_table[key].append(row[value_index])
            else:
                dict_table[key]=[row[value_index]]
        dict_new_table= {}
        for key in dict_table:
            if key==None:
                continue
            values=dict_table[key]
            value=0
            if method=="sum":
                values = [float(v) for v in values]
                value=sum(values)
            elif method=="avg":
                values = [float(v) for v in values]
                value=np.mean(values)
            elif method=="max":
                values = [float(v) for v in values]
                value=max(values)
            elif method=="min":
                values = [float(v) for v in values]
                value=min(values)
            elif method=="count":
                value=len(values)

            dict_new_table[key]=value
        return dict_new_table

if __name__=="__main__":
    root_path = "../datasets/perspectives/metaverse_itself"
    file_path = root_path + "/metaverse1.txt"

    headers = ["Year", 'WoS Core Collection Times Cited Count', 'Total Times Cited Count',
               'Usage Count (Last 180 Days)', 'Usage Count (Since 2013)']

    wos_fields = ["PY", "NR", "TC", "U1", "U2"]

    wtf = WosTabFile(file_path=file_path)

    table = wtf.generate_table(wos_fields)

    print()
    print('\t'.join(headers))
    for row in table:
        print('\t'.join(row))



