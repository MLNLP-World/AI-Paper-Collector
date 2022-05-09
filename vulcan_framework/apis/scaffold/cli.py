# -*- coding: utf-8 -*-
# Time       : 2022/5/4 2:34
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description:
from typing import Optional

from services.settings import logger


@logger.catch()
def query(
    content: str,
    mode: Optional[str] = "exact",
    threshold: Optional[int] = 50,
    limit: Optional[int] = None,
    conf: Optional[str] = None,
    output: Optional[str] = None,
    force: Optional[bool] = False,
):
    # except: ModuleNotFoundError
    from constant import init
    from searcher import exec_search
    from utils import show_res, output_res

    indexes, candidates = init(force)
    results = exec_search(indexes, candidates, content, mode, threshold, conf, limit)

    if not results:
        logger.error("[-] No results found.")
    else:
        show_res(results)
        output_res(results, output)


@logger.catch()
def update():
    """主动更新 cache"""
