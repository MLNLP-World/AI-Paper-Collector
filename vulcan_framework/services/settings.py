import os
from os.path import join, dirname

from services.utils import ToolBox

__all__ = [
    # ------------------------------
    # SETTINGS
    # ------------------------------
    "logger",
    "DIR_COOKIES",
    "DIR_TEMP_CACHE",
    "DIR_QUERY_LOG",
    "DIR_MODEL",
    "__version__"
    # ------------------------------
    # CONFIG
    # ------------------------------
]
__version__ = "AI-Paper-Collector V0.1"

"""
================================================ ʕ•ﻌ•ʔ ================================================
                                            (·▽·)欢迎宝友入座
================================================ ʕ•ﻌ•ʔ ================================================
[√]核心配置 [※]边缘参数
"""
# ---------------------------------------------------
# [√]工程根目录定位
# ---------------------------------------------------
# 系统根目录
PROJECT_ROOT = dirname(dirname(__file__))
# 文件数据库目录
PROJECT_DATABASE = join(PROJECT_ROOT, "database")
DIR_MODEL = join(PROJECT_ROOT, "model")
# conf 运行配置目录
DIR_CONF = join(PROJECT_ROOT, "conf")
# Cookie 工作目录
DIR_COOKIES = join(PROJECT_DATABASE, "cookies")
# 运行缓存目录
DIR_TEMP_CACHE = join(PROJECT_DATABASE, "temp_cache")
# 查询缓存
DIR_QUERY_LOG = join(DIR_TEMP_CACHE, "query_output")
# 服务日志目录
DIR_LOG = join(PROJECT_DATABASE, "logs")
# ---------------------------------------------------
# [√]服务器日志配置
# ---------------------------------------------------
logger = ToolBox.init_log(error=join(DIR_LOG, "error.log"), runtime=join(DIR_LOG, "runtime.log"))

# ---------------------------------------------------
# 路径补全
# ---------------------------------------------------
for _pending in [PROJECT_DATABASE, DIR_MODEL, DIR_COOKIES, DIR_TEMP_CACHE, DIR_QUERY_LOG, DIR_LOG]:
    if not os.path.exists(_pending):
        os.mkdir(_pending)
"""
================================================== ʕ•ﻌ•ʔ ==================================================
                                  若您并非项目开发者 请勿修改以下变量的默认参数
================================================== ʕ•ﻌ•ʔ ==================================================

                                            Enjoy it -> ♂ main.py
"""
config_ = ToolBox.check_sample_yaml(
    path_output=join(dirname(dirname(__file__)), "config.yaml"),
    path_sample=join(dirname(dirname(__file__)), "config-sample.yaml"),
)
