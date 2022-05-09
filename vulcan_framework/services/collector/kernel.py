# -*- coding: utf-8 -*-
# Time       : 2022/5/4 2:23
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description:
import re
from typing import Dict, List

from bs4 import BeautifulSoup
from lxml import etree
from requests.exceptions import RequestException

from services.collector.exceptions import PathMenuError
from services.settings import logger
from services.utils import SteelTorrent, ToolBox


class CollectorKernel(SteelTorrent):
    def __init__(self, action_name: str, docker=None):
        super(CollectorKernel, self).__init__(docker=docker)
        self.action_name = action_name

    def patch_menu(self, page_url, name):
        try:
            return ToolBox.handle_html(page_url)
        except (RequestException, ValueError) as err:
            logger.error(
                ToolBox.runtime_report(
                    motive="SKIP",
                    action_name=self.action_name,
                    message="Site parse error.",
                    name=name,
                    page_url=page_url,
                    err=err,
                )
            )
            raise PathMenuError from err

    def perform(self, job):
        """并行接口"""


# =========================================
# Synergy Leaves samples
# =========================================
class FactoryACL(CollectorKernel):
    def __init__(self):
        super().__init__("ACLAnthology")

    def patch_menu(self, page_url, name, *args, **kwargs):
        # filter: patch
        regex_str = kwargs.get("tag", "")

        titles = []
        response = super().patch_menu(page_url, name)
        soup = BeautifulSoup(response.text, "html.parser")
        for cls in soup.find_all("strong"):
            for paper_item in cls.find_all(href=re.compile(regex_str), class_="align-middle"):
                items = [item.string if item.string else item for item in paper_item.contents]
                title = "".join([item for item in items if isinstance(item, str)])
                titles.append(title)
        self.done_jobs.put_nowait({name: titles})


class FactoryDBLP(CollectorKernel):
    def __init__(self):
        super().__init__("DBLP")

    def patch_menu(self, page_url, name):
        tree = etree.HTML(super().patch_menu(page_url, name).content)
        titles = tree.xpath("//span[@class='title']/text()")
        self.done_jobs.put_nowait({name: titles})


class FactoryICLR(CollectorKernel):
    def __init__(self):
        super().__init__("ICLR")

    def patch_menu(self, page_url, name):
        """:except JSONDecodeError"""
        data = super().patch_menu(page_url, name).json()
        titles = [item["content"]["title"] for item in data["notes"]]
        self.done_jobs.put_nowait({name: titles})


class FactoryNIPS(CollectorKernel):
    def __init__(self):
        super().__init__("NIPS")

    def patch_menu(self, page_url, name):
        tree = etree.HTML(super().patch_menu(page_url, name).content)
        titles = tree.xpath("//div[@class='col']//ul//a/text()")
        self.done_jobs.put_nowait({name: titles})


# =========================================
# Paper samples
# =========================================
class PaperACL(FactoryACL):
    title: str
    authors: List[str]
    abstract: str
    doi: str
    resources: Dict[str, str] = {"pdf": "", "bib": "", "origin": "", "github": ""}

    ...
