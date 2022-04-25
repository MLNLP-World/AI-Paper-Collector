from unicodedata import category
import warnings
from crawler import do_crawl
from searcher import build_index
warnings.filterwarnings("ignore")

open_flag = """
  ___  _____ _____                     _               
 / _ \|_   _/  ___|                   | |              
/ /_\ \ | | \ `--.  ___  __ _ _ __ ___| |__   ___ _ __ 
|  _  | | |  `--. \/ _ \/ _` | '__/ __| '_ \ / _ \ '__|
| | | |_| |_/\__/ /  __/ (_| | | | (__| | | |  __/ |   
\_| |_/\___/\____/ \___|\__,_|_|  \___|_| |_|\___|_|  

AI-Paper-Collector V0.1
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


def init(force=False):
    # force=True: force to update the cache file incrementally
    print(open_flag)
    print(tip_flag)
    print("[+] Initializing System...")
    cache_file = 'cache/cache.json'
    res = do_crawl(cache_file, force)
    indexes, candidates = build_index(res)
    return indexes, candidates

