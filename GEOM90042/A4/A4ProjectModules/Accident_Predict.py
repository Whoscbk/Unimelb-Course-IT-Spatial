# Author:       Bingkun Ch
# Description:  This is th
# Written:      30/5/2020
# Last updated: 14/6/2020

import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler, OrdinalEncoder, OneHotEncoder
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression as LR
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR


class Accident_Predict:

    def get_train_data(self, acc_all):
        """
        This function is to get the original data for predictive modelling,
        and split them into x_train, x_predict and y_train.
        :param acc_all: pd.DataFrame
        :return: x_train, y_train, x_predict
        """
        try:
            acc_num = acc_all.copy()
            path1 = os.path.join(os.path.curdir,
                                 'add_dataset',
                                 'Weather_Condition.csv')

            path2 = os.path.join(os.path.curdir,
                                 'add_dataset',
                                 'future_weather.csv')

            weather_con = pd.read_csv(path1,
                                      sep=',',
                                      header=0)
            weather_predict = pd.read_csv(path2,
                                          sep=',',
                                          header=0)

            tab1 = pd.DataFrame(
                acc_num.groupby('ACCIDENT_D')['ACCIDENT_N'].count())
            tab1.reset_index(inplace=True)
            tab2 = weather_con.copy()

            tab1['Date'] = pd.to_datetime(tab1['ACCIDENT_D'])
            tab2['Date'] = pd.to_datetime(tab2['Date'])
            tab = pd.merge(tab1, tab2, on='Date')
            y_train = tab[['ACCIDENT_N']]
            x_train = tab[['Year', 'Month', 'Days',
                           'Max_temp', 'Min_temp',
                           'Rainfall', 'Solar_exposure']]
            x_predict = weather_predict.copy()
            return x_train, y_train, x_predict
        except OSError:
            print('Please check the file path')

    def fill_missing_value(self, table, col_name):
        """
        This function is to fill the missing value with median.
        :param table: pd.DataFrame
        :param col_name: string
        :return: x_fill
        """
        x_fill = table.copy()
        imp_median = SimpleImputer(strategy="median")
        x_fill.loc[:, [col_name]] = \
            imp_median.fit_transform(x_fill.loc[:, [col_name]])
        return x_fill

    def normalization(self, x_train, x_predict):
        """
        This function is to normalize the features by Min-Max scale.
        :param x_train: pd.DataFrame
        :param x_predict: pd.DataFrame
        :return: x_train_scale, x_predict_scale
        """
        x_train_scale = x_train.copy()
        x_predict_scale = x_predict.copy()
        fea_need_scale1 = x_train_scale.loc[:, ['Max_temp',
                                                'Min_temp',
                                                'Rainfall',
                                                'Solar_exposure']]
        fea_need_scale2 = x_predict_scale.loc[:, ['Max_temp',
                                                  'Min_temp',
                                                  'Rainfall',
                                                  'Solar_exposure']]
        scaler = MinMaxScaler()
        scaler.fit(fea_need_scale1)
        x_train_scale.loc[:, ['Max_temp',
                              'Min_temp',
                              'Rainfall',
                              'Solar_exposure']] = \
            scaler.transform(fea_need_scale1)
        x_predict_scale.loc[:, ['Max_temp',
                                'Min_temp',
                                'Rainfall',
                                'Solar_exposure']] = \
            scaler.transform(fea_need_scale2)
        return x_train_scale, x_predict_scale

    def ordinalEncode(self, x_train, x_predict):
        """
        This Function is to encode the discontinuous variable through
        OrdinalEncode method.
        :param x_train: pd.DataFrame
        :param x_predict: pd.DataFrame
        :return: x_train_encode, x_predict_encode
        """
        x_train_encode = x_train.copy()
        x_predict_encode = x_predict.copy()
        fea_need_encode1 = x_train_encode.loc[:, ['Month',
                                                  'Days']]
        fea_need_encode2 = x_predict_encode.loc[:, ['Month',
                                                    'Days']]
        enc = OrdinalEncoder()
        enc.fit(fea_need_encode1)
        x_train_encode.loc[:, ['Month', 'Days']] = \
            enc.transform(fea_need_encode1)
        x_predict_encode.loc[:, ['Month', 'Days']] = \
            enc.transform(fea_need_encode2)
        return x_train_encode, x_predict_encode

    def oneHotEncode(self, x_train, x_predict):
        """
        This Function is to encode the discontinuous variable through
        OneHotEncode method.
        :param x_train: pd.DataFrame
        :param x_predict: pd.DataFrame
        :return: x_train_encode, x_predict_encode
        """
        x_train_encode = x_train.copy()
        x_predict_encode = x_predict.copy()
        fea_need_encode1 = x_train_encode.loc[:, ['Month',
                                                  'Days']]
        fea_need_encode2 = x_predict_encode.loc[:, ['Month',
                                                    'Days']]
        enc = OneHotEncoder(categories='auto')
        enc.fit(fea_need_encode1)
        train = enc.transform(fea_need_encode1).toarray()
        predict = enc.transform(fea_need_encode2).toarray()
        fea_name = enc.get_feature_names().tolist()
        temp1 = pd.DataFrame(train)
        temp2 = pd.DataFrame(predict)
        temp1.columns = fea_name
        temp2.columns = fea_name
        x_train_encode.drop(['Month', 'Days'], axis=1, inplace=True)
        x_train_encoded = pd.concat([x_train_encode, temp1], axis=1)
        x_predict_encode.drop(['Month', 'Days'], axis=1, inplace=True)
        x_predict_encoded = pd.concat([x_predict_encode, temp2], axis=1)
        return x_train_encoded, x_predict_encoded

    def model_validation(self, x_ordinalEncode,
                         x_oneHotEncode, y):
        """
        This function utilize 10 folds cross-validation to evaluate the
        models with different encoded dataset, the mean R-square are set
        as the evaluation standard to judge the goodness of fit for a model.
        :param x_ordinalEncode: pd.DataFrame
        :param x_oneHotEncode: pd.DataFrame
        :param y: pd.DataFrame
        :return: res_tab
        """
        x_or = x_ordinalEncode.copy()
        x_oh = x_oneHotEncode.copy()
        y_val = y.values.ravel()

        # LinearRegression
        # Compare the goodness of fit-
        # -with different feature encode
        reg = LR()
        # 10-folds cross-validation
        lr_res_ordinalEncode = cross_val_score(reg,
                                               x_or,
                                               y_val,
                                               cv=10,
                                               scoring="r2")
        lr_res_or = lr_res_ordinalEncode.mean()

        lr_res_oneHotEncode = cross_val_score(reg,
                                              x_oh,
                                              y_val,
                                              cv=10,
                                              scoring="r2")
        lr_res_oh = lr_res_oneHotEncode.mean()

        # Support vector machine
        # Compare the goodness of fit-
        # -with different feature encode
        reg_SVR = SVR(kernel='linear')
        svm_res_ordinalEncode = cross_val_score(reg_SVR,
                                                x_or,
                                                y_val,
                                                cv=10,
                                                scoring="r2")
        svm_res_or = svm_res_ordinalEncode.mean()

        svm_res_oneHotEncode = cross_val_score(reg_SVR,
                                               x_oh,
                                               y_val,
                                               cv=10,
                                               scoring="r2")
        svm_res_oh = svm_res_oneHotEncode.mean()

        # Random Forest
        # Compare the goodness of fit-
        # -with different feature encode
        # Find best max_depth of model
        def get_best_max_depth(x_encoded, y_val):
            rfr_res = []
            for i in range(10):
                rfr = RandomForestRegressor(max_depth=i + 1,
                                            random_state=20)
                res = cross_val_score(rfr, x_encoded,
                                      y_val,
                                      cv=10, scoring="r2")
                rfr_res.append(res.mean())

            best = 1 + rfr_res.index(max(rfr_res))
            return best

        # Get best max_depth for ordinalEncode
        best_for_or = get_best_max_depth(x_or, y_val)
        rfr1 = RandomForestRegressor(max_depth=best_for_or,
                                     random_state=20)
        rfr_res_orEncode = cross_val_score(rfr1,
                                           x_or,
                                           y_val,
                                           cv=10,
                                           scoring="r2")
        rfr_res_or = rfr_res_orEncode.mean()
        # Get best max_depth for oneHotEncode
        best_for_oh = get_best_max_depth(x_oh, y_val)
        rfr2 = RandomForestRegressor(max_depth=best_for_oh,
                                     random_state=20)
        rfr_res_ohEncode = cross_val_score(rfr2,
                                           x_oh,
                                           y_val,
                                           cv=10,
                                           scoring="r2")

        rfr_res_oh = rfr_res_ohEncode.mean()

        res_summary = {'LR_or': {'R-square': abs(lr_res_or)},
                       'LR_oh': {'R-square': abs(lr_res_oh)},
                       'SVM_or': {'R-square': abs(svm_res_or)},
                       'SVM_oh': {'R-square': abs(svm_res_oh)},
                       'RFR_or': {'R-square': abs(rfr_res_or)},
                       'RFR_oh': {'R-square': abs(rfr_res_oh)}}
        res_tab = pd.DataFrame(res_summary)

        res_tab.columns = [['LinearRegression',
                            'LinearRegression',
                            'Support vector machine',
                            'Support vector machine',
                            'Random Forest',
                            'Random Forest'],
                           ['Ordinal', 'OneHot',
                            'Ordinal', 'OneHot',
                            'Ordinal', 'OneHot']]
        # output latex table
        latex = res_tab.copy()
        latex.index.set_names('$Model$', inplace=True)
        latex_reset = latex.reset_index()
        latex_final = latex_reset.to_latex(column_format='lcccccc',
                                           multicolumn=True,
                                           multicolumn_format='c',
                                           escape=False,
                                           caption='Results for '
                                                   'Cross-validation',
                                           label='Table 3',
                                           index=False)
        print(latex_final)
        return res_tab

    def train_LinearRegression(self, x, y):
        """
        This function is to train LinearRegression model.
        :param x: pd.DataFrame
        :param y: pd.DataFrame
        :return: reg
        """
        x_train = x.copy()
        y_train = y.values.ravel()
        reg = LR()
        reg.fit(x_train, y_train)

        return reg

    def train_SVM(self, x, y):
        """
        This function is to train SVM model.
        :param x: pd.DataFrame
        :param y: pd.DataFrame
        :return: svm
        """
        x_train = x.copy()
        y_train = y.values.ravel()
        svm = SVR(kernel='linear')
        svm.fit(x_train, y_train)

        return svm

    def train_RandomForest(self, x, y):
        """
        This function is to train RandomForest model.
        :param x: pd.DataFrame
        :param y: pd.DataFrame
        :return: rfr
        """
        x_train = x.copy()
        y_train = y.values.ravel()

        def get_best_max_depth(x_train, y_train):
            rfr_res = []
            for i in range(10):
                rfr = RandomForestRegressor(max_depth=i + 1,
                                            random_state=20)
                res = cross_val_score(rfr, x_train,
                                      y_train,
                                      cv=10, scoring="r2")
                rfr_res.append(res.mean())
            best = 1 + rfr_res.index(max(rfr_res))
            return best

        depth = get_best_max_depth(x_train, y_train)
        rfr = RandomForestRegressor(max_depth=depth,
                                    random_state=20)
        rfr.fit(x_train, y_train)

        return rfr

    def model_prediction(self, trained_model, model_name, x_future):
        """
        This function is for prediction
        :param trained_model: object
        :param model_name: string
        :param x_future: pd.DataFrame
        :return: result
        """
        x_pred = x_future.copy()
        y_predict = trained_model.predict(x_pred).astype(int)
        # predict accident number for the future 10 days
        tab = {model_name: {'16-6-2020': 0,
                            '17-6-2020': 0,
                            '18-6-2020': 0,
                            '19-6-2020': 0,
                            '20-6-2020': 0,
                            '21-6-2020': 0,
                            '22-6-2020': 0,
                            '23-6-2020': 0,
                            '24-6-2020': 0,
                            '25-6-2020': 0}}
        result = pd.DataFrame(tab)
        result[model_name] = y_predict

        return result

    def result_plot(self, res_lr, res_svm, res_rfr):
        """
        This function is to plot a line chart for the result.
        :param res_lr: pd.DataFrame
        :param res_svm: pd.DataFrame
        :param res_rfr: pd.DataFrame
        :return: none
        """
        plt.style.use('seaborn-whitegrid')
        xlabels = res_lr.index.tolist()
        day_num = 10
        line_lr = []
        line_svm = []
        line_rfr = []

        fig, ax = plt.subplots(figsize=(8, 6))
        for i in range(day_num):
            line_lr.append(res_lr.iloc[i, 0])

        for i in range(day_num):
            line_svm.append(res_svm.iloc[i, 0])

        for i in range(day_num):
            line_rfr.append(res_rfr.iloc[i, 0])

        ax.plot(xlabels, line_lr,
                linewidth=3,
                marker='o',
                markersize=9,
                label='LinearRegression')
        ax.plot(xlabels, line_svm,
                linewidth=3,
                marker='s',
                markersize=9,
                label='Support vector machine')
        ax.plot(xlabels, line_rfr,
                linewidth=3,
                marker='d',
                markersize=9,
                label='Random Forest')
        ax.set_ylabel('Predicted Accident Number',
                      fontsize=15,
                      fontweight='roman',
                      fontstyle='italic')
        ax.set_xlabel('Date',
                      fontsize=15,
                      fontweight='roman',
                      fontstyle='italic')
        ax.set_title('Number of accdients Prediction',
                     fontsize=18,
                     fontweight='roman',
                     fontstyle='italic')
        x = np.arange(len(xlabels))
        ax.set_xticks(x)
        ax.set_xticklabels(xlabels, fontsize=12)
        for tick in ax.get_xticklabels():
            tick.set_rotation(335)
        ax.legend(fontsize=14,
                  loc='upper left',
                  bbox_to_anchor=(1.02, 0.3), borderaxespad=0.)
        plt.show()

    def final_result(self, res_tab):
        """
        The function is to output the final result table.
        :param res_tab: pd.DataFrame
        :return: res
        """
        res = res_tab.copy()
        res['Mean'] = res.mean(axis=1)
        res = res.astype(int)

        latex = res.copy()
        latex.index.set_names('$Date$', inplace=True)
        latex_reset = latex.reset_index()
        latex_final = latex_reset.to_latex(column_format='lccc',
                                           escape=False,
                                           caption='Predicted Accident Number',
                                           label='Table 4',
                                           index=False)
        print(latex_final)
        return res
