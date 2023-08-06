# WoS Tab File

Extract information from the exported Web of Science's tab delimited text file

## Installation
```pip
pip install wos-tabfile
```

## Basic Usage
1. Retrieve publication year and numbers of citations in different indicators. 
```python
from wostabfile.core import WosTabFile
from collections import OrderedDict

# data source
root_path = "data/social network"
file_path = root_path + "/part1.txt"

# header fields in the text file
# Tag from: https://images.webofknowledge.com/images/help/WOS/hs_wos_fieldtags.html
wos_fields = ["PY", "NR", "TC", "U1", "U2"]
# load data by specific keys
wtf = WosTabFile(file_path=file_path)

table = wtf.generate_table(wos_fields)

print()
# group by year using count for numbers of publications per year
new_table=wtf.group_by(table,key_index=0,value_index=1,method="count")
new_table = OrderedDict(sorted(new_table.items()))

print("Year\tNumber of publication")
for year in new_table:
    print(f'{year}\t{new_table[year]}')

```

2. Retrieve keywords and its frequency from the bibliometric data

```python
from wostabfile.core import WosTabFile
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

root_path = "data/social network"
wos_fields = ["DE"]
wtf = WosTabFile(file_path=root_path)
dict_words={}

def singularize(text):
    wnl = WordNetLemmatizer()
    tokens = [token.lower() for token in word_tokenize(text)]
    lemmatized_words = [wnl.lemmatize(token) for token in tokens]
    return (' '.join(lemmatized_words)).strip()

def process_row(rows):
    global dict_words
    for ks in rows:
        wlist=ks[0]
        for w in wlist.split(";"):
            w=w.strip()
            if w=="":
                continue
            w=singularize(w)
            if w not in dict_words.keys():
                dict_words[w]=1
            else:
                dict_words[w]+=1

table = wtf.generate_table_by_folder(wos_fields,func=process_row)
dict_words =  dict(sorted(dict_words.items(),reverse=True, key=lambda item: item[1]))

print("Word\tTerm Count")
for k in list(dict_words.keys())[:20]:
    print(f'{k}\t{dict_words[k]}')
print()
print("Number of unique words: ",len(dict_words.keys()))

```

Sample bibliometric data in the above examples can be downloaded in this 
[link](https://github.com/dhchenx/dhchenx.github.io/blob/master/projects/wos-tabfile/social-network.zip?raw=true).

## License
The `wos-tabfile` project is provided by [Donghua Chen](https://github.com/dhchenx). 

