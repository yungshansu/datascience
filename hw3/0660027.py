from sklearn import datasets
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import f1_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.svm import SVC
import matplotlib.pylab as plt
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.decomposition import PCA
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier
import pickle
import pandas as pd
import numpy as np

def param_selection(x_train, x_test, y_train, y_test):
    tuned_parameters = {'max_depth': [4],
                        'gamma':[1],
                        'subsample':[0.6,0.8,1],
                        'colsample_bytree':[0.6,0.8,1]
                        }#[0.01, 0.1, 1, 10,100]
    scores = ['f1']
    for score in scores:
        clf = GridSearchCV(XGBClassifier(learning_rate=0.1,
                           n_estimators=1000,
                            max_depth=10,
                            gamma=0.001,
                           subsample=1,
                           num_class = 2,
                           objective='multi:softmax',
                           scale_pos_weight=3,
                           random_state=0,
                           n_jobs = 6,
                           importance_type="total_cover"),
                           tuned_parameters,
                           cv=3,
                           scoring='%s_micro' % score)
        print ("Start to train")
        clf.fit(x_train, y_train)
        print ("Finish train")
        print ("--------------Train data evaluation------------------")
        for par, mean_validation_score, cv_validation_scores in clf.grid_scores_ :
            print(str(par) + "  " + str(mean_validation_score) + "  " + str(cv_validation_scores))

        print ("--------------Test data evaluation------------------")
        y_true, y_pred = y_test, clf.predict(x_test)
        print(classification_report(y_true, y_pred))

        print(clf.best_estimator_)



def model_evaluate(train_pred, train_gd, test_pred, test_gd):
    print ("---------------------Training result-----------------------")
    precision, recall, fscore, support = precision_recall_fscore_support(
        train_gd,
        train_pred,
        # average = "micro"
    )
    print ("Precision : " + str(precision))
    print ("recall :" + str(recall))
    print ("fscore :" + str(fscore))
    print ("---------------------Testing data evaluation ---------------------")
    precision, recall, fscore, support = precision_recall_fscore_support(
        test_gd,
        test_pred,
        # average = "micro"
    )
    print ("Precision : " + str(precision))
    print ("recall :" + str(recall))
    print ("fscore :" + str(fscore))
    # print ("Support:" + str(support))
    # fscore = f1_score(test_pred, test_gd, average='micro')


