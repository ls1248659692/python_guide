#!/usr/bin/python
# coding=utf8

from  report_util.data_analysis_head import *


def start_plot():
    x = np.arange(0, 10)
    y = map(lambda x: x ** 2, x)
    z = map(lambda x: x ** 2.5, x)

    print x
    print y
    print z

    # Labeling the Axes and Title
    plt.title("Graph Drawing")
    plt.xlabel("Time")
    plt.ylabel("Distance")

    # Simple Plot
    plt.plot(x, y)
    plt.plot(x, z)
    plt.plot(x, y, 'r')
    plt.plot(x, y, '>')

    # Annotate
    plt.annotate(xy=[x[1] - 0.5, y[1] - 5], s='Second Entry')
    plt.annotate(xy=[x[2] - 0.5, y[2] - 5], s='Third Entry')

    # Adding Legends
    # plt.legend(['Race1'], loc=4)

    ## 以下选择一个运行，否者无法生成图片
    plt.show()
    # plt.savefig('test.png')


def draw_box():
    df = pd.DataFrame(np.random.rand(10, 5), columns=['A', 'B', 'C', 'D', 'E'])
    df.plot.box()
    plt.show()


def draw_heatmap():
    data = [{2, 3, 4, 1}, {6, 3, 5, 2}, {6, 3, 5, 4}, {3, 7, 5, 4}, {2, 8, 1, 5}]
    Index = ['I1', 'I2', 'I3', 'I4', 'I5']
    Cols = ['C1', 'C2', 'C3', 'C4']
    df = pd.DataFrame(data, index=Index, columns=Cols)

    plt.pcolor(df)
    plt.show()


def draw_scatter():
    df = pd.DataFrame(np.random.rand(50, 4), columns=['a', 'b', 'c', 'd'])
    df.plot.scatter(x='a', y='b')
    plt.show()


def draw_bubble():
    # create data
    x = np.random.rand(40)
    y = np.random.rand(40)
    z = np.random.rand(40)
    colors = np.random.rand(40)

    # use the scatter function
    plt.scatter(x, y, s=z * 1000, c=colors)
    plt.show()


if __name__ == "__main__":
    # start_plot()
    # draw_box()
    # draw_heatmap()
    # draw_scatter()
    draw_bubble()
