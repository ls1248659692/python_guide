#!/usr/bin/python
# coding=utf8

import os
import pickle

import graphviz

from numpy.random import shuffle
from scipy import integrate
from scipy.optimize import fsolve
from scipy.interpolate import lagrange
from sklearn import svm
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression as LR
from sklearn.linear_model import RandomizedLogisticRegression as RLR
from sklearn.tree import export_graphviz
from sklearn.tree import DecisionTreeClassifier as DTC
from sklearn.metrics import roc_curve
from sklearn.metrics import confusion_matrix
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import adfuller as ADF
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.arima_model import ARIMA

from  report_util.data_analysis_head import *

__author__ = 'Jam'
__date__ = '2018/11/27 15:39'

SRC_PATH = os.getcwd()


def ployinterp_column(index, df, k=5):
    y = df[list(range(index - k, index))
           + list(range(index + 1, index + 1 + k))]
    y = y[y.notnull()]
    return lagrange(y.index, list(y))(index)


# 拉格朗日插值代码
def ployinterp_fillnum():
    inputfile = SRC_PATH + '/data/catering_sale.xls'
    outputfile = SRC_PATH + '/tmp/sales.xls'

    data = pd.read_excel(inputfile)

    print data[(data[u'销量'] < 400) | (data[u'销量'] > 5000)]
    data.loc[(data[u'销量'] < 400) | (data[u'销量'] > 5000), u'销量'] = None

    df = data[data[u'销量'].isnull()]
    print df

    for index in df[u'销量'].index:
        data.at[index, u'销量'] = ployinterp_column(index, data[u'销量'])

    data.to_excel(outputfile)


def get_abnormal_data():
    datafile = SRC_PATH + '/data/normalization_data.xls'
    data = pd.read_excel(datafile, header=None)

    print((data - data.min()) / (data.max() - data.min()))  # 最小-最大规范化
    print((data - data.mean()) / data.std())  # 零-均值规范化
    print(data / 10 ** np.ceil(np.log10(data.abs().max())))  # 小数定标规范化


def cluster_plot(data, d, k):
    plt.figure(figsize=(8, 3))
    for j in range(0, k):
        plt.plot(data[d == j], [j for _ in d[d == j]], 'o')
    plt.ylim(-0.5, k - 0.5)
    return plt


# 求解非线性方程组2x1-x2^2=1,x1^2-x2=2
def nonlinear_equation(x):  # 定义要求解的方程组
    return [2 * x[0] - x[1] ** 2 - 1, x[0] ** 2 - x[1] - 2]


def solve_equations():
    result = fsolve(nonlinear_equation, [1, 1])  # 输入初值[1, 1]并求解
    print(result)  # 输出结果，为array([ 1.91963957,  1.68501606])


# 定义被积函数
def integral_function(x):
    return (1 - x ** 2) ** 0.5


def intergrate_solve():
    pi_2, err = integrate.quad(integral_function, -1, 1)  # 积分结果和误差
    print pi_2 * 2, err


# 逻辑回归 自动建模(相关模型无法运行)
def logistic_regression():
    # 参数初始化
    filename = SRC_PATH + '/data/bankloan.xls'
    data = pd.read_excel(filename)
    print data.head()
    print data.tail()

    x = data.iloc[:, :8].as_matrix()
    y = data.iloc[:, 8].as_matrix()

    print x, y

    rlr = RLR()  # 建立随机逻辑回归模型，筛选变量
    rlr.fit(x, y)  # 训练模型
    rlr.get_support()  # 获取特征筛选结果，也可以通过.scores_方法获取各个特征的分数
    print(u'通过随机逻辑回归模型筛选特征结束。')

    # print(u'有效特征为：%s' % ','.join(data.columns[rlr.get_support()]))
    # x = data[data.columns[rlr.get_support()]].as_matrix()  # 筛选好特征

    lr = LR()  # 建立逻辑货柜模型
    lr.fit(x, y)  # 用筛选后的特征数据来训练模型
    print(u'逻辑回归模型训练结束。')
    print(u'模型的平均正确率为：%s' % lr.score(x, y))  # 给出模型的平均正确率，本例为81.4%


