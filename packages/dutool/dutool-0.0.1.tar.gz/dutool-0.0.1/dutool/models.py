#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime


class Message():
    @staticmethod
    def test():
        print('Hello World')


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
