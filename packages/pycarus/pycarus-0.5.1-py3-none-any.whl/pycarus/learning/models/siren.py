from typing import List, Tuple, cast

import numpy as np
import torch
from torch import Tensor, nn


class Sine(nn.Module):
    def __init__(self) -> None:
        super().__init__()  # type: ignore

    def forward(self, x: Tensor) -> Tensor:
        return torch.sin(30 * x)


def weights_init(m: nn.Module) -> None:
    with torch.no_grad():  # type: ignore
        if hasattr(m, "weight"):
            lin = cast(nn.Linear, m)
            num_input = lin.weight.size(-1)
            lin.weight.uniform_(-np.sqrt(6 / num_input) / 30, np.sqrt(6 / num_input) / 30)


def first_layer_weights_init(m: nn.Module) -> None:
    with torch.no_grad():  # type: ignore
        if hasattr(m, "weight"):
            lin = cast(nn.Linear, m)
            num_input = lin.weight.size(-1)
            lin.weight.uniform_(-1 / num_input, 1 / num_input)


class SIREN(nn.Module):
    def __init__(
        self,
        input_dim: int,
        hidden_dim: int,
        num_hidden_layers: int,
        out_dim: int,
    ) -> None:
        super().__init__()  # type: ignore

        self.layers = nn.ModuleList()

        self.layers.append(nn.Sequential(nn.Linear(input_dim, hidden_dim), Sine()))
        for _ in range(num_hidden_layers):
            self.layers.append(nn.Sequential(nn.Linear(hidden_dim, hidden_dim), Sine()))
        self.layers.append(nn.Linear(hidden_dim, out_dim))

        self.layers.apply(weights_init)
        self.layers[0].apply(first_layer_weights_init)

    def forward(self, coordinates: Tensor) -> Tuple[Tensor, List[Tensor]]:
        features: List[Tensor] = []

        f = coordinates
        for layer in self.layers:
            f = layer(f)
            features.append(torch.clone(f))

        return f, features
