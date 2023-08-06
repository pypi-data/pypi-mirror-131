import ctypes
import sys
from pathlib import Path

import torch
from torch.onnx import register_custom_op_symbolic
from torch.utils.cpp_extension import load


def _python_version() -> str:
    return ''.join(str(n) for n in sys.version_info[:2])


def _torch_version() -> str:
    return ''.join(torch.__version__.split('.')[:2])


try:
    # Try to compile torch extension if it possible.
    load(
        name='fake_quantization_anchor',
        sources=[str(Path(__path__[0]).joinpath('fake_quantization_anchor.cpp').resolve())]
    )
except Exception:
    # If not, load precomplied extension.
    _loaded_libs = [
        ctypes.CDLL('libc10.so', mode=ctypes.RTLD_GLOBAL),
        ctypes.CDLL('libtorch.so', mode=ctypes.RTLD_GLOBAL),
        ctypes.CDLL('libtorch_cpu.so', mode=ctypes.RTLD_GLOBAL),
        ctypes.CDLL('libtorch_python.so', mode=ctypes.RTLD_GLOBAL),
    ]
    so_path = Path(__path__[0]).joinpath(
        f'fake_quantization_anchor_cp{_python_version()}_torch{_torch_version()}.so'
    ).resolve()
    torch.ops.load_library(str(so_path))


def _fake_quantization_anchor_symbolic_fn(g, x: torch.Tensor, threshold: torch.Tensor) -> torch.Tensor:
    return g.op('enot::fake_quantization_anchor', x, threshold)


register_custom_op_symbolic(
    symbolic_name='enot::fake_quantization_anchor',
    symbolic_fn=_fake_quantization_anchor_symbolic_fn,
    opset_version=9,
)
