from ik.arm import Arm
import numpy as np
from matplotlib import pyplot as plt
from ik.core import Actuator


def onclick(event):
    return x.data,y.data

if __name__=='__main__':

    leg=Actuator(['y',[0.0, 7.7, 0.0], 'z', [12.5, 0.0, 0.0], 'z', [12.5,0.0,0.0], 'z', [8.2, 0,0.0],'z',[2.,0.0,0.],[0.,0.,5.2],[0,-12.0,0.]])
    angles=[0,0,0,0,0]
    leg.angles=np.deg2rad(angles)
    arm=Arm()
    arm.set_angles(angles)
    thisx=[0]
    thisy=[0]
    thisx+=arm.cord[:,0].tolist()
    thisy+=arm.cord[:,1].tolist()
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.plot(thisx,thisy)
    cid=fig.canvas.mpl_connect('button_press_event',onclick)
    plt.show()

