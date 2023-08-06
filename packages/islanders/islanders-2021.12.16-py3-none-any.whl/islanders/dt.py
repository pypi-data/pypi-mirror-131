import pandas as pd
import numpy as np
import islanders as ir
import irdatacleaning
from sklearn.model_selection import train_test_split
from sklearn import model_selection
import sklearn.tree as tree

class DT:
    def __init__(self,*array,criterion = None,max_depth = None,min_samples_leaf = None,train_size=0.2):
        self.X_data = array[0]
        self.y_data = array[1]
        self.X_train,self.X_test, self.y_train,self.y_test = train_test_split(array[0],array[1],train_size=train_size)
        length_dt = tree.DecisionTreeClassifier()
        length_dt.fit(self.X_train,self.y_train)
        self.unique, counts = np.unique(self.y_train, return_counts=True)
        self.params_dt = {'criterion':['gini','entropy'],
                          'max_depth':[i for i in range(1,length_dt.get_depth()*2)],
                          'min_samples_leaf':list(range(2,length_dt.get_n_leaves()*2,2))}
        # self.number_of_category = number_of_category
        # self.cv = round()
    def acc(self):
        dt = tree.DecisionTreeClassifier()
        dt_opt = model_selection.GridSearchCV(dt,self.params_dt,cv = 4)


        # fit the model and optimize
        dt_opt.fit(self.X_train,self.y_train)

        # store the resutl sin a dataframe
        results = pd.DataFrame(dt_opt.cv_results_)
        ranking = np.array(results.rank_test_score.sort_values().index)
        top = {"rank":[],
               "score":[],
               "time":[],
               "stats":[]}
        for i in range(0,5):
            top["rank"].append(results["rank_test_score"][ranking[i]])
            top["score"].append(results["mean_test_score"][ranking[i]])
            top["time"].append(results["mean_score_time"][ranking[i]])
            top["stats"].append(results["params"][ranking[i]])
        not_num_1 = []
        columns = top.keys()
        for  i in range(len(top["rank"])):
            if top["rank"][i] >1:
                not_num_1.append(i)
        if len(not_num_1)!=0:
            for i in reversed(not_num_1):
                for j in columns:
                    top[j].pop(i)
        if len(top["rank"])>1:
            #     print(len(top))
            top_1 = pd.DataFrame(data = top, columns = columns)
            #     print(top_1)
            best_score = top_1.score.sort_values()
            #     print(best_score)
            if best_score[0]== best_score[1]:
                best_time = top_1.time.sort_values().index[0]
                best = top_1["stats"][best_time]
            #         print(best)
            else:
                best = top_1["stats"][top_1.score.sort_values().index]
        else:
            best = top["stats"][0]
        dt = tree.DecisionTreeClassifier(criterion = best["criterion"],max_depth = best["max_depth"],
                                         min_samples_leaf = best["min_samples_leaf"])
        return dt.fit(self.X_train,self.y_train)
if __name__ == "__main__":
    import pandas as pd
    import numpy as np
    import islanders as ir
    import irdatacleaning
    data = pd.read_csv("/Users/williammckeon/Sync/islander/dataset/amazon electronics.csv")
    name = [i for i in data.name]
    data.drop(columns = "name", inplace=True)
    data_x = np.array(data.iloc[:,:-1].values)
    data_y = np.array(data.iloc[:,-1].values)
    decsion = DT(data_x,data_y)
    bob = decsion.acc()
    print(bob.score(decsion.X_test,decsion.y_test))