# 使用决策树算法预测销量高低，促销
def decision_tree():
    # 参数初始化
    inputfile = SRC_PATH + '/data/sales_data.xls'
    data = pd.read_excel(inputfile, index_col=u'序号', sheet_name='sales_data')  # 导入数据

    # 数据是类别标签，要将它转换为数据
    # 用1来表示“好”、“是”、“高”这三个属性，用-1来表示“坏”、“否”、“低”
    data[data.isin([u'好', u'是', u'高'])] = 1
    data[data != 1] = -1

    x = data.iloc[:, :3].as_matrix().astype(int)
    y = data.iloc[:, 3].as_matrix().astype(int)

    dtc = DTC(criterion='entropy')  # 建立决策树模型，基于信息熵
    dtc.fit(x, y)  # 训练模型

    # 导入相关函数，可视化决策树。
    # 导出的结果是一个dot文件，需要安装Graphviz才能将它转换为pdf或png等格式。
    x = pd.DataFrame(x, columns=['weather', 'weekend', 'promotion'])  ## 中文在pdf 中无法显示
    print x

    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/graphviz-2.38/release/bin/'
    dot_data = export_graphviz(dtc, feature_names=x.columns, out_file=None)
    graph = graphviz.Source(dot_data)
    graph.render(SRC_PATH + "/tmp/tree")


# k_means 作图函数
def density_plot(data, k):
    kde = data.plot(kind='kde', linewidth=2, subplots=True, sharex=False)
    [kde[i].set_ylabel(u'密度') for i in range(k)]
    plt.xlabel('values')
    plt.legend()
    return plt


def kmeans_regression():
    # 参数初始化
    inputfile = SRC_PATH + '/data/consumption_data.xls'  # 销量及其他属性数据
    outputfile = SRC_PATH + '/tmp/data_type.xls'  # 保存结果的文件名
    k = 3  # 聚类的类别

    iteration = 500  # 聚类最大循环次数
    data = pd.read_excel(inputfile, index_col='Id')  # 读取数据
    data_standard = 1.0 * (data - data.mean()) / data.std()  # 数据标准化

    print data_standard

    model = KMeans(n_clusters=k, n_jobs=1, max_iter=iteration)  # 分为k类，并发数4
    model.fit(data_standard)  # 开始聚类

    # 简单打印结果
    r1 = pd.Series(model.labels_).value_counts()  # 统计各个类别的数目
    r2 = pd.DataFrame(model.cluster_centers_)  # 找出聚类中心

    print r1
    print r2

    r = pd.concat([r2, r1], axis=1)  # 横向连接（0是纵向），得到聚类中心对应的类别下的数目
    r.columns = list(data.columns) + [u'类别数目']  # 重命名表头
    print(r)

    # 详细输出原始数据及其类别
    r = pd.concat([data, pd.Series(model.labels_, index=data.index)], axis=1)  # 详细输出每个样本对应的类别
    r.columns = list(data.columns) + [u'聚类类别']  # 重命名表头
    r.to_excel(outputfile)  # 保存结果

    pic_output = SRC_PATH + '/tmp/pd_figure_'  # 概率密度图文件名前缀
    for i in range(k):
        density_plot(data[r[u'聚类类别'] == i], k).savefig(u'%s%s.png' % (pic_output, i))


def arima_regression():
    # 参数初始化
    discfile = SRC_PATH + '/data/arima_data.xls'
    forecastnum = 5

    # 读取数据，指定日期列为指标，Pandas自动将“日期”列识别为Datetime格式
    data = pd.read_excel(discfile, index_col=u'日期')

    # 时序图
    data.plot()
    plt.show()

    # 自相关图
    plot_acf(data).show()
    print u'原始序列的ADF检验结果为：', ADF(data[u'销量'])

    # 差分后的结果
    D_data = data.diff().dropna()
    D_data.columns = [u'销量差分']
    D_data.plot()  # 时序图
    plt.show()

    print data
    print D_data

    plot_acf(D_data).show()  # 自相关图
    plot_pacf(D_data).show()  # 偏自相关图
    print u'差分序列的ADF检验结果为：', ADF(D_data[u'销量差分'])  # 平稳性检测

    # 白噪声检验
    print(u'差分序列的白噪声检验结果为：', acorr_ljungbox(D_data, lags=1))  # 返回统计量和p值

    data[u'销量'] = data[u'销量'].astype(float)
    # 定阶
    pmax = int(len(D_data) / 10)  # 一般阶数不超过length/10
    qmax = int(len(D_data) / 10)  # 一般阶数不超过length/10
    bic_matrix = []  # bic矩阵
    for p in range(pmax + 1):
        tmp = []
        for q in range(qmax + 1):
            try:  # 存在部分报错，所以用try来跳过报错。
                tmp.append(ARIMA(data, (p, 1, q)).fit().bic)
            except:
                tmp.append(None)
        bic_matrix.append(tmp)

    bic_matrix = pd.DataFrame(bic_matrix)  # 从中可以找出最小值

    p, q = bic_matrix.stack().idxmin()  # 先用stack展平，然后用idxmin找出最小值位置。
    print(u'BIC最小的p值和q值为：%s、%s' % (p, q))
    model = ARIMA(data, (p, 1, q)).fit()  # 建立ARIMA(0, 1, 1)模型
    model.summary2()  # 给出一份模型报告
    model.forecast(5)  # 作为期5天的预测，返回预测结果、标准误差、置信区间。


