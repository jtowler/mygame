import math


def get_projections(r, theta):
    r_x = r * math.cos(theta)
    r_y = r * math.sin(theta)
    return int(r_x), int(r_y)


def get_angle(x, y, w, h):
    return math.atan2(y - h / 2, x - w / 2)


def project(m_x, m_y, w, h, r):
    theta = get_angle(m_x, m_y, w, h)
    return get_projections(r, theta)
