# -*- coding: utf-8 -*-
"""Copy of DiffusionDDPM.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1k7VP7fIWBjQNMQTdVngqR9BC0Q-3ONC6
"""

# !pip install modular-diffusion

# %cd /content/drive/MyDrive/
#!git clone https://github.com/cabralpinto/modular-diffusion.git

import shutil
import sys
from pathlib import Path

import torch
from einops import rearrange
from torchvision.datasets import ImageFolder
from torchvision.transforms import ToTensor
from torchvision.transforms.functional import resize
from torchvision.utils import save_image

import shutil
from pathlib import Path

import requests
from sentencepiece import SentencePieceProcessor, SentencePieceTrainer
from tqdm import tqdm

import os

# Get current working directory
current_path = os.getcwd()

print("Current Working Directory:", current_path)


input = "/data/dog"

c, h, w, p, q = 3, 64, 64, 2, 2
x, _ = zip(*ImageFolder(str(input), ToTensor()))
x = torch.stack(x) * 2 - 1
x = resize(x, [h, w], antialias=False)
x = rearrange(x, "b c (h p) (w q) -> b (h w) (c p q)", p=p, q=q)

import diffusion
from diffusion.data import Identity
from diffusion.loss import Simple
from diffusion.net import Transformer
from diffusion.noise import Gaussian
from diffusion.schedule import Cosine

model = diffusion.Model(
    data=Identity(x, batch=16, shuffle=True),
    schedule=Cosine(1000),
    noise=Gaussian(parameter="epsilon", variance="fixed"),
    net=Transformer(input=x.shape[2], width=768, depth=12, heads=12),
    loss=Simple(parameter="epsilon"),
    device="cuda" if torch.cuda.is_available() else "cpu",
)

file = Path.cwd()
input = file.parent / "modular-diffusion/examples/data/representative/in/afhq"
input.parent.mkdir(parents=True, exist_ok=True)
output = file.parent / "modular-diffusion/examples/data/representative/out" / file.stem
output.mkdir(parents=True, exist_ok=True)
torch.set_float32_matmul_precision("high")
torch.set_grad_enabled(False)

epoch = sum(1 for _ in output.glob("[0-9]*"))
for epoch, loss in enumerate(model.train(epochs=10000), epoch + 1):
    z = model.sample(batch=10)
    print(z[-1].min().item(), z[-1].max().item(), flush=True)
    z = z[torch.linspace(0, z.shape[0] - 1, 10).int()]
    z = rearrange(z, "t b (h w) (c p q) -> c (b h p) (t w q)", h=h // p, p=p, q=q)
    z = (z + 1) / 2
    save_image(z, output / f"{epoch}-{loss:.2e}.png")
    model.save(output / "model.pt")

import diffusion
from diffusion.data import Identity
from diffusion.loss import Simple
from diffusion.net import UNet
from diffusion.noise import Gaussian
from diffusion.schedule import Linear

model = diffusion.Model(
    data=Identity(x, batch=128, shuffle=True),
    schedule=Linear(1000, 0.9999, 0.98),
    noise=Gaussian(parameter="epsilon", variance="fixed"),
    net=UNet(channels=(1, 64, 128, 256)),
    loss=Simple(parameter="epsilon"),
    device="cuda" if torch.cuda.is_available() else "cpu",
)

# model.save("model.pt")

# losses = [*model.train(epochs=5)]#
# z = model.sample(batch=10)

model.load("model.pt")

z = model.sample(batch=10)

z = model.sample(batch=10)
print(z[-1].min().item(), z[-1].max().item(), flush=True)
z = z[torch.linspace(0, z.shape[0] - 1, 10).int()]
z = rearrange(z, "t b (h w) (c p q) -> c (b h p) (t w q)", h=h // p, p=p, q=q)
save_image((z + 1) / 2, "output.png")
