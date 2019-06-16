"""
Color

Color class that can be used interchangably as RGB or HSV with
seamless translation.  Use whichever is more convenient at the
time - RGB for familiarity, HSV to fade colors easily

RGB values range from 0 to 255
HSV values range from 0.0 to 1.0

    >>> red   = RGB(255, 0 ,0)
    >>> green = HSV(0.33, 1.0, 1.0)

Colors may also be specified as hexadecimal string:

    >>> blue  = Hex('#0000ff')

Both RGB and HSV components are available as attributes
and may be set.

    >>> red.r
    255

    >>> red.g = 128
    >>> red.rgb
    (255, 128, 0)

    >>> red.hsv
    (0.08366013071895424, 1.0, 1.0)

These objects are mutable, so you may want to make a
copy before changing a Color that may be shared

    >>> red = RGB(255,0,0)
    >>> purple = red.copy()
    >>> purple.b = 255
    >>> red.rgb
    (255, 0, 0)
    >>> purple.rgb
    (255, 0, 255)

Brightness can be adjusted by setting the 'v' property, even
when you're working in RGB.

For example: to gradually dim a color
(ranges from 0.0 to 1.0)

    >>> col = RGB(0,255,0)
    >>> while col.v > 0:
    ...   print col.rgb
    ...   col.v -= 0.1
    ... 
    (0, 255, 0)
    (0, 229, 0)
    (0, 204, 0)
    (0, 178, 0)
    (0, 153, 0)
    (0, 127, 0)
    (0, 102, 0)
    (0, 76, 0)
    (0, 51, 0)
    (0, 25, 0)

"""
import colorsys
from copy import deepcopy

__all__=['RGB', 'HSV', 'Hex', 'Color', 'RGBW']

def saturation(rgb):
    low = float(min(rgb.r, rgb.g, rgb.b))
    high = float(max(rgb.r, rgb.g, rgb.b))
    ret = 0
    if low > 0 and high > 0:
        ret = round(100.0*((high-low)/high))
    return ret

def getWhiteColor(rgb):
    ret = 0
    try:
        ret = int(round((255.0-saturation(rgb)) / 255.0 * (float(rgb.r) + float(rgb.b) + float(rgb.g))/3.0))
    except:
        print "Error", rgb
    return ret

def clamp(val, min_value, max_value):
    "Restrict a value between a minimum and a maximum value"
    return max(min(val, max_value), min_value)

def is_hsv_tuple(hsv):
    "check that a tuple contains 3 values between 0.0 and 1.0"
    return len(hsv) == 4 and all([(0.0 <= t <= 1.0) for t in hsv[0:3]])

def is_rgb_tuple(rgb):
    "check that a tuple contains 3 values between 0 and 255"
    return len(rgb) == 4 and all([(0 <= t <= 255) for t in rgb])

def is_rgbw_tuple(rgbw):
    "check for valid RGBW tuple"
    return len(rgbw) == 4 and all([(0 <= t <= 255) for t in rgbw])

def rgb_to_hsv(rgb):
    "convert a rgb[0-255] tuple to hsv[0.0-1.0]"
    f = float(255)
    ret = list(colorsys.rgb_to_hsv(rgb[0]/f, rgb[1]/f, rgb[2]/f))
    ret.append(rgb[-1])
    return tuple(ret)

def rgbw_to_hsv(rgbw):
    "convert a rgbw[0:3][0-255] tuple to hsv[0.0-1.0], plus w"
    f = float(255)
    ret = colorsys.rgb_to_hsv(rgbw[0]/f, rgbw[1]/f, rgbw[2]/f)
    ret.append(rgbw[-1])
    return tuple(ret)

def hsv_to_rgbw(hsv):
    assert is_hsv_tuple(hsv), "malformed hsv tuple:" + str(hsv)
    _rgb = colorsys.hsv_to_rgb(*tuple(hsv[0:3]))
    r = int(_rgb[0] * 0xff)
    g = int(_rgb[1] * 0xff)
    b = int(_rgb[2] * 0xff)
    return (r,g,b,hsv[-1])


def hsv_to_rgb(hsv):
    assert is_hsv_tuple(hsv), "malformed hsv tuple:" + str(hsv)
#    from IPython import embed; embed() 
    _rgb = colorsys.hsv_to_rgb(*tuple(hsv[0:3]))
    r = int(_rgb[0] * 0xff)
    g = int(_rgb[1] * 0xff)
    b = int(_rgb[2] * 0xff)
    return (r,g,b,hsv[-1])

