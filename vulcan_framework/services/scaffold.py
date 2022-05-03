# -*- coding: utf-8 -*-
# Time       : 2022/4/30 14:58
# Description: 应用接口层
from typing import Optional

from apis.scaffold import cli
from services.settings import __version__

open_flag = f"""
  ___  _____ _____                     _               
 / _ \|_   _/  ___|                   | |              
/ /_\ \ | | \ `--.  ___  __ _ _ __ ___| |__   ___ _ __ 
|  _  | | |  `--. \/ _ \/ _` | '__/ __| '_ \ / _ \ '__|
| | | |_| |_/\__/ /  __/ (_| | | | (__| | | |  __/ |   
\_| |_/\___/\____/ \___|\__,_|_|  \___|_| |_|\___|_|  

{__version__}
"""

tip_flag = """
Tips:
- enter "q" into any input to exit the program.
- enter "#" into any input to clear the screen.
- enter "h" into any input to see the help information.
- enter nothing means search with default settings.

"""

category_flag = """

Search Categories: 
- [ACL 2019-2021] [EMNLP 2019-2021] [NAACL 2019-2021] [COLING 2020]
- [CVPR 2019-2021] [ECCV 2020] [ICCV2019] [ACMMM 2019-2021]
- [ICLR 2019-2021] [ICML 2019-2021] [AAAI 2019-2021] [IJCAI 2019-2021]
- [SIGIR 2019-2021] [KDD 2019-2021] [CIKM 2019-2021] [WSDM 2019-2022]
- [WWW 2019-2021] [ECIR 2019-2022]

"""


class AIPaperCollector:
    def __init__(self, query=None, **kwargs):

        # 向下兼容 `--query` 语法
        if query:
            self.query(content=query, **kwargs)

    @staticmethod
    def query(
            content: str,
            mode: Optional[str] = "exact",
            threshold: Optional[int] = 50,
            limit: Optional[int] = None,
            conf: Optional[str] = None,
            output: Optional[str] = None,
            force: Optional[bool] = False,
            **kwargs,
    ):
        """
        Query to search for.

        Usage: python main.py query [key]
            - python main.py query NLP --mode=fuzzy
            - python main.py query NLP --mode=exact

        Advanced:

        Warning:

        :param content:
        :param mode: default `exact`. search mode.
        :param threshold: default 50. fuzzy search threshold.
        :param limit: default None. fuzzy search limit.
        :param conf: default None. conferences to search.
        :param output: default None. output file.
        :param force: default False. force to update the cache file incrementally
        :param kwargs:
        :return:
        """
        # =======================================================
        # Passing on alias
        # =======================================================
        mode = kwargs.get("m", mode)
        threshold = kwargs.get("t", threshold)
        limit = kwargs.get("l", limit)
        conf = kwargs.get("c", conf)
        output = kwargs.get("o", output)
        force = kwargs.get("f", force)

        # =======================================================
        # Cleaning
        # =======================================================
        if mode not in ["fuzzy", "exact"]:
            raise ValueError

        if conf:
            conf = conf.split(",")

        if output is None:
            conf_seq = "_".join(conf) if conf else None
            output = f"{mode}_{threshold}_{conf_seq}_{content}.text"

        # =======================================================
        # Business code
        # =======================================================
        return cli.query(
            content=content,
            mode=mode,
            threshold=threshold,
            limit=limit,
            conf=conf,
            output=output,
            force=force,
        )

    @staticmethod
    def runner():
        """集成 self-main <交互接口> 以及 <server localhost>"""

    @staticmethod
    def update():
        """主动更新 cache"""

    @staticmethod
    def test():
        print(open_flag)
        print(tip_flag)
