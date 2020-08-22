from itertools import cycle

from gym import Wrapper
import metaworld

from env_wrappers.metaworld.render_env import RenderEnv


class MWEnv(Wrapper):
    def __init__(self, task_name, ):
        mt1 = metaworld.MT1(task_name)  # Construct the benchmark, sampling tasks
        Env = mt1.train_classes[task_name]
        env = Env()  # Create an environment with task `pick_place`
        env = RenderEnv(env)
        super().__init__(env)

        def tasks():
            while True:
                mt1 = metaworld.MT1(task_name)  # Construct the benchmark, sampling tasks
                yield from mt1.train_tasks

        self.tasks = tasks()

    def reset(self):
        task = next(self.tasks)
        self.env.set_task(task)  # Set task
        return self.env.reset()


if __name__ == '__main__':
    from cmx import doc

    doc @ """
    # Meta-world Environment Wrapper
    
    To instantiate a single task, do this:
    """
    with doc:
        task_name = "box-close-v1"
        env = MWEnv(task_name)
        frames = []
        for i in range(200):
            obs = env.reset()
            a = env.action_space.sample()
            env.step(a)
            frames.append(env.render('rgb', width=100, height=100))

        doc.video(frames, f"videos/{task_name}.gif")
    doc @ """
    Note that the green marker is not going to set to hover
    above the box unless you call reset.
    """
