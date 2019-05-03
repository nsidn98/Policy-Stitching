import numpy as np
from gym import utils
from gym.envs.mujoco import mujoco_env

from gym.envs.mujoco.jaco import JacoEnv

<<<<<<< HEAD
=======
def goal_distance(goal_a, goal_b):
    assert goal_a.shape == goal_b.shape
    return np.linalg.norm(goal_a - goal_b, axis=-1)
>>>>>>> b4703b0dadbece0501a272c63f63f8dd97017d99

class JacoPickEnv(JacoEnv):
    def __init__(self, with_rot=1):
        super().__init__(with_rot=with_rot)
        self._config.update({
            "pick_reward": 10,
            "random_box": 0.1,
        })
        self._context = None
        self._norm = False
<<<<<<< HEAD
=======
        self.distance_threshold = 0.02
>>>>>>> b4703b0dadbece0501a272c63f63f8dd97017d99

        # state
        self._pick_count = 0
        self._init_box_pos = np.asarray([0.5, 0.0, 0.04])

        # env info
        self.reward_type += ["pick_reward", "success"]
        self.ob_type = self.ob_shape.keys()

        mujoco_env.MujocoEnv.__init__(self, "jaco_pick.xml", 4)
        utils.EzPickle.__init__(self)

    def set_norm(self, norm):
        self._norm = norm

    def set_context(self, context):
        self._context = context

    def _step(self, a):
        self.do_simulation(a, self.frame_skip)

        ob = self._get_obs()
        done = False
        success = False
        pick_reward = 0
        ctrl_reward = self._ctrl_reward(a)

        # dist_hand = self._get_distance_hand('box')
        dist_hand = self._get_distance_hand('target')
        box_z = self._get_box_pos()[2]
        in_air = box_z > 0.08
        on_ground = box_z < 0.08
        in_hand = dist_hand < 0.08

        # pick
        if in_air and in_hand:
            pick_reward = self._config["pick_reward"] * box_z
            self._pick_count += 1

        # fail
<<<<<<< HEAD
        if on_ground and self._pick_count > 0:
            done = True

        # success
        if self._pick_count == 50:
            success = True
            done = True
=======
        # if on_ground and self._pick_count > 0:
            # done = True

        done = False
        # success
        if self._pick_count == 50:
            success = True
            # done = True
>>>>>>> b4703b0dadbece0501a272c63f63f8dd97017d99
            print('success')

        reward = ctrl_reward + pick_reward
        info = {"ctrl_reward_sum": ctrl_reward,
                "pick_reward_sum": pick_reward,
                "success_sum": success}
        return ob, reward, done, info

    # def _get_obs(self):
    #     qpos = self.sim.data.qpos
    #     qvel = self.sim.data.qvel
    #     obs = np.concatenate([qpos, qvel]).ravel()
    #     if self._norm:
    #         std = [5, 10, 20, 50, 100, 150, 0.2, 0.2,
    #                0.2, 1, 0.2, 1, 1, 0.2, 0.2, 0.2,
    #                50, 50, 70, 70, 100, 100, 50, 50,
    #                50, 5, 2, 10, 50, 50, 50]
    #         obs /= std
    #     return obs

    def _get_obs(self):
        # print('GET OBS\n\n')
        # positions
<<<<<<< HEAD
        grip_pos = self.sim.data.get_joint_qpos('jaco_joint_finger_1')
        dt = self.sim.nsubsteps * self.sim.model.opt.timestep
        grip_velp = self.sim.data.get_joint_qvel('jaco_joint_finger_1') * dt
        object_pos = self._get_pos('target')
=======
        # grip_pos = self.sim.data.get_site_xpos('jaco:grip')
        grip_pos = self._get_pos("jaco_link_hand")
        print("Grip pos", grip_pos)
        # grip_pos = self._get_hand_pos()
        # dt = self.sim.nsubsteps * self.sim.model.opt.timestep
        # grip_velp = self.sim.data.get_joint_qvel('jaco_joint_6') * dt
        object_pos = self._get_pos('target')
        # print("Obj pos:",object_pos.ravel)
>>>>>>> b4703b0dadbece0501a272c63f63f8dd97017d99
        object_rel_pos = object_pos - grip_pos
        # achieved_goal = grip_pos.copy()
        achieved_goal = object_pos.copy()
        # print('Position')
        # print(grip_pos,object_pos,object_rel_pos)
        # print()
<<<<<<< HEAD
        obs = np.concatenate([
            [grip_pos], object_pos.ravel(), object_rel_pos.ravel()])
=======
        # print("Grip pos: ",grip_pos)

        obs = np.concatenate([grip_pos, object_pos.ravel(), object_rel_pos.ravel()])
>>>>>>> b4703b0dadbece0501a272c63f63f8dd97017d99
        # print("grip pos, object pos, relpos")
        # print(grip_pos)
        # print(self.sim.data.get_joint_qpos('jaco_joint_finger_2'))
        # print(self.sim.data.get_joint_qpos('jaco_joint_finger_3'))
        # print(object_pos.ravel())
        # print(object_rel_pos.ravel())
        # return {
        #     'observation': obs.copy(),
        #     'achieved_goal': achieved_goal.copy(),
        #     'desired_goal': self.goal.copy(),
        # }
        # print('GOAL SHAPE jaco_pick.py')
        # print(self.goal.shape)
        # print('GOAL!!!! jaco_pick.py',self.goal.shape)
        # print('ACHIEVED GOAL!!! jaco_pick.py',achieved_goal.shape)
        # print(type(float(self.goal)))
        # print(type(self.goal))
        # print(type(achieved_goal))
        return {
            'observation': obs.copy(),
            'achieved_goal': achieved_goal.copy(),
             'desired_goal': (self.goal.copy()),
        }
            
        

    def get_ob_dict(self, ob):
        return {'joint': ob}

    def reset_box(self):
        qpos = self.sim.data.qpos.ravel().copy()
        qvel = self.sim.data.qvel.ravel().copy()

        # set box's initial position
        sx, sy, ex, ey = -1, -1, 1, 1
        if self._context == 0:
            sx, sy = 0, 0
        elif self._context == 1:
            ex, sy = 0, 0
        elif self._context == 2:
            sx, ey = 0, 0
        elif self._context == 3:
            ex, ey = 0, 0

        self._init_box_pos = np.asarray(
            [0.5 + np.random.uniform(sx, ex) * self._config["random_box"],
             0.1 + np.random.uniform(sy, ey) * self._config["random_box"],
             0.04])
        qpos[9:12] = self._init_box_pos

        self.set_state(qpos, qvel)

        self._pick_count = 0

    def reset_model(self):
        qpos = self.init_qpos + self.np_random.uniform(low=-.005, high=.005, size=self.model.nq)
        qvel = self.init_qvel + self.np_random.uniform(low=-.005, high=.005, size=self.model.nv)
        # print('QPOS QVEL')
        # print(qpos,qvel)
        # print()
        self.set_state(qpos, qvel)

        self.reset_box()

        return self._get_obs()
<<<<<<< HEAD
=======

    def compute_reward(self, achieved_goal, goal, info):
        # Compute distance between goal and the achieved goal.
        d = goal_distance(achieved_goal, goal)
        if self.reward_type == 'sparse':
            return -(d > self.distance_threshold).astype(np.float32)
        else:
            return -d
>>>>>>> b4703b0dadbece0501a272c63f63f8dd97017d99
