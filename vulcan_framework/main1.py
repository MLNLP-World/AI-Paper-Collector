# -*- coding: utf-8 -*-
# Time       : 2022/5/4 1:19
# Author     : MLNLP-World
# Github     : https://github.com/MLNLP-World
# Description: 🥂 Welcome to use AI-Paper-Collector!
from fire import Fire

from services.scaffold import AIPaperCollector

if __name__ == "__main__":
    Fire(AIPaperCollector)
