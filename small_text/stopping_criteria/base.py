from abc import ABC, abstractmethod


class StoppingCriterion(ABC):

    @abstractmethod
    def stop(self, active_learner):
        pass
