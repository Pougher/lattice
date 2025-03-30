def colour_interpolate(c, t, v):
    interp = [
        int(c[0] - (c[0] - t[0]) * v),
        int(c[1] - (c[1] - t[1]) * v),
        int(c[2] - (c[2] - t[2]) * v),
    ]
    return interp
