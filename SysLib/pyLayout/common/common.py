#--- coding=utf-8
#--- @Author: Yongsheng.Guo@ansys.com, Henry.he@ansys.com,Yang.zhao@ansys.com
#--- @Time: 20230410


'''_
common.py模块主要用于存放一些常用的函数接口，比如加载json,csv,txt文件，查找文件等操作

log is a global variable for log module, every module can import this variable to output log information.

'''
from __future__ import print_function

import re
import os
import sys
import csv,json
from copy import deepcopy
from shutil import copy
from functools import wraps
import time
import contextlib  # 引入上下文管理包

#intial log
from .log import Log as logger
log = logger(logLevel = "DEBUG")  #CRITICAL > ERROR > WARNING > INFO > DEBUG,

isIronpython = "IronPython" in sys.version
is_linux = "posix" in os.name

def reSubR(pattern, repl, string, count=0, flags=0):
    return re.sub(pattern, repl, string[::-1],count,flags)[::-1]

def readData(path):
    '''读取文本文件

    Args:
        path (str): 文本文件路径

    Returns:
        list: 返回文件所有行
    '''

    with open(path, 'rb') as file:
        # 读取文件内容，得到字节串
        content = file.read()
        file.close()
        # 将字节串解码为 Unicode 字符串
    try:
        content.decode("utf-8")
        return content
    except:
        return content.decode("ascii")


def readlines(path):
    '''读取文本文件

    Args:
        path (str): 文本文件路径

    Returns:
        list: 返回文件所有行
    '''
#     with open(path,'r') as f:
#         line = "readData" 
#         while(line):
#             line = f.readline()
#             yield line
#         f.close()     
        
    try:
        with open(path, 'r') as file:
            # 读取文件内容，得到字节串
            line = "readData" 
            while(line):
                line = file.readline()
                yield line 
            file.close()


    except:
        print("文件读取错误")

        

def writeData(data,path):
    '''写入文本文件

    Args:
        data (list,str): 文本信息
        path (str): 文件路径，如果存在则被覆盖
    '''
    if isinstance(data, list):
        data = "\n".join(data)
    with open(path,'w+') as f:
        f.write(data)
        f.close()


def readCfgFile(path):
    '''读取简单的配置文件

    Args:
        path (str): 配置文件路径

    Returns:
        dict: 配置文件内容
    '''
    if not os.path.exists(path):
        raise FileNotFoundError("配置文件%s不存在"%path)
    
    config_dict = {}
    for line1 in readlines(path):
        line = line1.strip()
        if not line:
            continue
        if line.startswith("#"):
            continue

        if line.startswith("[") and not config_dict:
            #return ini file
            log.info("read as ini format: %s"%path)
            return readIniFile(path)
        
        key_value = line.split("=",maxsplit=1)
        key_value = re.split("\s*=\s*",line,maxsplit=1)
        if len(key_value) != 2:
            continue
        config_dict[key_value[0]] = key_value[1]
    
    return config_dict

def readIniFile(path):
    """
    read ini format file
    """
    if not os.path.exists(path):
        raise FileNotFoundError("配置文件%s不存在"%path)

    if isIronpython:
        import ConfigParser
        config = ConfigParser.ConfigParser()
        try:
            # 注意：Python 2.7 的 read 方法没有 encoding 参数
            # 如果文件不是 ASCII 编码，需要先解码
            with open(path, 'r') as f:
                content = f.read().decode('utf-8')  # 根据实际编码调整
                config.readfp(content.split('\n'))
        except ConfigParser.Error as e:
            raise ValueError("配置文件格式错误: %s" % e)

    else: #python 3.x
        import configparser
        config = configparser.ConfigParser(
            interpolation=None,  # 禁用字符串插值
            allow_no_value=True, # 允许没有值的键
            delimiters=('='),    # 严格使用等号作为分隔符
            inline_comment_prefixes=('#', ';')  # 支持的注释符号
        )

        try:
            config.read(path, encoding='utf-8')
        except configparser.Error as e:
            raise ValueError("配置文件格式错误: %s" % e)

    # 转换为字典结构
    config_dict = {}
    for section in config.sections():
        config_dict[section] = {}
        for option in config.options(section):
            try:
                # 自动类型转换（可选）
                value = config.get(section, option)
                if value.lower() in ('true', 'false'):
                    value = config.getboolean(section, option)
                elif value.isdigit():
                    value = config.getint(section, option)
                config_dict[section][option] = value
            except ValueError:
                config_dict[section][option] = value  # 保留原始字符串
 
    return config_dict


