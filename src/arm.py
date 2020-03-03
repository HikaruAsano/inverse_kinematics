import numpy as np
from gym import spaces

class Arm():
    def __init__(self,n_part,length):
        self.n_part=n_part
        self.l=[]
        for i in range(n_part):
            self.l.append(length[i])
        
        self.th=np.zeros(self.n_part)
        self.actions=np.array([[0.5,0,0],[0,0.5,0],[0,0,0.5],[-0.5,0.,0],[0.,-0.5,0],[0,0,-0.5]])
        self.action_space_d=spaces.Discrete(self.actions.shape[0])
        self.goal=np.array([np.sum(length)*np.random.random(),np.sum(length)*np.random.random()])

    def reset(self):
        self.goal=np.array([np.sum(self.l)*np.random.random(),np.sum(self.l)*np.random.random()])
        return np.zeros(self.n_part)

    def random_action(self):
        i=np.random.randint(0,self.actions.shape[0])
        return  list(self.actions[i])

    def step(self,act):
        self.th+=act
        reward=self.reward(act)
        done=self.is_end()
        return self.th,reward,done

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
        error=self.cal_dif()
        return -error  #目的関数は最大化するためマイナスをかけている

    def is_end(self):
        error=self.cal_dif()
        if error<0.3:
            return True
        else:
            return False

   