def RGBW(r,g,b,w):
    "Create new RGBW Color"
    t = (r,g,b,w)
    assert is_rgbw_tuple(t)
    return(Color(rgb_to_hsv(t)))

def RGB(r,g,b,w=0):
    "Create a new RGB color"
    t = (r,g,b,w)
    assert is_rgb_tuple(t)
    return Color(rgb_to_hsv(t))

def HSV(h,s,v, w=0.0):
    "Create a new HSV color"
    return Color((h,s,v,w))

def Hex(value):
    "Create a new Color from a hex string"
    value = value.lstrip('#')
    lv = len(value)
    rgb_t = (int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))
    raise Exception('HEX not supported yet in RGBW')
    return RGB(*rgb_t)   #JEM -not sure what to do here

class Color(object):
    def __init__(self, hsv_tuple, recalc=True):
        self._set_hsv(hsv_tuple, recalc )
        

    def copy(self):
        return deepcopy(self)

    def _set_hsv(self, hsv_tuple,recalc=True):
        assert is_hsv_tuple(hsv_tuple)

        self.hsv_t = list(hsv_tuple)
#        if self.recalc_w is True and init is False:                                           
        if recalc is True:
#            from IPython import embed; embed()
            new_w = int(getWhiteColor(self))
            l = list(hsv_tuple)
            l[-1] = new_w
            hsv_tuple = tuple(l)
            self.hsv_t = list(hsv_tuple)


    @property
    def rgbw(self):
        "returns a rgbw[0-255] tuple"
        return hsv_to_rgbw(self.hsv_t)


    @property
    def rgb(self):
        "returns a rgb[0-255] tuple"
        return hsv_to_rgb(self.hsv_t)

    @property
    def hsv(self):
        "returns a hsv[0.0-1.0] tuple"
        return tuple(self.hsv_t)

    @property
    def hex(self):
        "returns a hexadecimal string"
        return '#%02x%02x%02x' % self.rgb

    """
    Properties representing individual HSV compnents
    Adjusting 'H' shifts the color around the color wheel
    Adjusting 'S' adjusts the saturation of the color
    Adjusting 'V' adjusts the brightness/intensity of the color
    """
    @property
    def h(self):
        return self.hsv_t[0]

    @h.setter
    def h(self, val):
        assert 0.0 <= val <= 1.0
        v = clamp(val, 0.0, 1.0)
        self.hsv_t[0] = round(v, 8)

    @property
    def s(self):
        return self.hsv_t[1]

    @s.setter
    def s(self, val):
        assert 0.0 <= val <= 1.0
        v = clamp(val, 0.0, 1.0)
        self.hsv_t[1] = round(v, 8)

    @property
    def v(self):
        return self.hsv_t[2]

    @v.setter
    def v(self, val):
        assert 0.0 <= val <= 1.0
        v = clamp(val, 0.0, 1.0) 
        self.hsv_t[2] = round(v, 8)

    """
    Properties representing individual RGB components
    """
    @property
    def r(self):
        return self.rgb[0]

    @r.setter
    def r(self, val):
        assert 0 <= val <= 255
        r,g,b,w = self.rgb
        new = (val, g, b, w)
        assert is_rgb_tuple(new)
        self._set_hsv(rgb_to_hsv(new))

    @property
    def g(self):
        return self.rgb[1]

    @g.setter
    def g(self, val):
        assert 0 <= val <= 255
        r,g,b,w = self.rgb
        new = (r, val, b, w)
        assert is_rgb_tuple(new)
        self._set_hsv(rgb_to_hsv(new))

    @property
    def b(self):
        return self.rgb[2]

    @b.setter
    def b(self, val):
        assert 0 <= val <= 255
        r,g,b,w = self.rgb
        new = (r, g, val, w)
        assert is_rgb_tuple(new)
        self._set_hsv(rgb_to_hsv(new))

    @property
    def w(self):
        return int(self.rgbw[-1])

    @w.setter
    def w(self,val):
        assert 0 <= val <= 255
        r,g,b, w = self.rgbw
        new = (r, g, b, val)
        self._set_hsv(rgb_to_hsv(new),recalc=False)
        
if __name__=='__main__':
    import doctest
    doctest.testmod()
