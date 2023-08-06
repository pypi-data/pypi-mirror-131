# -*- coding:utf8 -*-

import threading
import time
import json
from websocket import create_connection

from fnirsLink.connection import Connection
from fnirsLink.sys_version import SysVersion


# 数据处理
class DataProcessing(threading.Thread):
    _ws = None
    running = False

    def __init__(self):
        super(DataProcessing, self).__init__()
        self.running = True
        try:
            self._ws = create_connection("ws://localhost:9000")
        except Exception as e:
            self._ws = None
            print('服务端未开启!')

    def run(self):
        if self._ws is None:
            return
        print('开始数据处理!')
        while self.running:
            result = self._ws.recv()  ##接收消息
            if result is not None:
                # result = result.encode('utf-8')
                print(result)


def test_read_data():
    """
    测试读取数据
    :return:
    """
    # 开始读取数据
    # 启动数据处理线程
    thread = DataProcessing()
    thread.start()

    # 读取5min的数据
    time.sleep(5 * 60)
    thread.running = False
    # 结束测试
    data = con.stop();
    print(data);


def test_research_mark():
    """
    测试科研外部触发
    :return:
    """
    # 触发近红外设备开始采集数据（参数1表示触发开始，参数具体含义可参考eprime触发文档）
    con.research_mark(1, "")
    # 触发开始后做任务（此处用sleep代替实际任务）
    time.sleep(5)
    # 任务中间进行打标（参数0表示打标，后面的"5"表示要打标的标记名称）
    con.research_mark(0, "5")
    # 打标后继续任务
    time.sleep(5)
    # 任务完成后结束采集（参数4表示结束采集）
    con.research_mark(4, "")


def test_clinical_mark():
    """
    测试临床外部触发
    :return:
    """
    # 触发近红外设备开始采集数据（参数1表示触发开始，参数具体含义可参考eprime触发文档）
    # 4个参数分别表示 1、任务名称   2、静息时间  3、任务时间  4、休息时间
    con.clinical_mark_start("test name", 5, 5, 5)
    # 触发开始后做任务（此处用sleep代替实际任务）
    time.sleep(15)
    # 任务完成后结束采集
    con.clinical_mark_end()


if __name__ == '__main__':
    con = Connection()

    start = time.time()
    # 建立连接
    data = con.start();
    # 打印连接返回信息
    if SysVersion.PY3:
        print(data)
    else:
        print(json.dumps(data, encoding="UTF-8", ensure_ascii=False))
    # 判断是否连接成功
    if data['success'] is True:
        end = time.time()
        # print(end - start) #打印平均响应时间
        test_type = 1
        # 测试读取数据
        if test_type == 1:
            test_read_data()
        # 测试科研打标
        elif test_type == 2:
            test_research_mark()
        # 测试临床打标
        elif test_type == 3:
            test_clinical_mark()
