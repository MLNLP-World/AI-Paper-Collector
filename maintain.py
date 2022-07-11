import os
import sys
import json
import re
from crawler import crawl

COMMENT_CONFS_LIST_START = "<!-- confs-list-start -->"
COMMENT_CONFS_LIST_END = "<!-- confs-list-end -->"

cache_path = os.path.join(os.path.dirname(__file__), "cache", "cache.json")
readme_path = "README.md"
acl_conf_path = os.path.join(os.path.dirname(__file__), "conf", "acl_conf.json")
dblp_conf_path = os.path.join(os.path.dirname(__file__), "conf", "dblp_conf.json")
nips_conf_path = os.path.join(os.path.dirname(__file__), "conf", "nips_conf.json")
iclr_conf_path = os.path.join(os.path.dirname(__file__), "conf", "iclr_conf.json")
thecvf_conf_path = os.path.join(os.path.dirname(__file__), "conf", "thecvf_conf.json")


def generate_new_readme(src: str, content: str, start_comment: str, end_comment: str) -> str:
    """Generate a new Readme.md"""
    pattern = f"{start_comment}[\\s\\S]+{end_comment}"
    repl = f"{start_comment}\n\n{content}\n\n{end_comment}"
    if re.search(pattern, src) is None:
        print(f"can not find section in src, please check it, it should be {start_comment} and {end_comment}")
    return re.sub(pattern, repl, src)


def get_one_line(confs):
    res = "- "
    for conf in confs:
        _conf = list(conf.keys())[0]
        _year = conf[_conf]
        res += f"[{_conf} {min(_year)}-{max(_year)}] "
    return res


def update_readme():
    readme_path = "README.md"
    with open(readme_path, "r") as f:
        src = f.read()

    confs_list = {}
    for files in [acl_conf_path, dblp_conf_path, nips_conf_path, iclr_conf_path, thecvf_conf_path]:
        with open(files, "r") as f:
            for conf in json.load(f):
                # print(conf)
                year = re.search(r"\d{4}", conf["name"]).group()
                # cut by year
                conf_name = re.sub(r"\d{4}(.*)", "", conf["name"]).strip()

                if conf_name.upper() not in confs_list.keys():
                    confs_list[conf_name.upper()] = set()
                confs_list[conf_name.upper()].add(year)

    # 4 confs for one line
    confs_list_str = "```text\n"
    waiting_list = []
    for conf in confs_list.keys():
        if len(waiting_list) == 4:
            confs_list_str += get_one_line(waiting_list) + "\n"
            waiting_list = []
        waiting_list.append({conf: list(confs_list[conf])})
    if len(waiting_list) != 0:
        confs_list_str += get_one_line(waiting_list) + "\n"
    confs_list_str += "```\n"

    with open(readme_path, "w") as f:
        src = generate_new_readme(src, confs_list_str, COMMENT_CONFS_LIST_START, COMMENT_CONFS_LIST_END)
        f.write(src)


def force_update():
    res = crawl(cache_file=None, force=True)
    with open(cache_path, "w") as f:
        json.dump(res, f)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        update_readme()
    elif len(sys.argv) == 2:
        if sys.argv[1] == "force":
            force_update()
        else:
            print("unknown argument")
