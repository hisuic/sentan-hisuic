# source: https://qiita.com/y_itoh/items/fa04c1e2f3df2e807d61

import re
import zipfile
import urllib.request
import os.path
import glob

# URL of the book
URL = 'https://www.aozora.gr.jp/cards/000081/files/43737_ruby_19028.zip'

# Def for getting zipfile and unzipping
def download(URL):
    zip_file = re.split(r'/', URL)[-1] #1
    urllib.request.urlretrieve(URL, zip_file) #2
    dir = os.path.splitext(zip_file)[0] #3

    with zipfile.ZipFile(zip_file) as zip_object: #4
        zip_object.extractall(dir) #5

    os.remove(zip_file) #6

    path = os.path.join(dir,'*.txt') #7
    list = glob.glob(path) #8
    return list[0] #9

def convert(download_text):
    data = open(download_text, 'rb').read() #➀
    text = data.decode('shift_jis') #➁

    # 本文抽出
    text = re.split(r'\-{5,}', text)[2] #➂  
    text = re.split(r'底本：', text)[0] #➃
    text = re.split(r'［＃改ページ］', text)[0] #➄

    # ノイズ削除
    text = re.sub(r'《.+?》', '', text) #➅
    text = re.sub(r'［＃.+?］', '', text) #➆
    text = re.sub(r'｜', '', text) #➇
    text = re.sub(r'\r\n', '', text) #➈
    text = re.sub(r'\u3000', '', text) #➉   

    return text

download_file = download(URL)
text = convert(download_file)

print(text)

# MeCabによる「分かち書き」
import MeCab

mecab = MeCab.Tagger("-Owakati")
text = mecab.parse(text)

# print(text)

# use split
separated_text = text.split()
#print(separated_text)

# output result data
with open('output.txt', 'w') as f:
    f.write(text)

# download file from colaboratory to local
# from google.colab import files
#
# files.download('output.txt')
