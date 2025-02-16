from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import json

def load_data(data_path):
    if data_path.endswith(".json"):
        #with open(data_path, "r",encoding='utf-8') as fin:
        with open(data_path, "r") as fin:
            data = json.load(fin)
    elif data_path.endswith(".jsonl"):
        data = []
        with open(data_path, "r") as fin:
            for k, example in enumerate(fin):
                example = json.loads(example)
                #print("example:",example)
                data.append(example)
    return data


# 将距离转换为相似度分数
#similar_scores = []
#dissimilar_scores = []

#similar_scores = [2.3,2.2,2.1,2.123,1.8,19,2.0]
#dissimilar_scores = [0.5,0.6,0.7,0.9,1.0,1.1123,1.342,1.4342,0.6534]

# neg_data=load_data("neg.jsonl")[0]['ctxs']
# dissimilar_scores=[float(i['score']) for i in neg_data]


dissimilar_scores=[]
pos_data=load_data("neg.jsonl")
for i in pos_data:
    for j in i['ctxs']:
        dissimilar_scores.append(float(j['score']))
dissimilar_scores.sort()
similar_scores=dissimilar_scores


similar_scores=[]
pos_data=load_data("pos.jsonl")
for i in pos_data:
    for j in i['ctxs']:
        similar_scores.append(float(j['score']))
similar_scores.sort()
similar_scores=similar_scores

# 合并数据
scores = similar_scores + dissimilar_scores
labels = [1] * len(similar_scores) + [0] * len(dissimilar_scores)

# 计算ROC曲线
fpr, tpr, thresholds = roc_curve(labels, scores)
roc_auc = auc(fpr, tpr)

# 绘制ROC曲线
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right")
plt.show()

maxindex = (tpr-fpr).tolist().index(max(tpr-fpr))
threshold = thresholds[maxindex]
print(threshold)
