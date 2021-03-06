# -*- coding:utf-8 -*-
from src.client import AutoAgent
from src.client import AutoSSH
from src.client import AutoSalt
from conf import settings
import os

def client():
    if settings.MODE == 'agent':
        cli = AutoAgent(url=settings.API_URL)
    elif settings.MODE == 'ssh':
        cli = AutoSSH()
    elif settings.MODE == 'salt':
        cli = AutoSalt()
    else:
        raise Exception('请配置资产采集模式，如：ssh、agent、salt')

    cli.process()


def update_client():
    if settings.MODE == 'agent':
        cli = AutoAgent(url=settings.UP_API_URL)
    elif settings.MODE == 'ssh':
        cli = AutoSSH()
    elif settings.MODE == 'salt':
        cli = AutoSalt()
    else:
        raise Exception('请配置资产采集模式，如：ssh、agent、salt')

    ret = cli.process()
    print(ret)
    # os.system('pause')


