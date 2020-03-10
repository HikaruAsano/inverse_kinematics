import numpy as np
from gym import spaces

class Arm():
    def __init__(self,n_part,length):
        self.n_part=n_part
        self.l=[]
        for i in range(n_part):
            self.l.append(length[i])
        
        self.th=np.zeros(self.n_part)
        self.actions=np.array([[np.pi/1000,0,0,0],[0,np.pi/1000,0,0],[0,0,np.pi/1000,0],[-np.pi/1000,0.,0,0],[0.,-np.pi/1000,0,0],[0,0,-np.pi/1000,0],[0,0,0,np.pi/1000],[0,0,0,-np.pi/1000]])
        self.action_space_d=spaces.Discrete(self.actions.shape[0])
        pi=np.random.random()
        self.goal=np.array([np.sum(length)*(np.cos(pi*2*np.pi)),np.sum(length)*(np.sin(pi*2*np.pi))])
        self.state=np.concatenate([self.th, self.goal], 0)
 
    def reset(self):
        pi=np.random.random()
        self.goal=np.array([np.sum(self.l)*(np.cos(pi*2*np.pi)),np.sum(self.l)*(np.cos(pi*2*np.pi))])
        self.th=np.zeros(self.n_part)
        return np.concatenate([self.th, self.goal], 0)

    def random_action(self):
        return np.random.randint(0,self.actions.shape[0])
        
    def forward(self):
        pos=np.zeros((self.n_part,2))
        x=0
        y=0
        j=0
        for i in range(self.n_part):  
            j=i+1       
            x+=self.l[i]*np.cos( np.sum(self.th[:j]) )
            y+=self.l[i]*np.sin( np.sum(self.th[:j]) )
            pos[i,0]=x
            pos[i,1]=y
        return pos

    def step(self,act):
        self.th+=self.actions[act]
        reward=self.reward(act)
        done=self.is_end()
        self.state=np.concatenate([self.th, self.goal], 0)
        return self.state,reward,done

    def cal_dif(self):
        x=0
        y=0
        for i in range(self.n_part):
            x+=self.l[i]*np.cos( np.sum(self.th[:i]) )
            y+=self.l[i]*np.sin( np.sum(self.th[:i]) )
        x_error=self.goal[0]-x
        y_error=self.goal[1]-y
        return x_error*x_error+y_error*y_error
    
    def reward(self,act):
        reward=0
        error=self.cal_dif()
        if error < 0.1:
            return 1
        if error < 0.05:
            return 5
        if error < 0.01:
            return 10
        else:
             return - error

    def is_end(self):
        error=self.cal_dif()
        if error<0.01:
            return True
        else:
            return False