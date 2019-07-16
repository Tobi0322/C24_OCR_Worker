#!/usr/local/bin/python
# coding: utf8
import os


if __name__ == '__main__':
    name = "documents\\2019\\04\\05\\95953\\darlehensvertrag-abbezahlungsbestätigung.pdf"
    folder = "ImageFiles"
    path = os.path.join(folder, name)
    with open(path, 'r+') as my_file:
        print(my_file)