#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 16:53:21 2015

@author: maciek
"""

import numpy as np
import math
import itertools


def checkEqual(a):
    """
    returns boolean if every element in iterable is equal
    """
    try:
        a = iter(a)
        first = next(a)
        return all(first == rest for rest in a)
    except StopIteration:
        return True

def max_ix(i):
    """
    returns max value in list and index of this value
    """
    ix = i.index(max(i))
    return (i[ix], ix)

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)


def searchN(a, n):
    """
    search for n repeating numbers
    a = iterable
    n = number of repeating elements
    """
    check = []
    carrier = a[n-1:]
    for index, value in enumerate(carrier):
        check = checkEqual(a[index: index+n])
        if check:
            break
    return check


def cart2polar(x, y):
    """
    function acommodates for cartesian coordinates 0,0 centered
    """
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    if theta < 0:
        theta = theta + (math.pi * 2)
    return r, theta


def fstr(l, s):
    """
    returns elements of list l which contain string s
    """
    return [el for el in l if s in el]


def polar2cart(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y


def ans_angle(angle):
    """
    in radians, for 360 deg
    """
    if 45 > angle >= 0 or 360 >= angle >= 315:
        return 'right'
    elif 45 <= angle < 135:
        return 'up'
    elif 135 <= angle < 225:
        return 'left'
    elif 225 <= angle < 315:
        return 'down'


def confmx_4AFC(actual, correct):
    """
    resolves a confusion matrix in 4AFC task
    # < > ^ v
    < # 1 2 2
    > 1 # 2 2
    ^ 2 2 # 1
    v 2 2 1 #
    level 1 confusion (along the axis)
    level 2 confusion (against the axis)
    """
    v = ['up', 'down']
    h = ['left', 'right']
    check = lambda x,y,z: [x in y, x in z]

    if actual == correct:
        return 'correct'
    else:
        if check(actual, h, v) == check(correct, h, v):
            return 'type1'
        else:
            return 'type2'


def cart_dist(a, b):
    """
    a, b - two points as iterables a = [x1,y1], b = [x2,x2]
    """
    return math.sqrt((b[0]-a[0])**2. +(b[1]-a[1])**2.)


def evenno(n):
    return math.ceil(n/2.) * 2

if __name__ == '__main__':
    main()
