from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from datasets import load_dataset, Dataset

# データセットのロードと前処理
# 日本人の英文データとネイティブの英文データをそれぞれ用意
japanese_texts = ["日本人が書いた英文1", "日本人が書いた英文2", ...]
native_texts = ["ネイティブが書いた英文1", "ネイティブが書いた英文2", ...]

# ラベル付け
texts = japanese_texts + native_texts
labels = [0] * len(japanese_texts) + [1] * len(native_texts)

# データフレームに変換
import pandas as pd
df = pd.DataFrame({'text': texts, 'label': labels})

# データセットをトレイン・テストに分割
train_texts, test_texts, train_labels, test_labels = train_test_split(df['text'], df['label'], test_size=0.2)

# Datasetオブジェクトに変換
train_dataset = Dataset.from_dict({'text': train_texts, 'label': train_labels})
test_dataset = Dataset.from_dict({'text': test_texts, 'label': test_labels})

# トークナイザーとモデルの準備
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)

# トークン化
def preprocess_function(examples):
    return tokenizer(examples['text'], truncation=True, padding=True)

train_dataset = train_dataset.map(preprocess_function, batched=True)
test_dataset = test_dataset.map(preprocess_function, batched=True)

# トレーニングの設定
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
)

# トレーナーの設定
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

# モデルの訓練
trainer.train()

# モデルの評価
trainer.evaluate()

