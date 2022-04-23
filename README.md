# AI-Paper-collector :memo:
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
## Search Categories
``` 
- [ACL 2019-2021] [EMNLP 2019-2021] [NAACL 2019-2021] [COLING 2020]
- [CVPR 2019-2021] [ECCV 2020] [ICCV2019] [ACMMM 2019-2021]
- [ICLR 2019-2021] [ICML 2019-2021] [AAAI 2019-2021] [IJCAI 2019-2021]
- [SIGIR 2019-2021] [KDD 2019-2021] [CIKM 2019-2021] [WSDM 2019-2022]
- [WWW 2019-2021] [ECIR 2019-2022]
```
## Requirements
```shell
pip install python-Levenshtein thefuzz beautifulsoup4 requests tqdm
```
## Usage
```shell
python main.py
```
## Help information
```
Search Commands:
- --mode <mode: fuzzy|exact> [optional: --threshold <num>] [optional: --conf <string/list(string)>]
- e.g. "--mode fuzzy --threshold 50" means fuzzy search with similarity >= 50 with all papers
- e.g. "--mode exact --conf ACL" means exact search with all papers in ACL
- e.g. "--mode exact --conf ACL,CVPR" means exact search with all papers in ACL and CVPR
- Note that the threshold is only for fuzzy search from 0 to 100 (default: 50)
- Note that the list of confs should be separated by comma (e.g. "ACL,CVPR")
```
## Example
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
