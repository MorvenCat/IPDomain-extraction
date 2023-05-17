# IPDomain-extraction
可以从指定文档中提取IP和域名，专治杂乱无章的资产表

支持多种文本格式，自动对不规范的中英文符号进行转换以及对结果进行去重

自动读取当前路径下的 `blacklist.txt` 文件作为过滤项

默认结果保存在result.txt中



## 用法

python ipandomain.py -h										 帮助

python ipandomain.py -t data.txt						   从data.txt中提取数据

python ipandomain.py -t data.txt -o result.txt     指定输出结果保存位置

python ipandomain.py -t data.txt -ip/-d				指定仅提取IP或域名



