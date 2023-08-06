import numpy as np
import cython
try:
    import _bessel
    from _bessel import yv_range_dispatcher as _yv_range_dispatcher

    def yv_range(v_from, n, xs, out=None):
        xs = np.asarray(xs)
        return _yv_range_dispatcher(v_from, n, xs)
except ImportError:
    import scipy.special as sp

    def yv_range(v_from, n, xs, out=None):
        order_yvs = [sp.yv(v_from + i, xs) for i in range(n)]
        return np.stack(order_yvs, axis=-1, out=out)

def main():
    arr = np.empty(50, dtype=np.int)
    print(_bessel.yv_range(-5.3, 11, 3))
    print(_bessel.yv_range_dispatcher(-5.3, 3, arr))
    print(yv_range(-5.3, 3., arr))
    # print(_bessel.yv_range_float_impl(-5.3, 3., arr))
    print(arr)
    # print(_bessel.yv_range_impl(-25.3, 3., arr))
    print('-')


if __name__ == '__main__':
    main()
