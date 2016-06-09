# -*- coding: utf-8 -*-
from __future__ import absolute_import
import random
from typing import List, Tuple, Any, Optional

from scipy import sparse as sp


class ExperienceMemory:
    """
    Experience replay memory.

    We're using state-action value $Q(a)$ functions with Q-learning algorithm.
    To learn Q function we need "training examples":

    * $a_t$ action taken (i.e. link followed);
    * $r_{t+1}$ observed reward (e.g. whether a form is found or
      is a page on-topic);
    * a set of actions $A_{t+1}$ (i.e. links) available at this page;
      next action $a_{t+1} \in A_{t+1}$ used for TD updates is chosen
      from this set. In Q-learning it is a link with the highest $Q(a_{t+1})$
      score; we need to store all available actions because $Q$ function
      changes over time.

    FIXME/TODO:
    * discount $\gamma$? How does it work? There is a footnote in
      http://arxiv.org/pdf/1511.05952v4.pdf;
    * $s_t$ state (information about the page the link is extracted from);
    * $s_{t+1}$ state (information about the page the link leads to) - what
      is it for?
    * multiple rewards for multiple tasks

    With this data we can train a regression model for $Q(s,a)$ function:

    $$R_{predicted} = Q(s_t, a_t)$$
    $$R_{observed TD} = r_{t+1} + \gamma*Q(s_{t+1}, a_{t+1}), 0 <= \gamma <= 1$$

    """
    def __init__(self):
        self.data = []  # TODO: more efficient storage

    def add(self, a_t, A_t1, r_t1) -> None:
        # if A_t1 is None:
        #     A_t1 = sp.csr_matrix((0, a_t.shape[1]))
        self.data.append((a_t, A_t1, r_t1))

    def sample(self, k: Optional[int]) -> List[Tuple[Any, Any, Any]]:
        if k is None:
            k = len(self.data)
        k = min(k, len(self.data))
        sample = random.sample(self.data, k)
        # actions, available_actions, rewards = zip(*sample)
        return sample

    def clear(self) -> None:
        self.data.clear()

    def __len__(self) -> int:
        return len(self.data)
