from math import e

from matplotlib import pyplot as plt
import SmartReviewRecommendations.EbbinghausForgettingCurve.EbbinghausCurves as Eb



def main():
    a11 = -2.2515171935807575e-06
    b11 = -0.03234073841959593
    a10 = -1.2467053257506555e-05
    b10 = -0.13903372905754122
    a01 = -8.57839280720141e-06
    b01 = -0.0890746714685621
    a00 = -1.2833467689157539e-05
    b00 = -0.3447389387293679
    a1 = -1.4865132163367318e-07
    b1 = -0.06476805277713989
    a0 = -5.033426596650367e-06
    b0 = -0.2784718873971984
    t = range(10,1000000,1)
    t1 = range(10,10000000,1)
    t2 = range(10,100000,1)
    # 字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.grid(True, linestyle="--", color="g", linewidth="0.5")
    plt.tick_params(labelsize=11)
    y11 = [e ** (a11 * i + b11) for i in t]
    y10 = [e ** (a10 * i + b10) for i in t2]
    y01 = [e ** (a01 * i + b01) for i in t2]
    y00 = [e ** (a00 * i + b00) for i in t2]
    y1 = [e ** (a1 * i + b1) for i in t1]
    y0 = [e ** (a0 * i + b0) for i in t]

    plt.scatter(Eb.result_T[:,0], Eb.result_T[:,1], s=30, marker='o')
    plt.title("第一次做对", fontsize=13)
    plt.xlabel('t（min）', fontsize=12)
    plt.ylabel('memory_rate（%）', fontsize=12)
    plt.plot(t1, y1, label='1')
    plt.show()

    plt.grid(True, linestyle="--", color="g", linewidth="0.5")
    plt.scatter(Eb.result_F[:, 0], Eb.result_F[:, 1], s=30, marker='o')
    plt.title("第一次做错", fontsize=13)
    plt.xlabel('t（min）', fontsize=12)
    plt.ylabel('memory_rate（%）', fontsize=12)
    plt.plot(t, y0, label='0')
    plt.show()

    plt.grid(True, linestyle="--", color="g", linewidth="0.5")
    plt.scatter(Eb.result_T_T[:, 0], Eb.result_T_T[:, 1], s=30, marker='o')
    plt.title("第一次做对，第二次做对", fontsize=13)
    plt.xlabel('t（min）', fontsize=12)
    plt.ylabel('memory_rate（%）', fontsize=12)
    plt.plot(t, y11, label='11')
    plt.show()

    plt.grid(True, linestyle="--", color="g", linewidth="0.5")
    plt.scatter(Eb.result_T_F[:, 0], Eb.result_T_F[:, 1], s=30, marker='o')
    plt.title("第一次做对，第二次做错", fontsize=13)
    plt.xlabel('t（min）', fontsize=12)
    plt.ylabel('memory_rate（%）', fontsize=12)
    plt.plot(t2, y10, label='10')
    plt.show()

    plt.grid(True, linestyle="--", color="g", linewidth="0.5")
    plt.scatter(Eb.result_F_T[:, 0], Eb.result_F_T[:, 1], s=30, marker='o')
    plt.title("第一次做错，第二次做对", fontsize=13)
    plt.xlabel('t（min）', fontsize=12)
    plt.ylabel('memory_rate（%）', fontsize=12)
    plt.plot(t2, y01, label='01')
    plt.show()

    plt.grid(True, linestyle="--", color="g", linewidth="0.5")
    plt.scatter(Eb.result_F_F[:, 0], Eb.result_F_F[:, 1], s=30, marker='o')
    plt.title("第一次做错，第二次做错", fontsize=13)
    plt.xlabel('t（min）', fontsize=12)
    plt.ylabel('memory_rate（%）', fontsize=12)
    plt.plot(t2, y00, label='10')
    plt.show()


if __name__ == '__main__':
    main()
