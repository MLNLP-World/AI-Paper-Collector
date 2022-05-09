# -*- coding: utf-8 -*-
# Time       : 2022/1/16 0:27
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description:
import os
import shutil
import sys
import warnings
from datetime import datetime
from datetime import timedelta
from typing import List, Union, Dict, Optional, Any

import pytz
import requests
import yaml
from gevent.queue import Queue
from loguru import logger
from requests import Response

warnings.filterwarnings("ignore", category=FutureWarning)


class ToolBox:
    """可移植的工具箱"""

    logger_tracer = Queue()

    @staticmethod
    def check_sample_yaml(path_output: str, path_sample: str) -> Optional[Dict[str, Any]]:
        """
        检查模板文件是否存在，检查配置文件是否存在，读取系统配置返回

        :param path_output: 配置生成路径（user）
        :param path_sample: 模板文件路径（built-in）
        :return:
        """
        try:
            # 丢失模板文件
            if not os.path.exists(path_sample):
                print("[EXIT] 系统配置模板文件(config-sample.yaml)缺失。")
                raise FileNotFoundError

            # 项目未初始化，自动拷贝模板文件
            if not os.path.exists(path_output):
                print("系统配置文件(config.yaml)缺失")
                shutil.copy(path_sample, path_output)
                print("[EXIT] 生成配置文件，请合理配置并重启项目-->config.yaml")
                sys.exit()

            # 配置正常，读取配置参数
            with open(path_output, "r", encoding="utf8") as stream:
                config_ = yaml.safe_load(stream.read())
                if __name__ == "__main__":
                    print("读取配置文件-->config.yaml")
                    print(config_)

            return config_

        # 需要到项目仓库重新拉取文件
        except FileNotFoundError:
            print(
                "Please do not delete the system built-in `config-sample.yaml` "
                "Make sure it is located in the project root directory"
            )

    @staticmethod
    def runtime_report(action_name: str, motive: str = "RUN", message: str = "", **params) -> str:
        """格式化输出"""
        flag_ = f">> {motive} [{action_name}]"
        if message != "":
            flag_ += f" {message}"
        if params:
            flag_ += " - "
            flag_ += " ".join([f"{i[0]}={i[1]}" for i in params.items()])

        # feat(pending): 将系统级日志按序插入消息队列
        # ToolBox.logger_tracer.put(flag_)

        return flag_

    @staticmethod
    def transfer_cookies(
        api_cookies: Union[List[Dict[str, str]], str]
    ) -> Union[str, List[Dict[str, str]]]:
        """
        将 cookies 转换为可携带的 Request Header
        :param api_cookies: api.get_cookies() or cookie_body
        :return:
        """
        if isinstance(api_cookies, str):
            return [
                {"name": i.split("=")[0], "value": i.split("=")[1]} for i in api_cookies.split("; ")
            ]
        return "; ".join([f"{i['name']}={i['value']}" for i in api_cookies])

    @staticmethod
    def date_format_now(
        mode: Optional[str] = None, zone: Optional[str] = None, threshold: Optional[int] = None
    ) -> str:
        """
        输出格式化日期
        :param threshold:
        :param zone: 时区
        :param mode: with [file log threshold]
            - file：符合文件标准　yyyy-mm-dd
            - log：人类可读 yyyy-mm-dd HH:MM:SS
        :return:
        """
        mode = "log" if mode is None else mode
        zone = "Asia/Shanghai" if zone is None else zone
        threshold = 30 if threshold is None else threshold
        timezone = pytz.timezone(zone)

        format_date: str = ""
        if mode == "file":
            format_date = str(datetime.now(timezone)).split(" ", maxsplit=1)[0]
        elif mode == "log":
            format_date = str(datetime.now(timezone)).split(".", maxsplit=1)[0]
        elif mode == "threshold":
            format_date = str(datetime.now(timezone) + timedelta(seconds=threshold))
        return format_date

    @staticmethod
    def init_log(**sink_path):
        """初始化 loguru 日志信息"""
        event_logger_format = (
            "<g>{time:YYYY-MM-DD HH:mm:ss}</g> | "
            "<lvl>{level}</lvl> - "
            # "<c><u>{name}</u></c> | "
            "{message}"
        )
        logger.remove()
        logger.add(
            sink=sys.stdout,
            colorize=True,
            level="DEBUG",
            format=event_logger_format,
            diagnose=False,
        )
        if sink_path.get("error"):
            logger.add(
                sink=sink_path.get("error"),
                level="ERROR",
                rotation="1 week",
                encoding="utf8",
                diagnose=False,
            )
        if sink_path.get("runtime"):
            logger.add(
                sink=sink_path.get("runtime"),
                level="DEBUG",
                rotation="20 MB",
                retention="20 days",
                encoding="utf8",
                diagnose=False,
            )
        return logger

    @staticmethod
    def handle_html(url) -> Optional[Response]:
        headers = {"user-agent": "IM NOT ROBOT."}

        response = requests.get(url, headers=headers, allow_redirects=False)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response
