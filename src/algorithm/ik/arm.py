import numpy as np
import copy
from gym import spaces

class Arm():
    def __init__(self):
        self.n_part=7
        self.l=[77,125,125,82,20,52,120]
        self.angles=[0,0,0,0,0]
        self.cord=np.array([[0,77.,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]])
        self.th=self.angles[0]*np.pi/180
        self.R=[[np.cos(self.th),0,np.sin(self.th)],[0,1,0],[-1.*np.sin(self.th),0,np.cos(self.th)]]
   

    def set_angles(self,ths):
        if len(ths)==5:
            for i in range(5) :
                self.angles[i]=ths[i]
        self.cord=np.array([[0,77.,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]])
        self.th=self.angles[0]*np.pi/180
        self.R=[[np.cos(self.th),0,np.sin(self.th)],[0,1,0],[-1.*np.sin(self.th),0,np.cos(self.th)]]
        return self.cal_xyz_cord()

    def cal_xy_cord(self):
        for i in range(1,7):
            if i < 5:
                for j in range(i):
                    self.cord[i,0]+=self.l[j+1]*np.cos(np.pi*(np.sum(self.angles[1:(j+2)])/180))
                    self.cord[i,1]+=self.l[j+1]*np.sin(np.pi*(np.sum(self.angles[1:(j+2)])/180))
                    print(np.sum(self.angles[1:(j+2)]))
                    print(self.l[j+1])
            elif i==5:
                self.cord[i,0]=copy.copy(self.cord[4][0])
                self.cord[i,1]=copy.copy(self.cord[4][1])
                self.cord[i,2]=self.l[i]
            elif i==6:
                self.cord[i][0]=copy.copy(self.cord[5][0])
                self.cord[i][1]=copy.copy(self.cord[5][1])
                print("88888888")
                print(self.cord[i][0])
                print(self.cord[i][1])
                self.cord[i][2]=52
                th=self.angles[1:]
                th=np.sum(th)
                print(th)
                th=(th-90)
                print(th)
                th=th*np.pi/180
                self.cord[i,0]+=self.l[i]*np.cos(th)
                self.cord[i,1]+=self.l[i]*np.sin(th)
            print()

        for i in range(1,7):
            self.cord[i,1]+=77

        return 0

    def cal_xyz_cord(self):
        self.cal_xy_cord()
        for i in range(7):
            self.cord[i]=(np.dot(self.R,self.cord[i])).tolist()

        return 0

  