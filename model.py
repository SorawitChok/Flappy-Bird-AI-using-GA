import torch
import torch.nn as nn

class FlappyBirdModel(nn.Module):
    def __init__(self, input_dim: int, hidden_1: int, output_dim: int, allow_bias: bool = False):
        super().__init__()
        self.layer_1 = nn.Linear(input_dim, hidden_1, allow_bias)
        self.layer_2 = nn.Linear(hidden_1, output_dim, allow_bias)
    
    def forward(self, input: torch.Tensor):
        x = self.layer_1(input)
        x = self.layer_2(x)
        return x
