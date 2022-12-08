from math import exp

import matplotlib.pyplot as plt
from mpmath import ln


def main():
    t = [i + 1 for i in range(146 // 2)]
    # y=k.*t.^(-c);
    k = 31.8
    c = 0.125
    y0 = [k * ((i / 1460) ** (-c)) for i in t]
    y1 = [(k - 3) * ((i / 1460) ** (-c)) for i in t]
    y2 = [k * ((i / 1460) ** (-c + 0.05)) for i in t]

    plt.plot(t, y0)
    plt.plot(t, y1)
    plt.plot(t, y2)
    plt.legend(['y0', 'y1', 'y2'])
    plt.show()


if __name__ == '__main__':
    main()
