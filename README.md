<p align="center">
<h1 align="center"> <img src="./pics/icon/ai.png" width="30" /> AI-Paper-Collector</h1>
</p>
<p align="center">
  	<a href="https://img.shields.io/badge/version-v0.1.0-blue">
      <img alt="version" src="https://img.shields.io/badge/version-v0.1.0-blue?color=FF8000?color=009922" />
    </a>
  <a >
       <img alt="Status-building" src="https://img.shields.io/badge/Status-building-blue" />
  	</a>
  <a >
       <img alt="PRs-Welcome" src="https://img.shields.io/badge/PRs-Welcome-red" />
  	</a>
   	<a href="https://github.com/MLNLP-World/AI-Paper-collector/stargazers">
       <img alt="stars" src="https://img.shields.io/github/stars/MLNLP-World/AI-Paper-collector" />
  	</a>
  	<a href="https://github.com/MLNLP-World/AI-Paper-collector/network/members">
       <img alt="FORK" src="https://img.shields.io/github/forks/MLNLP-World/AI-Paper-collector?color=FF8000" />
  	</a>
    <a href="https://github.com/MLNLP-World/AI-Paper-collector/issues">
      <img alt="Issues" src="https://img.shields.io/github/issues/MLNLP-World/AI-Paper-collector?color=0088ff"/>
    </a>
    <br />
</p>

## <img src="./pics/icon/motivation.png" width="25" />Motivation

Fully-automated scripts for collecting AI-related papers.
Support fuzzy and exact search for paper titles.

```
  ___  _____ _____                     _               
 / _ \|_   _/  ___|                   | |              
/ /_\ \ | | \ `--.  ___  __ _ _ __ ___| |__   ___ _ __ 
|  _  | | |  `--. \/ _ \/ _` | '__/ __| '_ \ / _ \ '__|
| | | |_| |_/\__/ /  __/ (_| | | | (__| | | |  __/ |   
\_| |_/\___/\____/ \___|\__,_|_|  \___|_| |_|\___|_|  

AI-Search-Engine V0.1

Tips:
- enter "q" into any input to exit the program.
- enter "#" into any input to clear the screen.
- enter "help" into any input to see the help.
- enter nothing means search with default mode: exact.
```
## <img src="./pics/icon/intro.png" width="25" />Search Categories
``` 
- [ACL 2019-2021] [EMNLP 2019-2021] [NAACL 2019-2021] [COLING 2020]
- [CVPR 2019-2021] [ECCV 2020] [ICCV2019] [ACMMM 2019-2021]
- [ICLR 2019-2021] [ICML 2019-2021] [AAAI 2019-2021] [IJCAI 2019-2021]
- [SIGIR 2019-2021] [KDD 2019-2021] [CIKM 2019-2021] [WSDM 2019-2022]
- [WWW 2019-2021] [ECIR 2019-2022]
```
## <img src="https://cdn.jsdelivr.net/gh/LightChen233/blog-img/resource.png" width="25" /> Installation
```shell
pip install python-Levenshtein thefuzz beautifulsoup4 requests tqdm
```

## <img src="https://cdn.jsdelivr.net/gh/LightChen233/blog-img/catalogue.png" width="27" /> Usage(v0.1.0)
```shell
python main.py
```

## <img src="./pics/icon/notes.png" width="25" />Help information
```
Search Commands:
- --mode <mode: fuzzy|exact> [optional: --threshold <num>] [optional: --conf <string/list(string)>]
- e.g. "--mode fuzzy --threshold 50" means fuzzy search with similarity >= 50 with all papers
- e.g. "--mode exact --conf ACL" means exact search with all papers in ACL
- e.g. "--mode exact --conf ACL,CVPR" means exact search with all papers in ACL and CVPR
- Note that the threshold is only for fuzzy search from 0 to 100 (default: 50)
- Note that the list of confs should be separated by comma (e.g. "ACL,CVPR")
```
## <img src="./pics/icon/folders.png" width="25" />Example

Only 3 steps shown as follows.

1. keyword query
2. options (search mode and conference source)
3. output path (enter save filename)

```
[+] Initializing System...
[+] Loading from cache...
[+] Enter 'help' into any input for more information when first starting.
[+] Enter your query: few-shot 
[+] Enter Search Commands: --mode fuzzy --conf SIGIR,WSDM,CIKM
[+] Search Results:
[=] Only show Top-5, Please Save results to see all.
[1] [CIKM2021] REFORM: Error-Aware Few-Shot Knowledge Graph Completion.
[2] [CIKM2021] Boosting Few-shot Abstractive Summarization with Auxiliary Tasks.
[3] [CIKM2021] Multi-objective Few-shot Learning for Fair Classification.
[4] [CIKM2020] Graph Few-shot Learning with Attribute Matching.
[5] [CIKM2020] Few-shot Insider Threat Detection.
[+] Enter Save filename: 
[+] Writing results to output/results.txt
[+] Writing results Done!
```

## <img src="https://cdn.jsdelivr.net/gh/LightChen233/blog-img/folders.png" width="25" /> How to add new conferences from DBLP
* clean the cache
```shell
rm -rf cache/cache.json
```
* add new conferences by modifying the `conf/dblp_conf.json` file
```python
[
    # add the name and dblp_url of the new conf
    {
        "name": "WWW2021",
        "url": "https://dblp.org/db/conf/www/www2021.html"
    },
    ... 
]
```
* run the script
```shell
python main.py
```

## <img src="./pics/icon/organizer.png" width="25" />Organizers
<a href="https://github.com/Doragd"> <img src="pics/profile/Gordon.png"  width="80" >  </a> 

## <img src="./pics/icon/heart.png" width="25" />Contributors
Thanks to the contributors:
<a href="https://github.com/Doragd"> <img src="pics/profile/Gordon.png"  width="80" >  </a> 
<a href="https://github.com/yhshu">  <img src="pics/profile/yiheng.png"  width="80" /></a> 