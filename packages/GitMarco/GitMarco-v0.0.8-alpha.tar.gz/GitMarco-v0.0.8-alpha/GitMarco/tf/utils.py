import tensorflow as tf


def random_dataset(shape=(32, 10), seed=22):
    """
    :param shape: shape of the desired tensor
    :param seed: random seed
    :return: a random tf tensor of the specified shape
    """
    return tf.random.uniform(shape, seed)

