
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

if __name__ == '__main__':
    data = np.loadtxt("F:\学习资料\数学建模\\assignment\附件1：区域高程数据.xlsx", dtype=float)
    x, y, z = data[:, 0], data[:, 1], data[:, 2]

    # 准备待插值位置
    xi = np.linspace(x.min(), x.max(), 200)
    yi = np.linspace(y.min(), y.max(), 200)
    X, Y = np.meshgrid(xi, yi)

    # 插值
    Z = griddata((x, y), z, (X, Y), method='cubic')

    # 绘图
    fig = plt.figure()
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot_surface(X, Y, Z, cmap='jet')
    ax1.contour(X, Y, Z, cmap='jet')

    ax2 = fig.add_subplot(122)
    ax2.contourf(X, Y, Z, cmap='jet')

    plt.tight_layout()
    plt.show()