import numpy as np

from small_text.data.sampling import _get_class_histogram
from small_text.integrations.pytorch.exceptions import PytorchNotFoundError

try:
    import torch
    from torch.utils.data import DataLoader
    from torch.utils.data.sampler import BatchSampler, SequentialSampler, RandomSampler
except ImportError:
    raise PytorchNotFoundError('Could not import pytorch')


def dataloader(data_set, batch_size, collate_fn, train=True):
    """
    Convenience method to obtain a `DataLoader`.

    Parameters
    ----------
    data_set : small_text.data.Dataset
        The target dataset.
    batch_size : int
        Batch size.
    collate_fn : func
        The `collate-fn` required by `DataLoader`.
    train : bool
        Indicates if the dataloader is used for training or testing. For training random sampling
        is used, otherwise sequential sampling.

    Returns
    -------
    iter : DataLoader
        A DataLoader for the given `data_set`.
    """
    data_set = np.array(data_set, dtype=object, copy=False)

    if train:
        base_sampler = RandomSampler(data_set)
    else:
        base_sampler = SequentialSampler(data_set)

    sampler = BatchSampler(
        base_sampler,
        batch_size=batch_size,
        drop_last=False)

    return DataLoader(data_set,
                      batch_size=None,
                      collate_fn=collate_fn,
                      sampler=sampler)


def get_class_weights(y, num_classes, eps=1e-8):
    label_counter = _get_class_histogram(y, num_classes, normalize=False)
    pos_weight = torch.ones(num_classes, dtype=torch.float)
    num_samples = len(y)
    for c in range(num_classes):
        pos_weight[c] = (num_samples - label_counter[c]) / (label_counter[c] + eps)

    if num_classes == 2:
        pos_weight[pos_weight.argmin()] = 1.0

    return pos_weight
