import torch


__all__ = ["build_mse_loss", "build_mae_loss", "build_sae_loss"]


class LossFnError(Exception):
    pass


def build_mse_loss(properties, loss_tradeoff=None, weight: float = 1.0):
    """
    Build the mean squared error loss function.

    Args:
        properties (list): mapping between the model properties and the dataset properties
        loss_tradeoff (list or None): multiply loss value of property with tradeoff factor

    Returns:
        mean squared error loss function

    """
    if loss_tradeoff is None:                 loss_tradeoff = [1] * len(properties)
    if len(properties) != len(loss_tradeoff): raise LossFnError("loss_tradeoff must have same length as properties!")


    def loss_fn(batch, result):
        loss = 0.0
        for prop, factor in zip(properties, loss_tradeoff):
            diff   = batch[prop] - result[prop]
            diff   = diff ** 2
            err_sq = weight * factor * torch.sum(diff)
            loss  += err_sq
        return loss

    return loss_fn

def build_sae_loss(properties, loss_tradeoff=None, weight: float = 1.0):
    """
    Build the sum abs error loss function.

    Args:
        properties (list): mapping between the model properties and the dataset properties
        loss_tradeoff (list or None): multiply loss value of property with tradeoff factor

    Returns:
        sum abs error loss function

    """
    if loss_tradeoff is None:                 loss_tradeoff = [1] * len(properties)
    if len(properties) != len(loss_tradeoff): raise LossFnError("loss_tradeoff must have same length as properties!")

    def loss_fn(batch, result):
        loss = 0.0
        for prop, factor in zip(properties, loss_tradeoff):
            diff  = batch[prop] - result[prop]
            err   = weight * factor * torch.sum(torch.abs(diff))
            loss += err
        return loss

    return loss_fn

def build_mae_loss(properties, loss_tradeoff=None, weight:float = 1.0):
    """
    Build the mean absolute error loss function.

    Args:
        properties (list): mapping between the model properties and the dataset properties
        loss_tradeoff (list or None): multiply loss value of property with tradeoff factor

    Returns:
        mean absolute error loss function

    """
    if loss_tradeoff is None:                 loss_tradeoff = [1] * len(properties)
    if len(properties) != len(loss_tradeoff): raise LossFnError("loss_tradeoff must have same length as properties!")

    def loss_fn(batch, result):
        loss = 0.0
        for prop, factor in zip(properties, loss_tradeoff):
            diff   = batch[prop] - result[prop]
            err_sq = weight * factor * torch.mean(torch.abs(diff))
            loss  += err_sq
        return loss

    return loss_fn

