import tensorflow as tf
import hypergan as hg
import hyperchamber as hc
import numpy as np

from hypergan.samplers.static_batch_sampler import StaticBatchSampler
from hypergan.gan_component import ValidationException
from hypergan.ops import TensorflowOps
from tests.mocks import mock_gan

class StaticBatchSamplerTest(tf.test.TestCase):
    def test_sample(self):
        with self.test_session():
            gan = mock_gan()

            sampler = StaticBatchSampler(gan)
            self.assertEqual(sampler._sample()['generator'].shape[-1], 1)

if __name__ == "__main__":
    tf.test.main()
