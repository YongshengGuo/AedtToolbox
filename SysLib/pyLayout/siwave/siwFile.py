#--- coding=utf-8
#--- @Author: Yongsheng.Guo@ansys.com, Henry.he@ansys.com,Yang.zhao@ansys.com
#--- @Time: 20250331


import re,os
from ..common.common import log,readlines,readData


class SiwFile(object):

    def __init__(self,path):
        self.path = path
        self.datas = None
        self.load(path)
    

    def search(self,regList,loc=0):
        if isinstance(regList, str):
            regList = [regList]
        
        i = loc
        maxi = len(self.datas)-1
        for reg in regList:
            flag = False
            while(True):
                try:
                    line = self.datas[i].strip().decode("utf-8")
                except:
                    i += 1
                    continue
                
                if re.search(reg,line):
                    flag = True
                    break
                if i<maxi:
                    i += 1
                else:
                    break
            if flag:
                continue
            else:
                log.error("Search not found! %s"%reg)
                return -1
                
        return i
    
    def replaceLine(self,regList,txt,loc=0):
        if isinstance(regList, str):
            regList = [regList]
        
        i = self.search(regList,loc)
        self.datas[i] = txt.encode("utf-8")

        return i
        

    def load(self,path):
        if path is not None and os.path.exists(path):
            self.path = path
        else:
            log.error("SiwFile: path is not exists!")
            return
        
        with open(path, 'rb') as file:
            # 读取文件内容，得到字节串
            content = file.read()
            file.close()
            # 将字节串解码为 Unicode 字符串

        self.datas = content.splitlines()

    def save(self,path=None):
        if path is None:
            path = self.path
        split = "\n".encode("utf-8")
        with open(path,'wb') as f:
            for line in self.datas:
                f.write(line+split)