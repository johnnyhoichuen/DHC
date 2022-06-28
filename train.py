import os
import random
import time

import torch
import numpy as np
import ray

from worker import GlobalBuffer, Learner, Actor
import configs

os.environ["OMP_NUM_THREADS"] = "1"
torch.manual_seed(0)
np.random.seed(0)
random.seed(0)


def main(num_actors=configs.num_actors, log_interval=configs.log_interval):
    ray.init()

    # init buffer, learner and actor
    buffer = GlobalBuffer.remote()
    learner = Learner.remote(buffer, 16000)
    time.sleep(1)
    actors = [Actor.remote(worker_id=i, epsilon=0.4 ** (1 + (i / (num_actors - 1)) * 7), learner=learner, buffer=buffer)
              for i in range(num_actors)]

    for actor in actors:
        actor.run.remote()

    while not ray.get(buffer.ready.remote()):
        time.sleep(5)
        ray.get(learner.stats.remote(5))
        ray.get(buffer.stats.remote(5))

    print('start training')
    buffer.run.remote()
    learner.run.remote()

    done = False
    while not done:
        time.sleep(log_interval)
        done = ray.get(learner.stats.remote(log_interval))
        ray.get(buffer.stats.remote(log_interval))
        print()


if __name__ == '__main__':
    main()
