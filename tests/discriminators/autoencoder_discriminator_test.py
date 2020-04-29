import tensorflow as tf
import hyperchamber as hc
import numpy as np
from hypergan.discriminators.pyramid_discriminator import PyramidDiscriminator
from hypergan.discriminators.autoencoder_discriminator import AutoencoderDiscriminator
from hypergan.gan_component import ValidationException
from hypergan.ops import TensorflowOps
import hypergan as hg

from hypergan.gan_component import GANComponent

from unittest.mock import MagicMock
from tests.mocks import MockDiscriminator, mock_gan, MockInput

from hypergan.discriminators.pyramid_discriminator import PyramidDiscriminator
from hypergan.generators.resizable_generator import ResizableGenerator

config = {
        'initial_depth': 1,
        'activation': tf.nn.tanh,
        'layers': 3,
        'initial_depth': 6,
        'depth_increase' : 3,
        'block' : hg.discriminators.common.standard_block,
        'distance': 'l2_distance',
        'encoder': PyramidDiscriminator,
        'decoder': ResizableGenerator

        }

class AutoencoderDiscriminatorTest(tf.test.TestCase):
    def test_config(self):
        return None #disabled for now
        with self.test_session():
            gan = mock_gan()
            discriminator = AutoencoderDiscriminator(gan, config)
            self.assertEqual(discriminator.config.activation, tf.nn.tanh)

    def test_create(self):
        return None #disabled for now
        with self.test_session():
            remove_d_config = hg.Configuration.default()
            remove_d_config['discriminator'] = None
            remove_d_config['loss'] = None
            remove_d_config['trainer'] = None
            gan = mock_gan(config = remove_d_config)
            discriminator = AutoencoderDiscriminator(gan, config)
            gan.encoder = gan.create_component(gan.config.encoder)
            gan.generator = gan.create_component(gan.config.generator)
            self.assertEqual(int(net.get_shape()[1]), 32)

if __name__ == "__main__":
    tf.test.main()
