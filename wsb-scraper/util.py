import os
import shutil
import csv

def fetch_symbols():
    os.mkdir("temp")
    os.system("curl --ftp-ssl anonymous:jupi@jupi.com "
            "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt "
            "> ./temp/nasdaq.lst")
    os.system("curl --ftp-ssl anonymous:jupi@jupi.com "
            "ftp://ftp.nasdaqtrader.com/SymbolDirectory/otherlisted.txt "
            "> ./temp/otherslisted.lst")
    os.system("tail -n +43 ./temp/nasdaq.lst | cat | sed '$d' | sed 's/|/ /g' > "
            "./temp/nasdaq.lst2")
    os.system("tail -n +43 ./temp/otherslisted.lst | cat | sed '$d' | sed 's/|/ /g' > "
            "./temp/otherslisted.lst2")
    # os.system("awk '{print $1}' ./temp/nasdaq.lst2 > nasdaq.csv")
    # os.system("awk '{print $1}' ./temp/otherslisted.lst2 > otherslisted.csv")
    os.system("awk '{print $1}' ./temp/otherslisted.lst2 ./temp/nasdaq.lst2 > symbols.txt")
    shutil.rmtree("temp")

# Not Used
def csv2dict():
    with open('symbols.txt','r') as c:
        lines = c.readlines()
    stocks = []
    for line in lines:
        line = line.strip('\n')
        data = line
        stocks.append(data)
    # if "Z" in stocks:
    #     print("HELLO THERE")
    return stocks
