import MeCab
import json

input_file_path = "output.txt"

output_file_path = "word_dictionary.json"

with open(input_file_path, "r", encoding="utf-8") as file:
    text = file.read()

words = text.split()

mecab = MeCab.Tagger()

word_pos_dict = {}

for word in words:
    node = mecab.parseToNode(word)
    while node:
        if node.surface:
            word_pos_dict[node.surface] = node.feature.split(",")[0]
        node = node.next

with open(output_file_path, "w", encoding="utf-8") as f:
    json.dump(word_pos_dict, f, ensure_ascii=False, indent=4)
