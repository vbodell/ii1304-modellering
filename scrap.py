import sys

initialSick = 2
upperBound = 3

initSickPos = []
for ndx in range(initialSick):
    xy = input("Enter positions for sick person #%d (separated by comma): " % (ndx+1))
    (x,y) = xy.split(',')
    x = int(x)
    y = int(y)
    if x < 0 or x >= upperBound or y < 0 or y >= upperBound or (x,y) in initSickPos:
        print("Invalid index, must be in interval [0,%d) and cannot be same as a previous position. Terminating" % upperBound)
        sys.exit(1)
    initSickPos.append((x,y))
return initSickPos
