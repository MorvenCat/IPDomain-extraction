import re
import argparse
import os
import sys
import docx2txt
import pandas as pd

print(" __  __                             _____      _   ")
print("|  \/  |                           / ____|    | |  ")
print("| \  / | ___  _ ____   _____ _ __ | |     __ _| |_ ")
print("| |\/| |/ _ \| '__\ \ / / _ \ '_ \| |    / _` | __|")
print("| |  | | (_) | |   \ V /  __/ | | | |___| (_| | |_ ")
print("|_|  |_|\___/|_|    \_/ \___|_| |_|\_____\__,_|\__|")
print("Link:https://github.com/MorvenCat/IPDomain-extraction")


# 读取文件中的文本
def extract_text(file_path):
    _, extension = os.path.splitext(file_path)
    if extension == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    elif extension == ".docx" or extension == ".doc":
        text = docx2txt.process(file_path)
    elif extension == ".xlsx" or extension == ".xls":
        df = pd.read_excel(file_path, engine="openpyxl")
        text = df.to_string(index=False)
    elif extension == ".csv":
        df = pd.read_csv(file_path)
        text = df.to_string(index=False)
    else:
        sys.exit("不支持这种格式捏~")

    text = text.replace('。', '.')
    return text


# 从文本中提取IP和域名
def extract_ip_and_domain(text, extract_ip=True, extract_domain=True):
    if extract_ip:
        ip_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
        ips = ip_pattern.findall(text)
    else:
        ips = []

    if extract_domain:
        domain_pattern = re.compile(
            r"(?:https?://)?([a-zA-Z0-9\-]+(?:\.[a-zA-Z0-9\-]+)*\.[a-zA-Z]+)(?::\d+)?(?:[^a-zA-Z\.]|$)")
        domains = domain_pattern.findall(text)
    else:
        domains = []

    blacklist_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "blacklist.txt")
    if os.path.exists(blacklist_path):
        with open(blacklist_path, "r", encoding="utf-8") as f:
            blacklist = f.read()
        if blacklist:
            print("已加载过滤名单")
            blacklist = blacklist.split("\n")
            filtered_ips = [ip for ip in ips if not any(exclusion in ip for exclusion in blacklist)]
            filtered_domains = [domain for domain in domains if
                                not any(exclusion in domain for exclusion in blacklist)]
        else:
            print("blacklist.txt为空，那就全部打印吧~")
            filtered_ips = ips
            filtered_domains = domains
    else:
        print("没有找到blacklist.txt，那就全部打印吧~")
        filtered_ips = ips
        filtered_domains = domains

    # 过滤掉重复IP和域名
    filtered_ips = list(set(filtered_ips))
    filtered_domains = list(set(filtered_domains))

    return filtered_ips, filtered_domains


# 主函数
def main():
    parser = argparse.ArgumentParser(description="从指定文件中提取IP和域名")
    parser.add_argument("-t", "--target", type=str, required=True, help="指定目标文件")
    parser.add_argument("-o", "--output", type=str, default="result.txt", help="指定输出文件，默认输出为result.txt")
    parser.add_argument("-ip", action="store_true", help="仅提取IP地址")
    parser.add_argument("-d", "--domain", action="store_true", help="仅提取域名")
    args = parser.parse_args()

    if not os.path.exists(args.target):
        sys.exit(f"没有找到{args.target}哦，看看是不是自己搞错了~")

    text = extract_text(args.target)
    ips, domains = extract_ip_and_domain(text, extract_ip=not args.domain, extract_domain=not args.ip)

    with open(args.output, "w") as f:
        if not ips and not domains:
            print("什么都没找到/(ㄒoㄒ)/~~")
            f.write("什么都没找到/(ㄒoㄒ)/~~")
            return
        if ips:
            f.write("IP addresses:\n")
            for ip in ips:
                f.write(ip + "\n")
            if domains:
                f.write("\n")
        if domains:
            f.write("Domains:\n")
            for domain in domains:
                f.write(domain + "\n")
        print(f"提取结果保存到{args.output}了喵~")


if __name__ == "__main__":
    main()
