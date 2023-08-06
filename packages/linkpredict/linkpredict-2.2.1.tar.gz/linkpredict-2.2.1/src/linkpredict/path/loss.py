from .base import MediumLoss

from ..utils import make_callable


class SimpleMediumLoss(MediumLoss):

    def __init__(self, medium_loss):
        self.loss = make_callable(medium_loss)

    def get_loss(self, time=None):
        return self.loss(time)
