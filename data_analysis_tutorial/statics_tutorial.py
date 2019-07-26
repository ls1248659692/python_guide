#!/usr/bin/python
# coding=utf8

from scipy import stats
from scipy.stats import binom, poisson

from  report_util.data_analysis_head import *


## 统计学相关基础数据
def calc_deviation():
    d = {'Name': pd.Series(['Tom', 'James', 'Ricky', 'Vin', 'Steve', 'Smith', 'Jack',
                            'Lee', 'Chanchal', 'Gasper', 'Naviya', 'Andres']),
         'Age': pd.Series([25, 26, 25, 23, 30, 25, 23, 34, 40, 30, 25, 46]),
         'Rating': pd.Series([4.23, 3.24, 3.98, 2.56, 3.20, 4.6, 3.8, 3.78, 2.98, 4.80, 4.10, 3.65])}

    # Create a DataFrame
    df = pd.DataFrame(d)
    print df.describe()

    print df.mean()
    print df.median()
    print df.mode()

    # Calculate the standard deviation
    print df.std()

    # Measuring Skewness
    print df.skew()


## 正态分布
def draw_normal_distribution():
    ## sigma = 1  stand normal distribution
    miu, sigma = 0.5, 1
    s = np.random.normal(miu, sigma, 1000)

    # Create the bins and histogram
    count, bins, ignored = plt.hist(s, 20, density=True)

    # Plot the distribution curve
    plt.plot(bins, 1 / (sigma * np.sqrt(2 * np.pi)) *
             np.exp(- (bins - miu) ** 2 / (2 * sigma ** 2)), linewidth=3, color='y')
    plt.show()


## 二项式分布
def draw_binomial_distribution():
    binom.rvs(size=10, n=20, p=0.8)

    data_binom = binom.rvs(n=20, p=0.8, loc=0, size=1000)
    ax = sns.distplot(
        data_binom,
        kde=True,
        color='blue',
        hist_kws=
        {
            "linewidth": 25,
            'alpha': 1
        }
    )

    ax.set(xlabel='Binomial', ylabel='Frequency')
    plt.show()


## 泊松分布
def draw_poisson_distribution():
    data_binom = poisson.rvs(mu=4, size=10000)
    ax = sns.distplot(
        data_binom,
        kde=True,
        color='green',
        hist_kws=
        {
            "linewidth": 25,
            'alpha': 1
        }
    )

    ax.set(xlabel='Poisson', ylabel='Frequency')
    plt.show()


## 相关性分析
def draw_correlation():
    df = sns.load_dataset('iris')

    # without regression
    sns.pairplot(df, kind="scatter")
    plt.show()


## 卡方分布
def draw_chi_square():
    x = np.linspace(0, 10, 100)
    fig, ax = plt.subplots(1, 1)

    linestyles = [':', '--', '-.', '-']
    deg_of_freedom = [1, 4, 7, 6]
    for df, ls in zip(deg_of_freedom, linestyles):
        ax.plot(x, stats.chi2.pdf(x, df), linestyle=ls)

    plt.xlim(0, 10)
    plt.ylim(0, 0.4)

    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Chi-Square Distribution')

    plt.legend()
    plt.show()


## 线性回归
def draw_linear_regression():
    df = sns.load_dataset('tips')
    sns.regplot(x="total_bill", y="tip", data=df)
    plt.show()


if __name__ == "__main__":
    # calc_deviation()
    # draw_normal_distribution()
    # draw_binomial_distribution()
    # draw_poisson_distribution()
    # draw_correlation()
    # draw_chi_square()
    draw_linear_regression()
