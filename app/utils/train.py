import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from app.models import outcome
import csv
import json

def train():
    # 读取数据
    path = './app/dataset/train_in_use.csv'
    data = pd.read_csv(path)
    data.fillna(0,inplace=True)
    df=data
    df.replace('nan', 0, inplace=True)
    dataset=df
    dataset = dataset.drop(
        ['feature1', 'feature20', 'feature32', 'feature54', 'feature57', 'feature60', 'feature64', 'feature65', 'feature77',
        'feature78', 'feature80', 'feature88', 'feature92', 'feature100'], axis=1)  # 删除特定列
    # 数据预处理 选择自变量x 因变量y
    X = dataset.iloc[:, 1:-1].values
    y = dataset.iloc[:, -1].values
    # 将数据集拆分为训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1341)
    # 数据标准化 特征标度
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    classifier = RandomForestClassifier(n_estimators=71, criterion='gini', max_depth=55, min_samples_split=4,
                                        max_leaf_nodes=500, max_features=60, random_state=1341)
    classifier.fit(X_train, y_train)
    train_accuracy = classifier.score(X_test, y_test)  #模型的准确度

    # save model
    joblib.dump((classifier, scaler), "./app/models/model_alpha.joblib")
    return train_accuracy

def predict(path):
    #删除原有结果表中的所有旧内容
    outcome.objects.all().delete()
    
    # 加载已经训练好的模型
    model, scaler = joblib.load('./app/models/model_alpha.joblib')

    from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

    data = pd.read_csv(path)
    data.fillna(0,inplace=True)
    df=data
    df.replace('nan', 0, inplace=True)
    dataset=df
    y = dataset.iloc[:, -1].values
    dataset = dataset.drop(
        ['feature1', 'feature20', 'feature32', 'feature54', 'feature57', 'feature60', 'feature64', 'feature65', 'feature77',
        'feature78', 'feature80', 'feature88', 'feature92', 'feature100', 'sample_id', 'label'], axis=1)  # 删除特定列
    dataset = scaler.transform(dataset)

    # 预测结果
    y_pred = model.predict(dataset)
    print(y_pred)

    f = open('./app/to_download/outcome.csv','w',newline="")
    csv_writer = csv.writer(f)
    csv_writer.writerow(["样本id","预测结果"])


    #将新的结果存入数据库中的表和供用户下载的表中
    for i in range(0,len(data)):
        outcome.objects.create(sample_id=i,label=y_pred[i])
        csv_writer.writerow([i,y_pred[i]])
    f.close()
    queryset = outcome.objects.all()

    # # 创建一个空字典来保存序号和预测结果
    # result_dict = {}
    # y_pred_list = y_pred.tolist()
    # # 枚举预测结果并保存到字典中
    # for i, pred in enumerate(y_pred_list):
    #     result_dict[i] = pred
    # # 将字典转换为JSON字符串
    # json_str = json.dumps(result_dict)
    # # 将JSON字符串写入文件
    # with open('./app/jsons/predictions.json', 'w') as file:
    #     file.write(json_str)

    # 查看模型准确度
    confusion_matrix = confusion_matrix(y, y_pred)
    report = classification_report(y, y_pred, output_dict=True)
    accuracy_score = round(accuracy_score(y, y_pred),2)   #准确度

    macro_precision = report['macro avg']['precision']
    macro_recall = report['macro avg']['recall']
    f1 = 2 * (macro_precision * macro_recall) / (macro_precision + macro_recall)  
    macro_f1 = round(100 * f1,2)                #macro_f1得分
    return accuracy_score,macro_f1,queryset