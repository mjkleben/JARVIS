import os


def main(str):
    sa = os.system("curl -d" + " text={} ".format(str) +
                   "http://text-processing.com/api/sentiment/")
    print (sa)
