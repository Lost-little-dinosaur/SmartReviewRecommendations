from math import e

from matplotlib import pyplot as plt


def main():
    a11 = -2.2515171935807575e-06
    b11 = -0.03234073841959593
    a10 = -1.2467053258896204e-05
    b10 = -0.13903372905214134
    a01 = -8.57839280720141e-06
    b01 = -0.0890746714685621
    a00 = -1.2833467689157539e-05
    b00 = -0.3447389387293679
    a1 = -1.4865132163367318e-07
    b1 = -0.06476805277713989
    a0 = -5.033426596650367e-06
    b0 = -0.2784718873971984
    x = [i for i in range(0, 100000000, 100000)]
    y11 = [e ** (a11 * i + b11) for i in x]
    y10 = [e ** (a10 * i + b10) for i in x]
    y01 = [e ** (a01 * i + b01) for i in x]
    y00 = [e ** (a00 * i + b00) for i in x]
    y1 = [e ** (a1 * i + b1) for i in x]
    y0 = [e ** (a0 * i + b0) for i in x]
    plt.plot(x, y11, label='11')
    plt.plot(x, y10, label='10')
    plt.plot(x, y01, label='01')
    plt.plot(x, y00, label='00')
    plt.plot(x, y1, label='1')
    plt.plot(x, y0, label='0')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
