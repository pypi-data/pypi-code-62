from gym.envs import register
from gym.error import Error
from metaworld.envs.mujoco.env_dict import ALL_V1_ENVIRONMENTS

ALL_ENVS = []

if __name__ != '__main__':
    for task_name in ALL_V1_ENVIRONMENTS:
        ID = f'{task_name.capitalize()}'
        register(id=ID,
                 entry_point='env_wrappers.metaworld.mw_env:MWEnv',
                 kwargs=dict(task_name=task_name,
                             # width=84, height=84, frame_skip=4
                             ),
                 )
        ALL_ENVS.append(ID)
else:
    from cmx import doc

    doc @ """
    # Metaworld Environment Wrappers
    
    This module includes wrappers that are required to work 
    with `metaworld` [link](https://github.com/rlworkgroup/metaworld).
    In particular, we implemented a camera wrapper that directly
    taps into the underlying `env.sim.render` function as opposed
    to the gym environment `env.render` which is not implemented
    in metaworld [L:111-113](https://github.com/rlworkgroup/metaworld/blob/master/metaworld/envs/mujoco/mujoco_env.py#L109-L111).
    
    This wrapper makes it easy.
    
    # Usage Example
    
    We register single task metaworld environments under the 
    `env_wrappers.metaworld` module, so that you can use `gym
    .make` to create the environments without have to import
    `metaworld` manually.
    """
    with doc:
        import gym
        from env_wrappers.metaworld import ALL_ENVS

        for env_id in ALL_ENVS:
            env = gym.make(f'env_wrappers.metaworld:{env_id}')
            frames = []
            for i in range(10):
                env.reset()
                frames.append(env.render("rgb", width=240, height=240))
            doc.video(frames, f"videos/{env_id}.gif")
            break
    doc @ """
    The full list of environments are
    """
    doc.yaml @ ALL_ENVS
    doc.flush()

