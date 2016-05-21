# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

import os
import glob
import time
import sys
from lib.core.data import conf, paths, th, logger
from lib.core.enums import CUSTOM_LOGGING
from lib.utils.update import update


def checkArgs(args):
    module = args.m
    f = args.f
    i = args.i
    n = args.n
    target = args.TARGET
    show = args.show
    T = args.T
    C = args.C
    update = args.update

    if update:
        return

    if show:
        module_name_list = glob.glob(r'./module/*.py')
        infoMsg = 'Module Name (total:%s)\n' % str(len(module_name_list) - 1)
        for each in module_name_list:
            _str = os.path.splitext(os.path.split(each)[1])[0]
            if _str not in ['__init__']:
                infoMsg += '  %s\n' % _str
        sys.exit(logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg))

    if not module:
        msg = 'Use -m to select a module name. Example: -m spider'
        sys.exit(logger.log(CUSTOM_LOGGING.ERROR, msg))

    if (not T and not C) or (T and C):
        msg = 'Use -T to set Multi-Threaded mode or -C to set Coroutine mode.'
        sys.exit(logger.log(CUSTOM_LOGGING.ERROR, msg))

    if module and not os.path.isfile("./module/" + module + ".py"):
        msg = 'module not exist. Use --show to view all available module names.'
        sys.exit(logger.log(CUSTOM_LOGGING.ERROR, msg))

    # TODO 待优化
    target_mode_flag = 0
    if target:
        target_mode_flag += 1
    if f:
        target_mode_flag += 2
    if i:
        target_mode_flag += 4
    if n:
        target_mode_flag += 8
    if target_mode_flag not in (1, 2, 4, 8):
        msg = 'To load targets, please choose one from [TARGET|-i|-f|-n].'
        sys.exit(logger.log(CUSTOM_LOGGING.ERROR, msg))

    if f and not os.path.isfile(f):
        msg = 'TargetFile not found: %s' % f
        sys.exit(logger.log(CUSTOM_LOGGING.ERROR, msg))

    if i:
        help_str = "invalid input in [-i], Example: python POC-T -m test -i 1-100."
        try:
            _int = i.strip().split('-')
            if int(_int[0]) < int(_int[1]):
                if int(_int[1]) - int(_int[0]) > 1000000:
                    warnMsg = 'Loading %d Payloads...\nMaybe its too much, continue? [y/N]' % (
                        int(_int[1]) - int(_int[0]))
                    logger.log(CUSTOM_LOGGING.WARNING, warnMsg)
                    a = raw_input()
                    if a in ('Y', 'y', 'yes'):
                        pass
                    else:
                        msg = 'User quit!'
                        sys.exit(logger.log(CUSTOM_LOGGING.ERROR, msg))
            else:
                sys.exit(logger.log(CUSTOM_LOGGING.ERROR, help_str))
        except Exception, e:
            sys.exit(logger.log(CUSTOM_LOGGING.ERROR, help_str))
    # TODO 添加规则以增加稳定性
    if n:
        pass
    if target:
        pass

    if not args.nF and args.o:
        msg = 'You cannot use [--nF] and [-o] together, please read the usage with [-h].'
        sys.exit(logger.log(CUSTOM_LOGGING.ERROR, msg))

    if not args.nF and args.browser:
        msg = '[--browser] is based on file output, please remove [--nF] in your command and try again.'
        sys.exit(logger.log(CUSTOM_LOGGING.ERROR, msg))


def setArgs(args):
    conf.MODULE_NAME = args.m
    conf.MODULE_FILE_PATH = os.path.join(paths.MODULES_PATH, conf.MODULE_NAME + ".py")
    conf.THREADS_NUM = args.t
    conf.SCREEN_OUTPUT = args.nS
    conf.FILE_OUTPUT = args.nF
    conf.SINGLE_MODE = args.single
    conf.DEBUG = args.debug
    conf.NETWORK_STR = args.n
    conf.SINGLE_TARGET_STR = args.TARGET
    conf.OPEN_BROWSER = args.browser

    # TODO
    th.THREADS_NUM = conf.THREADS_NUM

    if args.update:
        conf.UPDATE = args.update
        update()

    if args.T:
        conf.ENGINE = 't'
    elif args.C:
        conf.ENGINE = 'c'

    if args.f:
        conf.MODULE_MODE = 'f'
        conf.INPUT_FILE_PATH = args.f
    elif args.i:
        conf.MODULE_MODE = 'i'
        conf.I_NUM2 = args.i
        conf.INPUT_FILE_PATH = None
    elif args.n:
        conf.MODULE_MODE = 'n'
        conf.INPUT_FILE_PATH = None
    elif args.TARGET:
        conf.MODULE_MODE = 'target'
        th.THREADS_NUM = conf.THREADS_NUM = 1
        conf.INPUT_FILE_PATH = None

    conf.OUTPUT_FILE_PATH = os.path.abspath(args.o) if args.o else \
        os.path.abspath(
            os.path.join(
                paths.OUTPUT_PATH, time.strftime(
                    '[%Y%m%d-%H%M%S]', time.localtime(
                        time.time())) + conf.MODULE_NAME + '.txt'))

    conf.SCREEN_OUTPUT = args.nS
    conf.FILE_OUTPUT = args.nF
