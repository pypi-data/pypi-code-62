import gym
from gym import error, spaces, utils
from gym.utils import seeding

import os
import pybullet as p
import pybullet_data
import math
import numpy as np
import random

MAX_EPISODE_LEN = 20*100
JOINTS=[0,1,4,5]

class NFEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    _max_episode_steps=MAX_EPISODE_LEN

    def __init__(self):
        self.step_counter = 0
        #p.connect(p.GUI)
        p.connect(p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.action_space = spaces.Box(np.array([-1]*4), np.array([1]*4))
        self.observation_space = spaces.Box(np.array([-1]*14), np.array([1]*14))

    def reset(self):
        self.step_counter = 0
        p.resetSimulation()
        p.setGravity(0,0,-10)
        self.plane_id = p.loadURDF("plane.urdf")
        cubeStartPos = [0,0,2.5]
        cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])
        self.bot_id = p.loadURDF("/Users/dj/stuff/bot/urdf/bot4.urdf",cubeStartPos, cubeStartOrientation)

        maxForce = 0
        mode = p.VELOCITY_CONTROL
        for i in range(8):
            p.setJointMotorControl2(self.bot_id, i, controlMode=mode, force=maxForce)

        c = p.createConstraint(self.bot_id, 1, self.bot_id, 3, jointType=p.JOINT_GEAR,jointAxis =[1,0,0],parentFramePosition=[0,0,0],childFramePosition=[0,0,0])
        p.changeConstraint(c, gearRatio=-1, maxForce=10000)

        c = p.createConstraint(self.bot_id, 1, self.bot_id, 2, jointType=p.JOINT_GEAR,jointAxis =[1,0,0],parentFramePosition=[0,0,0],childFramePosition=[0,0,0])
        p.changeConstraint(c, gearRatio=1, maxForce=10000)

        c = p.createConstraint(self.bot_id, 5, self.bot_id, 7, jointType=p.JOINT_GEAR,jointAxis =[1,0,0],parentFramePosition=[0,0,0],childFramePosition=[0,0,0])
        p.changeConstraint(c, gearRatio=-1, maxForce=10000)

        c = p.createConstraint(self.bot_id, 5, self.bot_id, 6, jointType=p.JOINT_GEAR,jointAxis =[1,0,0],parentFramePosition=[0,0,0],childFramePosition=[0,0,0])
        p.changeConstraint(c, gearRatio=1, maxForce=10000)

        obs=[]
        for i in range(4):
            joint_no=JOINTS[i]
            res=p.getJointState(self.bot_id, joint_no)
            obs.append(res[0])
            obs.append(res[1])
        res=p.getBaseVelocity(self.bot_id)
        obs+=res[0] # lin vel (3)
        obs+=res[1] # ang vel (3)
        self.observation = obs 
        return np.array(self.observation).astype(np.float32)

    def step(self, action):
        mode = p.TORQUE_CONTROL
        for i in range(4):
            force=action[i]*100
            joint_no=JOINTS[i]
            p.setJointMotorControl2(self.bot_id, joint_no, controlMode=mode, force=force)

        p.stepSimulation()

        pos=p.getBasePositionAndOrientation(self.bot_id)[0]
        if pos[2]<=0.8:
            reward = -100
            done = True
        else:
            reward = 1
            done = False

        self.step_counter += 1
        if self.step_counter > MAX_EPISODE_LEN:
            reward = 0
            done = True

        info = {}

        obs=[]
        for i in range(4):
            joint_no=JOINTS[i]
            res=p.getJointState(self.bot_id, joint_no)
            obs.append(res[0]) # pos
            obs.append(res[1]) # vel
        res=p.getBaseVelocity(self.bot_id)
        obs+=res[0] # lin vel (3)
        obs+=res[1] # ang vel (3)
        self.observation = obs 

        return np.array(self.observation).astype(np.float32), reward, done, info

    def render(self):
        pass

    def _get_state(self):
        return self.observation

    def close(self):
        p.disconnect()
