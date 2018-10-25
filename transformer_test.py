import numpy as np
import tensorflow as tf
from transformer import Transformer


class TransformerTest(tf.test.TestCase):
    def setUp(self):
        self.t = Transformer()
        self.batch_size = 4
        self.seq_len = 5
        self.input_ph = tf.placeholder(tf.int32, shape=(self.batch_size, self.seq_len))

    def test_construct_padding_mask(self):
        with self.test_session() as sess:
            data = np.array([
                [1, 2, 3, 4, 5],
                [1, 2, 0, 0, 0],
                [1, 2, 3, 4, 0],
                [1, 2, 3, 0, 0],
            ])
            mask_ph = self.t.construct_padding_mask(self.input_ph)
            mask = sess.run(mask_ph, feed_dict={self.input_ph: data})
            expected = np.array([
                [[1., 1., 1., 1., 1.]] * self.seq_len,
                [[1., 1., 0., 0., 0.]] * self.seq_len,
                [[1., 1., 1., 1., 0.]] * self.seq_len,
                [[1., 1., 1., 0., 0.]] * self.seq_len,
            ])
            np.testing.assert_array_equal(mask, expected)

    def test_construct_autoregressive_mask(self):
        with self.test_session() as sess:
            data = np.random.randint(5, size=(self.batch_size, self.seq_len))
            tri_matrix = [[1, 0, 0, 0, 0],
                          [1, 1, 0, 0, 0],
                          [1, 1, 1, 0, 0],
                          [1, 1, 1, 1, 0],
                          [1, 1, 1, 1, 1]]
            expected = np.array([tri_matrix] * self.batch_size).astype(np.float32)
            mask_ph = self.t.construct_autoregressive_mask(self.input_ph)
            mask = sess.run(mask_ph, feed_dict={self.input_ph: data})
            np.testing.assert_array_equal(mask, expected)

    def test_label_smoothing(self):
        pass