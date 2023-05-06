import re
import argparse
import os
import sys
import docx2txt
import pandas as pd
import ipaddress

print(" __  __                             _____      _   ")
print("|  \/  |                           / ____|    | |  ")
print("| \  / | ___  _ ____   _____ _ __ | |     __ _| |_ ")
print("| |\/| |/ _ \| '__\ \ / / _ \ '_ \| |    / _` | __|")
print("| |  | | (_) | |   \ V /  __/ | | | |___| (_| | |_ ")
print("|_|  |_|\___/|_|    \_/ \___|_| |_|\_____\__,_|\__|")

def extract_text(file_path):
    _, extension = os.path.splitext(file_path)
    if extension == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    elif extension == ".docx":
        text = docx2txt.process(file_path)
    elif extension == ".xlsx":
        df = pd.read_excel(file_path, engine="openpyxl")
        text = df.to_string(index=False)
    else:
        sys.exit("不支持这种格式捏~")
    return text


def extract_ip_and_domain(text, extract_ip=True, extract_domain=True):
    if extract_ip:
        ip_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
        ips = ip_pattern.findall(text)
    else:
        ips = []

    if extract_domain:
        domain_pattern = re.compile(r"(?:https?://)?([a-zA-Z\-]+(?:\.[a-zA-Z\-]+)+)(?::\d+)?(?:/|$)")
        domains = domain_pattern.findall(text)
    else:
        domains = []

    filtered_ips = set()
    for ip in ips:
        try:
            if not ipaddress.ip_address(ip).is_private:
                filtered_ips.add(ip)
        except ValueError:
            pass

    filtered_domains = set(domains)

    return filtered_ips, filtered_domains


def main():
    parser = argparse.ArgumentParser(description="从指定文件中提取IP和域名")
    parser.add_argument("-t", "--target", type=str, required=True, help="指定目标文件")
    parser.add_argument("-o", "--output", type=str, default="result.txt", help="指定输出文件，默认输出为result.txt")
    parser.add_argument("-ip", action="store_true", help="仅提取IP地址")
    parser.add_argument("-d", "--domain", action="store_true", help="仅提取域名")
    args = parser.parse_args()

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