def loadCSV(csvPath, fmt = 'list'):
    '''读取csv文件

    Args:
        csvPath (str): csv路径
        fmt (str, optional): 返回格式 list or dict. Defaults to 'list'.

    Returns:
        list: fmt = list
        dict: fmt = dict
    '''

    if not os.path.exists(csvPath):
        log.debug("csv not exit: %s"%csvPath)
        return []
    
    with open(csvPath) as f:
        if 'list' in fmt:
            reader  = csv.reader(f)
        elif 'dict' in fmt:         
            reader  = csv.DictReader(f)
        else:
            log.debug("fmt must be list or dict")
            
        datas = list(reader)
        f.close()
    return datas


def writeCSV(csvPath,datas, header = [],fmt = 'list'):
    '''写入CSV文件

    Args:
        csvPath (str): 写入的csv文件路径，覆盖写入
        datas (list，dict): 写入的数据集
        header (list, optional): 写入title行. Defaults to [].
        fmt (str, optional): datas的数据格式 list or dict. Defaults to 'list'.
    '''
    with open(csvPath,'w+') as f:
        if fmt == 'list':
            if header:
                f.write(",".join(header) + "\n")
            lines = (",".join((str(d) for d in data)) for data in list(datas))
            f.write("\n".join(lines))
        else:
            dialect = csv.excel
            dialect.lineterminator = "\n"
            f_csv = csv.DictWriter(f,header,dialect = dialect)
            f_csv.writeheader()
            f_csv.writerows(datas)
        f.close()

def loadJson(jsonPath):
    '''读取json文件

    Args:
        jsonPath (str): json路径

    Returns:
        dict: 返回json代表的dict
    '''
    with open(jsonPath,'r') as load_f:
        config = json.load(load_f)
        load_f.close()
    return config

def writeJson(path,config):
    '''写入json文件

    Args:
        path (str): json路径
        config (dict): 文件内容
    '''
    with open(path,"w+") as f:
        json.dump(config,f,indent=4, separators=(',', ': '))
        f.close()


def tuple2list(tuple_obj):
    if isinstance(tuple_obj, (tuple,list)):
        return [tuple2list(item) for item in tuple_obj]
    else:
        return tuple_obj


def findDictValue(key,dict1,default = None, valid = None,ignorCase = True, maps = None):
    '''查找字典的key对应的value，key不存在时返回默认值

    Args:
        key (str): 查找的key值
        dict1 (dict): 查找的字典
        default (any, optional): key不存在时，返回的值. Defaults to None.
        valid (any, optional): 返回的value无效时（空值,False,null），返回的值. Defaults to None.
        ignorCase (bool, optional): 是否区分key的大小写. Defaults to True.
        maps(dict): key alias maps, {alias1:key1,alias2:key1}

    Returns:
        Any: 返回查找到的Value，key无效时返回default值
    '''
    
    # if kye in dict1
    if ignorCase:
        for k in dict1:
            if k.lower()==key.lower():
                if not dict1[k] and valid != None:
                    return valid
                else:
                    return dict1[k]
    else:
        if k in dict1:
            if not dict1[k] and valid != None:
                return valid
            else:
                return dict1[k]
    #other case, eg key not in dict1   
    val = default if valid == None else valid
    #log.debug("Not found key value:%s , return value %s"%(key,val))
    
    if maps:
        for k,v in maps.items():
            if v.lower() == key.lower():
                log.debug("found key in maps, mapKey: %s:"% k)
                return findDictValue(k,dict1,default,valid,ignorCase)
        
    return val

def findDictKey(key,dict1,ignorCase = True):
    '''
    test a key in given dict, return found key or "//key_not_found//"
    '''
    if ignorCase:
        for k in dict1:
            if k.lower()==key.lower():
                return k
    else:
        if k in dict1:
            return k
    #other case   
#     log.debug("not found key value:%s"%key)
    return "//key_not_found//"

def splitList(list_collection, n):
    """
    将集合均分，每份n个元素
    :param list_collection:
    :param n:
    :return:返回的结果为评分后的每份可迭代对象
    """
    for i in range(0, len(list_collection), n):
        yield list_collection[i: i + n]


def update2Dict(dict1,dict2,ignorCase = True):
    '''
    dict2 update to dict1, considered Multi-level dict keys
    '''
    
    #if dict2 not dict, use dict2 value override dict1
    if not isinstance(dict2, (dict)):
        dict1 = dict2
        return dict1
    
    for key2 in dict2:
        key1 = findDictKey(key2,dict1,ignorCase)
            
        if key1 != "//key_not_found//":
            dict1[key1] = update2Dict(dict1[key1], dict2[key2])
        else:
            dict1[key2] = deepcopy(dict2[key2])
            
    return dict1
    

def getParent(path):
    return os.path.abspath(os.path.join(path, os.pardir))

def getFileList(path,reg = ".*"):
    '''列出给定目录下符合条件的文件路径

    Args:
        path (str): 文件夹路径
        reg (str, optional): 过滤条件. Defaults to ".*".

    Returns:
        list: 返回符合条件的文件路径
    '''
    files = os.listdir(path)
    regFiles = list(filter(lambda x: re.match(reg,x,re.IGNORECASE),files))
    if regFiles:
        return [os.path.join(path,x)  for x in regFiles]
    else:
        []

