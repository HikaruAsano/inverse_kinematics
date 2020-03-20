from ik.arm import Arm
import numpy as np
from matplotlib import pyplot as plt
from ik.core import Actuator
from mpl_toolkits.mplot3d import Axes3D 

# def onclick(event):
#     x=list()
#     x.append(event.xdata)
#     x.append(event.ydata)
#     leg.ee(x)
#     return leg.angles
    

# if __name__=='__main__':



#from scipy.integrate import trapz

# def find_nearest(array,value):
#     idx = (np.abs(array-value)).argmin()
#     return array[idx]

# Simple mouse click function to store coordinates
def onclick(event):
    global ix, iy
    ix, iy = event.xdata, event.ydata

    # assign global variable to access outside of function
    global coords
    coords=[ix,iy]

    # Disconnect after 2 clicks
    fig.canvas.mpl_disconnect(cid)
    plt.close(1)
    return



if __name__ =="__main__":

    while(True):
        leg=Actuator(['y',[0.0, 7.7, 0.0], 'z', [12.5, 0.0, 0.0], 'z', [12.5,0.0,0.0], 'z', [8.2, 0,0.0],'z',[2.,0.0,0.],[0.,0.,5.2],[0,-12.0,0.]])
        angles=[0,0,0,0,0]
        leg.angles=np.deg2rad(angles)
        arm=Arm()
        arm.set_angles(angles)
        thisx=[0]+arm.cord[:,0].tolist()
        thisy=[0]+arm.cord[:,1].tolist()


        fig=plt.figure(1)
        ax=fig.add_subplot(111)
        ax.plot(thisx,thisy)

        coords=[]
        
        cid=fig.canvas.mpl_connect('button_press_event',onclick)
        plt.show(1)

        fig = plt.figure(1)
        ax = fig.add_subplot(111)
        ax.plot(thisx,thisy)

        # Call click func
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        plt.show(1)

        coords.append(arm.cord[6][2])
        coords=list(map( lambda x:x/10,coords))
        leg.ee=coords
        angles=leg.angles
        angles=angles*180/np.pi
        arm.set_angles(angles)
        
        fig=plt.figure()
        ax=fig.add_subplot(111)
        ax.grid()
        line,=ax.plot([],[],'o-',lw=3)
        thisx=[0]
        thisy=[0]
        thisz=[0]
        thisx+=arm.cord[:,0].tolist()
        thisy+=arm.cord[:,1].tolist()
        thisz+=arm.cord[:,2].tolist()

        print(arm.cord[6])
        print(coords)

        fig=plt.figure()
        fig.set_figheight(10)
        fig.set_figwidth(10)
        ax1=fig.add_subplot(3,1,1)
        ax1.plot(thisx,thisy, color="red")
        ax2=fig.add_subplot(3,1,2)
        ax2.plot(thisx,thisz, color="blue")
        ax3=fig.add_subplot(3,1,3,projection='3d')
        ax3.plot(thisx,thisz,thisy)
        fig.tight_layout()
        fig.show()
                

