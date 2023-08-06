class math:
    def slope(x1, y1, x2, y2):
        mksure = int(x1)
        mksure1 = int(x2)
        x3 = mksure1 - mksure
        mksure2 = int(y1)
        mksure3 = int(y2)
        y3 = mksure3 - mksure2
        xy1 = y3 / x3
        return xy1
    def addone(num1):
      num2 = num1 + 1
      return num2
    def subone(num1):
     num2 = num1 - 1
     return num2
    def midpointxcoord(x1, x2):
        x12 = x1 + x2
        x123 = x12 / 2
        return x123
    def midpointycoord(y1, y2):
     y12 = y1 + y2
     y123 = y12 / 2
     return y123