def findFiles(root,reg = ".*"):
    '''在目录下查找文件，便利子目录

    Args:
        root (str): 根文件路径
        reg (str, optional): 过滤条件. Defaults to ".*".

    Returns:
        list: 返回符合条件的所有文件路径
    '''
    regFiles = []
    for root, dirs, files in os.walk(root):
        regFiles += [os.path.join(root,f) for f in filter(lambda x: re.match(reg, x,re.IGNORECASE),files)]

    return regFiles


def taskForEach(MaxParallel = 4):
    '''
    tasks = taskForEach(5)
    tasks(inputList,func)
    '''
    if isIronpython:
        import clr #System lib need
        from System.Threading.Tasks import Parallel,ParallelOptions 
        taskOptions = ParallelOptions()
        taskOptions.MaxDegreeOfParallelism = MaxParallel
        
        def forEach(inputList,func):
            Parallel.ForEach(inputList,taskOptions,func)
        return forEach
    else:
        import multiprocessing
        # 创建一个进程池，包含MaxParallel个工作进程
        pool = multiprocessing.Pool(processes=MaxParallel)
        def forEach(inputList,func):
            # 使用 map 方法分配任务给进程池
            results = pool.map(func,inputList)
            # 关闭进程池，不再接受新的任务
            pool.close()
            # 等待所有进程完成
            pool.join()
        return forEach
        


def regAnyMatch(regs,val,flags = re.IGNORECASE):
    '''
    regs: str or list
    val: str or list
    '''
    if isinstance(regs, str) and isinstance(val, str):
        return re.match(regs+"$",val,flags)
    
    if not isinstance(regs,str) and isinstance(val, str):
        return any([regAnyMatch(r+"$",val) for r in regs])

    if not isinstance(val, (str,list,tuple)):
        return False

    return any([regAnyMatch(regs,v) for v in val])

def copyAedt(source,target):
    
    #source = (source,source+".aedt")(".aedt" in source)
    if ".aedt" not in source:
        log.debug("source must .aedt file: %s"%source)
        return
    if not os.path.exists(source):
        log.debug("source file not found: %s"%source)
        return
    
    
    aedtTarget = (target+".aedt",target)[".aedt" in target]
    aedtTargetDir = os.path.dirname(aedtTarget)
    if not os.path.exists(aedtTargetDir):
        log.debug("make dir: %s"%aedtTargetDir)
        os.mkdir(aedtTargetDir)
    
    copy(source,aedtTarget)
    
    edbSource = source[:-5]+".aedb" +"/edb.def"
    edbTargetdir = aedtTarget[:-5]+".aedb"
    
    #if not 3DL
    if not os.path.exists(edbSource):
        return
    
    if not os.path.exists(edbTargetdir):
        log.debug("make dir: %s"%edbTargetdir)
        os.mkdir(edbTargetdir)
    copy(edbSource,edbTargetdir)
    
    
    

def ProcessTime(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        log.info("start function: {0}".format(func.__name__))
        if isIronpython:
            tfun = time.clock
        else:
            tfun = time.time
            
        start = tfun()
        func(*args, **kwargs)
        end = tfun()
        
        log.info("{0}: Process time {1}s".format(func.__name__,end-start))
    return wrapped_function

def DisableAutoSave(func):
    @wraps(func)
    def wrapped_function(self,*args, **kwargs):
        log.info("Disable AutoSave for function: {0}".format(func.__name__))
        temp = self.layout.enableAutosave(flag=False)
        func(self,*args, **kwargs)
        log.info("Recover AutoSave for function: {0}".format(func.__name__))
        temp = self.layout.enableAutosave(flag=temp)
    return wrapped_function


# class ProgressBar(object):
# 
#     def __init__(self,total=100,prompt="progress",step=3):
#         self.total = total
#         self.prompt = prompt
#         self.step = step
#         self.pos = 0
#         self.temp = 0
#         self.start = None
#         
#     def showPercent(self,pos=None):
#         if self.start == None:
#             self.start = time.time()
#         if pos==None:
#             self.pos +=1
#         else:
#             self.pos = None
#             
#         progress = int(self.pos*100/self.total)
#         if progress>self.temp:
# #             print("\r{} %{}: {}".format(self.prompt,progress, "#" * (int(progress/self.step)+1)),end="")
#             finsh = "▓" * int(progress/self.step+1)
#             need_do = "-" * int(100/self.step - int(progress/self.step+1))
#             dur = time.time() - self.start
#             print("\r{}: {:^3.0f}%[{}->{}]  {:.2f}s  ".format(self.prompt,progress, finsh, need_do, dur), end="")          
# #             sys.stdout.flush()
#             self.temp = progress
#         
#     def animation(self):
#         pass
