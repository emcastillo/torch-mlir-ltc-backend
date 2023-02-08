import torch
import torch._lazy
import torch_mlir._mlir_libs._REFERENCE_LAZY_BACKEND as lazy_backend

# Register the example LTC backend.
lazy_backend._initialize()

device = 'lazy'


class ConvLinear(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.lin = torch.nn.Linear(10, 1)

    def forward(self, x):
        return self.lin(x)

module = ConvLinear()
module.eval()
inputs = torch.randn(10).to(device)
module.to(device)
outputs = module(inputs)
torch._lazy.mark_step()
print('Results:', outputs)

# Optionally dump MLIR graph generated from LTC trace.
computation = lazy_backend.get_latest_computation()
if computation:
    print(computation.debug_string())