def plot_cm(y, yp):
    cm = confusion_matrix(y, yp)  # 混淆矩阵

    plt.matshow(cm, cmap=plt.cm.Greens)  # 画混淆矩阵图，配色风格使用cm.Greens，更多风格请参考官网。
    plt.colorbar()  # 颜色标签

    for x in range(len(cm)):  # 数据标签
        for y in range(len(cm)):
            plt.annotate(cm[x, y], xy=(
                x, y), horizontalalignment='center', verticalalignment='center')

    plt.ylabel('True label')  # 坐标轴标签
    plt.xlabel('Predicted label')  # 坐标轴标签
    return plt


def plot_roc(test, predict_result, label_name):
    fpr, tpr, thresholds = roc_curve(
        test[:, 3], predict_result, pos_label=1)
    plt.plot(fpr, tpr, linewidth=2, label='ROC of CART', color='green')  # 作出ROC曲线
    plt.xlabel('False Positive Rate')  # 坐标轴标签
    plt.ylabel('True Positive Rate')  # 坐标轴标签
    plt.ylim(0, 1.05)  # 边界范围
    plt.xlim(0, 1.05)  # 边界范围
    plt.legend(loc=4)  # 图例
    plt.show()  # 显示作图结果
    return plt


def svm_regression():
    inputfile = SRC_PATH + '/data/moment.csv'  # 数据文件
    outputfile1 = SRC_PATH + '/tmp/cm_train.xls'  # 训练样本混淆矩阵保存路径
    outputfile2 = SRC_PATH + '/tmp/cm_test.xls'  # 测试样本混淆矩阵保存路径

    data = pd.read_csv(inputfile, encoding='gbk')  # 读取数据，指定编码为gbk
    data = data.as_matrix()

    shuffle(data)  # 随机打乱数据

    data_train = data[:int(0.8 * len(data)), :]  # 选取前80%为训练数据
    data_test = data[int(0.8 * len(data)):, :]  # 选取前20%为测试数据

    # 构造特征和标签
    x_train = data_train[:, 2:] * 30
    y_train = data_train[:, 0].astype(int)

    print  x_train
    print  y_train

    x_test = data_test[:, 2:] * 30
    y_test = data_test[:, 0].astype(int)

    # 导入模型相关的函数，建立并且训练模型
    model = svm.SVC()
    model.fit(x_train, y_train)
    pickle.dump(model, open(SRC_PATH + '/tmp/svm.model', 'wb'))
    # 最后一句保存模型，以后可以通过下面语句重新加载模型：
    # model = pickle.load(open('../tmp/svm.model', 'rb'))

    # 导入输出相关的库，生成混淆矩阵
    cm_train = metrics.confusion_matrix(y_train, model.predict(x_train))  # 训练样本的混淆矩阵
    cm_test = metrics.confusion_matrix(y_test, model.predict(x_test))  # 测试样本的混淆矩阵

    # 保存结果
    pd.DataFrame(cm_train, index=range(1, 6), columns=range(1, 6)).to_excel(outputfile1)
    pd.DataFrame(cm_test, index=range(1, 6), columns=range(1, 6)).to_excel(outputfile2)


if __name__ == "__main__":
    # ployinterp_fillnum()
    # get_abnormal_data()
    # solve_equations()
    # intergrate_solve()
    # logistic_regression()
    # decision_tree()
    # kmeans_regression()
    # arima_regression()
    svm_regression()
    pass
