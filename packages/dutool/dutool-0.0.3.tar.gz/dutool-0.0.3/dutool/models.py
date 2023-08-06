#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import sys
import os
import you_get
import re
from ffmpy import FFmpeg


class FileUtil:
    @staticmethod
    def get_file_curlist(path):
        file_list = []
        for i in os.listdir(path):
            file_path = os.path.join(path, i)
            if os.path.isfile(file_path):
                file_list.append(file_path)
        return file_list

    @staticmethod
    def get_file_alllist(path):
        file_list = []
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                file_list.append((os.path.join(dirpath, filename)))
        return file_list


class DateUtil:
    @staticmethod
    def date_range(start_date, end_date):
        start = datetime.date(int(start_date[0:4]), int(start_date[4:6]), int(start_date[6:8]))
        end = datetime.date(int(end_date[0:4]), int(end_date[4:6]), int(end_date[6:8]))
        date_list = []
        for i in range((end-start).days+1):
            cur_date = start+datetime.timedelta(days=i)
            cur_date = cur_date.strftime("%Y%m%d")
            date_list.append(cur_date)
        return date_list


class BilibiliAudio:
    def download(self, url):
        """
        下载bilibili视频（MP4）
        """
        sys.argv = ["you-get", "--format", "dash-flv360", "-o", os.getcwd(), "-O", "temp", url]
        you_get.main()

    def transform(self):
        """
        生成bilibili音频（MP3）
        """
        inputpath = os.path.join(os.getcwd(), "temp.mp4")
        outputpath = os.path.join(os.getcwd(), "temp.mp3")
        ff = FFmpeg(inputs={inputpath: None}, outputs={outputpath: None})
        ff.cmd
        ff.run()

    def rename(self):
        """
        重命名bilibili音频
        """
        for filename in os.listdir(os.getcwd()):
            if filename.endswith(".xml"):
                res = filename
                res = res.replace(".cmt.xml", "")
                res = re.sub(u'[^\\u4e00-\\u9fff0-9a-zA-Z]+', ' ', res)
                res = "{}.mp3".format(res)
                break
        inputpath = os.path.join(os.getcwd(), "temp.mp3")
        outputpath = os.path.join(os.getcwd(), res)
        os.rename(inputpath, outputpath)

    def clean(self):
        """
        清理临时文件
        """
        for filename in os.listdir(os.getcwd()):
            if filename in ("temp.mp3", "temp.mp4"):
                os.remove(os.path.join(os.getcwd(), filename))
            if filename.endswith(".cmt.xml"):
                os.remove(os.path.join(os.getcwd(), filename))

    def __init__(self, url):
        """
        主程序
        """
        self.clean()
        self.download(url)
        self.transform()
        self.rename()
        self.clean()