def main():
    pred_test = True
    model_file_name = "rfc.pickle"
    label_en_list = [None] * 14
    onehot_en = [None] * 14
    Normalizer_list = [None] * 14
    pca_list = [None] * 14
    """Preprocess data"""
    data = pd.read_csv('train.csv',header=None)
    label = data.iloc[:,[14]].values
    label = label.flatten()
    # label[label==0] = -1

    ignore_set = set([2])#set([8,5,3,13])
    need_labelencode = set([1,3,5,6,7,8,9,13])
    need_onehotencode = set([])
    # star_featureset = set([6,7,10])
    # need_onehot = set(6,7,13])



    #Onehot encoder
    feature1 = np.array(data.iloc[:,[0]].values)
    Normalizer_list[0] = StandardScaler()
    # feature1 = Normalizer_list[0].fit_transform(feature1)
    features = np.array(feature1)
    test_label_encoder = LabelEncoder()
    for i in range(1,14):
        if i in ignore_set:
            continue
        if i in need_labelencode:
            feature = data.iloc[:,[i]].values
            label_en_list[i] = LabelEncoder()
            feature = label_en_list[i].fit_transform(feature).reshape(-1,1)
            features = np.hstack((features,feature))

        else:
            Normalizer_list[i] = StandardScaler()
            feature = np.array(data.iloc[:,[i]].values)
            # feature = Normalizer_list[i].fit_transform(feature)
            features = np.hstack((features,feature))



    # """Normalize data"""
    df = pd.DataFrame(label)
    df.to_csv("label.csv")

    df = pd.DataFrame(features[:][:])
    df.to_csv("log.csv")
    # """Decompose data"""
    # pca = PCA(n_components=40)
    # features = pca.fit_transform(features)
    # df = pd.DataFrame(features[0:10][:])
    # df.to_csv("log2.csv")

    """Split data to train and test"""
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        label,
        random_state=0,
        test_size=0.1)

    df = pd.DataFrame(x_train)
    df.to_csv("x_train.csv")

    df = pd.DataFrame(y_train)
    df.to_csv("y_train.csv")
    """Predict test data"""
    if pred_test == True:
        data_test = pd.read_csv('test.csv',header=None)
        feature1_test = np.array(data_test.iloc[:,[0]].values)
        # feature1_test = Normalizer_list[0].transform(feature1_test)
        features_test = np.array(feature1_test)
        for i in range(1,14):
            if i in ignore_set:
                continue
            if i in need_labelencode:
                feature = data_test.iloc[:,[i]]
                feature = label_en_list[i].transform(feature.values)
                # feature = onehot_en[i].transform(feature.reshape(-1,1))
                # if i != 9: # sex
                #     feature = pca_list[i].transform(feature)
                features_test = np.hstack((features_test,feature))
            else:
                print i
                feature = np.array(data_test.iloc[:,[i]].values)
                # feature = Normalizer_list[i].transform(feature)
                features_test = np.hstack((features_test,feature))
        with open(model_file_name, 'rb') as f:

            model = pickle.load(f)
            id =np.arange(len(features_test))
            test_pred = model.predict(features_test)
            result = np.hstack((id.reshape(-1,1),test_pred.reshape(-1,1)))
            print np.shape(result)
            np.savetxt("ans.csv",result)
            df = pd.DataFrame(result)
            df.columns= ["ID","ans"]
            df.to_csv("ans.csv",index=False)
            return

    #svc_param_selection(x_train_std, x_test_std, y_train, y_test)
    """ SVM train"""
    #Train models
    # print ("SVM train")
    # svm = SVC(kernel = 'rbf', C=100, gamma=0.001, verbose=True)#
    # svm.fit(x_train, y_train)
    # y_train_pred = svm.predict(x_train)
    # y_test_pred = svm.predict(x_test)
    # model_evaluate(y_train_pred, y_train, y_test_pred, y_test)


    # """AdaBoost classifier"""
    # print ("Adaboost train")
    # adaboost = AdaBoostClassifier(
    #     base_estimator = DecisionTreeClassifier(max_depth=15,splitter="random",criterion="entropy",class_weight={0: 1, 1: 2}),
    #     n_estimators=500,
    #     learning_rate=0.5,
    #     random_state=10)
    # adaboost.fit(x_train, y_train)
    # y_train_pred = adaboost.predict(x_train)
    # y_test_pred = adaboost.predict(x_test)
    # model_evaluate(y_train_pred, y_train, y_test_pred, y_test)
    # with open(model_file_name, 'wb') as f:
    #     pickle.dump(adaboost, f)

    # """GradientBoostingClassifier"""
    # print ("GradientBoostingClassifier train")
    # gdbc = GradientBoostingClassifier(n_estimators=300, learning_rate=0.01,
    #     max_depth = 10, random_state=0,verbose=True)
    # gdbc.fit(x_train_std, y_train)
    # y_train_pred = gdbc.predict(x_train_std)
    # y_test_pred = gdbc.predict(x_test_std)
    # model_evaluate(y_train_pred, y_train, y_test_pred, y_test)
    # with open(model_file_name, 'wb') as f:
    #     pickle.dump(gdbc, f)

    """Random forest tree"""
    # print ("Random forest tree")
    #
    # rfd = RandomForestClassifier(n_estimators=200, max_depth=15, n_jobs=4, class_weight={0:1,1:2}, verbose=True,criterion="entropy")#
    # rfd.fit(x_train, y_train)
    # y_train_pred = rfd.predict(x_train)
    # y_test_pred = rfd.predict(x_test)
    # model_evaluate(y_train, y_train_pred, y_test, y_test_pred)
    # with open(model_file_name, 'wb') as f:
    #     pickle.dump(rfd, f)


    """xgboost"""
    # param_selection(x_train, x_test, y_train, y_test)
    # print ("xgboost")
    #0.87647
    xgb = XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
       colsample_bytree=1, gamma=1, importance_type='total_cover',
       learning_rate=0.1, max_delta_step=0, max_depth=4,
       min_child_weight=1, missing=None, n_estimators=1000, n_jobs=6,
       nthread=None, num_class=2, objective='multi:softmax',
       random_state=0, reg_alpha=0, reg_lambda=1, scale_pos_weight=3,
       seed=None, silent=True, subsample=1)
    #0.87588
    # xgb = XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
    #    colsample_bytree=0.7, gamma=1, importance_type='total_cover',
    #    learning_rate=0.1, max_delta_step=0, max_depth=4,
    #    min_child_weight=1, missing=None, n_estimators=1000, n_jobs=6,
    #    nthread=None, num_class=2, objective='multi:softmax',
    #    random_state=0, reg_alpha=0, reg_lambda=1, scale_pos_weight=3,
    #    seed=None, silent=True, subsample=1)



    xgb.fit(x_train, y_train, eval_set = [(x_test,y_test)],eval_metric = "mlogloss",
               early_stopping_rounds = 10, verbose = True)
    y_train_pred = xgb.predict(x_train)
    y_test_pred = xgb.predict(x_test)
    model_evaluate(y_train, y_train_pred, y_test, y_test_pred)
    with open(model_file_name, 'wb') as f:
        pickle.dump(xgb, f)

if __name__ == '__main__':
    main()
