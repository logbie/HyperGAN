#From https://gist.github.com/EndingCredits/b5f35e84df10d46cfa716178d9c862a3
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow.python.ops import control_flow_ops
from tensorflow.python.ops import math_ops
from tensorflow.python.ops import state_ops
from tensorflow.python.framework import ops
from tensorflow.python.training import optimizer
import tensorflow as tf
import hyperchamber as hc
import numpy as np
import inspect
from operator import itemgetter
from hypergan.train_hooks.base_train_hook import BaseTrainHook

class InputFitnessTrainHook(BaseTrainHook):
  "Keep track of Xs with high discriminator values"
  def __init__(self, gan=None, config=None, trainer=None, name="GpSnMemoryTrainHook", memory_size=2, top_k=1):
    super().__init__(config=config, gan=gan, trainer=trainer, name=name)
    gan_inputs = self.gan.inputs.x

    self.input = tf.split(self.gan.inputs.x, self.gan.batch_size(), axis=0)
    fitness = self.gan.loss.d_real
    if self.config.abs:
        fitness = tf.abs(self.gan.loss.d_real)
    if self.config.reverse:
        fitness = -self.gan.loss.d_real
    if self.config.nabs:
        fitness = -tf.abs(self.gan.loss.d_real)
    self.d_real = tf.split(fitness, self.gan.batch_size(), axis=0)
    self.feed_input = tf.split(self.gan.feed_x, self.gan.batch_size(), axis=0)

    self.sample_batch = self.gan.set_x
    cache_count = self.gan.batch_size()
    self.cache = [tf.Variable(tf.zeros_like(self.input[i])) for i in range(len(self.input))]
    print("C ", self.cache, self.input)
    self.set_cache = [tf.assign(c, x) for c, x in zip(self.cache, self.input)]
    self.restore_cache = [tf.assign(self.gan.inputs.x[i], tf.reshape(self.cache[i], self.ops.shape(self.gan.inputs.x[i]))) for i in range(self.gan.batch_size())]
    #for i in range(self.gan.batch_size()):
    #    restore = []
    #    for j in range(self.gan.batch_size()):
    #        op = tf.assign(self.gan.inputs.x[i], tf.reshape(self.cache[j], self.ops.shape(self.gan.inputs.x[i])))
    #        restore.append(op)
    #    self.restore_cache.append(restore)
    self.loss = [None, None]
    if self.config.k_lipschitz is not None:
        klip = self.gan.configurable_param(self.config.k_lipschitz)
        k_lip = tf.nn.relu(tf.abs(tf.reduce_mean(self.gan.loss.d_real-self.gan.loss.d_fake))-klip)
        self.gan.add_metric("k_lip", k_lip)
        self.loss = [k_lip, None]

  def after_step(self, step, feed_dict):
    pass

  def losses(self):
      return self.loss

  def before_step(self, step, feed_dict):
    def sort():
        score_index = np.argsort(np.array(scores).flatten())
        score_index = score_index[:self.gan.batch_size()]

        sticky = 0
        total = 0
        for i in range(self.gan.batch_size()):
            scorei = score_index[i]
            if (i+self.gan.batch_size()) not in score_index:
                sticky+=1
                self.gan.session.run(self.restore_cache[i])
            total += 1
        if total == sticky or sticky == 0:
            print("Sticky "+str(sticky) + " / "+ str(total))

    for i in range(self.config.search_steps or 1):
        scores = []
        scores += self.gan.session.run(self.d_real)
        self.gan.session.run(self.set_cache)
        self.gan.session.run(self.sample_batch)
        scores += self.gan.session.run(self.d_real)
        sort()

