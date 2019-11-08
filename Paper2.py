import cv2
import numpy as np

T = cv2.imread("P1 Resources/c4t.bmp")
D = cv2.imread("P1 Resources/c4d.bmp")
td = 60000
tt = 30000
p1,p2 = [],[]
s = 20

# Standard deviation function
def SSD(refPatch, iPatch):
        #print(refPatch)
        #print(iPatch)
        temp = np.sum(np.subtract(refPatch,iPatch)**2)
        #ret = temp*temp
        return temp

# on mouse function to pass as a cv2.setMouseCallback() parameter.
def mouse(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDBLCLK:    # if left mouse button is double clicked
                # clears previous coordinates and appends current mouse coordinate.
                p1.clear()
                p1.append(x)
                p2.clear()
                p2.append(y)
                # grabs patch around mouse click and displays patch.
                im2 = patch(p1[0],p2[0],T,s)
                cv2.imshow('test',im2)
                print(dtObj(x,y,tt,td,T,D,20)) # check cv2 tresholds.
                return True

# function that returns a patch around a single coordinate.

'''
def patch(y,x,img, size):
        # gets the maximum possible xy coordinate.
        maxY,maxX = img.shape[0], img.shape[1]

        # if statements to handle coordinates that go out of bounds.
        if x-(size/2) < 0:
                newX = 0
        elif x+(size/2) > maxX-1:
                newX = maxX-(size+1)
        else:
                newX = x-(size/2)

        if y-(size/2) < 0:
                newY = 0
        elif y+(size/2) > maxY-1:
                newY = maxY-(size+1)
        else:
                newY = y+(size/2)
        
        # changes values from float to int
        newX = int(newX)
        newY = int(newY)

        # grabing patch using numpy array
        patch = img[newX:newX+size, newY-size:newY, :]
        return patch
'''

def patch(y,x,img,size):
        temp = int(size/2)
        return img[x-temp:x+temp, y-temp:y+temp]

# resource: "Efficient Object Selection using Depth and Texture Information", Dylan Seychell, Carl James Debono 
def dtObj(xs,ys,treshD,treshT,T,D,Patch):
        x,y,i = 20,20,0
        Ld,Lt = [],[]
        #ssdD,ssdT = [],[]
        dPatch = patch(xs,ys,D,Patch)
        tPatch = patch(xs,ys,T,Patch)
        while(x<(T.shape[1]-Patch) and y<(T.shape[0]-Patch)):
                idPatch = patch(x,y,D,Patch)
                #print(idPatch)
                itPatch = patch(x,y,T,Patch)
                #print(itPatch)
                ssdD = SSD(dPatch,idPatch)
                ssdT = SSD(tPatch,itPatch)
                print(ssdD)

                if ssdD < treshD:
                        Ld.append([x,y])
                if ssdT < treshT:
                        Lt.append([x,y])

                x = x + Patch
                y = y + Patch
        return Ld, Lt


cv2.imshow('Texture',T)
#cv2.imshow('Depth',D)
cv2.setMouseCallback('Texture', mouse)
cv2.waitKey(0)
cv2.destroyAllWindows