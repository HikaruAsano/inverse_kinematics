import chainer 
import chainer.functions as F 
import chainer.links as L 
import chainerrl
import gym
import numpy as np
from gym import spaces
from arm import Arm




class QFunction(chainer.Chain):

    def __init__(self,obs_size,n_actions,n_hidden_channels=50):
        super().__init__()
        with self.init_scope():
            self.l0=L.Linear(obs_size,n_hidden_channels)
            self.l1=L.Linear(n_hidden_channels,n_hidden_channels*2)
            self.l2=L.Linear(n_hidden_channels*2,n_hidden_channels*2)
            self.l3=L.Linear(n_hidden_channels*2,n_actions)

    def __call__(self,x,test=False):
        h=F.tanh(self.l0(x))
        h=F.tanh(self.l1(h))
        h=F.tanh(self.l2(h))
        return chainerrl.action_value.DiscreteActionValue(self.l3(h))

if __name__ == "__main__":
    env=Arm(4,[1.,1.,1.,1.])
    print('observation space:',env.state)
    print('action space:',env.actions)
    obs=env.reset()

    #env.render()
    print('initial observation:',obs)

    action=env.random_action()
    print(action)
    state,r,done=env.step(action)
    print('next observation:',state)
    print('reward:',r)
    env.actions.shape[0]

    obs_size=env.state.shape[0]
    n_actions=env.actions.shape[0]
    q_func=QFunction(obs_size,n_actions)

    optimizer=chainer.optimizers.Adam(eps=1e-2)
    optimizer.setup(q_func)

    gamma=0.99

    #######################################
    explorer=chainerrl.explorers.ConstantEpsilonGreedy(
        epsilon=0.2,random_action_func=env.action_space_d.sample)

    replay_buffer=chainerrl.replay_buffer.ReplayBuffer(capacity=10**6)
    phi=lambda x:x.astype(np.float32,copy=False)
    agent=chainerrl.agents.DoubleDQN(
        q_func,optimizer,replay_buffer,gamma,explorer,
        replay_start_size=500,update_interval=1,target_update_interval=100,phi=phi)

    n_episodes = 10000
    max_episode_len = 3000
    for i in range(1, n_episodes + 1):
        obs = env.reset()
        reward = 0
        done = False
        R = 0  # return (sum of rewards)
        t = 0  # time step
        while not done and t < max_episode_len:
            # Uncomment to watch the behaviour
            # env.render()
            action = agent.act_and_train(obs, reward)
            obs, reward, done = env.step(action)
            R += reward
            t += 1
        #print("total step of this iteration:"+str(t))
        #print("last error of this step:"+str(reward))
        if i % 10 == 0:
            print('episode:', i,
                'R:', R,
                'statistics:', agent.get_statistics())
        agent.stop_episode_and_train(obs, reward, done)
        if i%100==0:
            agent.save("agent_"+str(i))

    print('Finished.')

