#--- coding=utf-8
#--- @author: yongsheng.guo@ansys.com
#--- @Time: 20250330

import os,sys,re
import shutil
import filecmp
import configparser

appPath = os.path.realpath(__file__)
appDir = os.path.split(appPath)[0] 
sys.path.append(appDir)

def readIniFile(path):
    """
    read ini format file
    """
    if not os.path.exists(path):
        raise FileNotFoundError("配置文件%s不存在"%path)

    
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

def sync_folders(source_folder, target_folder, mode=1):
    """
    将源文件夹同步到目标文件夹，并删除目标文件夹中多余的文件。
    mode: 1-全量同步，0-增量同步
    """
    # 确保目标文件夹存在
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
 
    # 同步源文件夹中的文件和子目录到目标文件夹
    for root, dirs, files in os.walk(source_folder):

        # print("sync folder: %s"%root)
        # 计算相对路径
        relative_path = os.path.relpath(root, source_folder)
        target_root = os.path.join(target_folder, relative_path)
 
        if re.match(r".*[\\/]*\.\w+.*",relative_path):  #skip hidden folder
            # print("skip hidden folder: %s"%root)
            continue
        if "__pycache__" in relative_path: #skip __pycache__ folder
            # print("skip __pycache__ folder: %s"%root)
            continue

        print("sync folder: %s"%root)
        # 确保目标子目录存在
        if not os.path.exists(target_root):
            os.makedirs(target_root)
 
        # 同步文件
        for file in files:
            source_file = os.path.join(root, file)
            target_file = os.path.join(target_root, file)

            if not os.path.exists(target_file) or \
               os.path.getmtime(source_file) > os.path.getmtime(target_file):
                try:
                    shutil.copy2(source_file, target_file)  # 复制文件并保留元数据
                    print(f"Download file: {source_file} to {target_file}")
                except Exception as e:
                    print(f"Failed to Download file {source_file}. Reason: {e}")
 
        # 同步子目录（os.walk 已经处理了子目录的遍历，这里主要是确保目录结构）
        # 实际上，os.makedirs 在上面已经确保了目录结构的存在

    if not mode:
        return

    #mode = 1
    # 删除目标文件夹中多余的文件和子目录
    for root, dirs, files in os.walk(target_folder, topdown=False):
        # 删除多余的文件
        for file in files:
            target_file = os.path.join(root, file)
            source_file_path = os.path.join(source_folder, os.path.relpath(target_file, target_folder))
            if not os.path.exists(source_file_path):
                try:
                    os.remove(target_file)
                    print(f"Deleted extra file: {target_file}")
                except Exception as e:
                    print(f"Failed to delete {target_file}. Reason: {e}")
 
        # 删除多余的子目录
        for dir in dirs:
            target_dir = os.path.join(root, dir)
            source_dir_path = os.path.join(source_folder, os.path.relpath(target_dir, target_folder))
            if not os.path.exists(source_dir_path):
                try:
                    shutil.rmtree(target_dir)
                    print(f"Deleted extra directory: {target_dir}")
                except Exception as e:
                    print(f"Failed to delete {target_dir}. Reason: {e}")



def incremental_sync(src, dst):
    """
    增量同步（仅同步变化文件）
    :param src: 源文件夹路径
    :param dst: 目标文件夹路径
    """
    # 如果目标文件夹不存在则创建
    if not os.path.exists(dst):
        os.makedirs(dst)
    
    # 遍历源文件夹
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        
        # 如果是文件：检查是否需要更新
        if os.path.isfile(src_path):
            if not os.path.exists(dst_path) or \
               os.path.getmtime(src_path) > os.path.getmtime(dst_path):
                try:
                    print("Download file: %s"%src_path)
                    # shutil.copy2(src_path, dst_path)
                except:
                    print("copy file error: %s"%src_path)
        # 如果是子文件夹：递归同步
        elif os.path.isdir(src_path):
            name = os.path.basename(src_path)
            if name.startswith("."): #skip hidden folder
                continue
            if name == "__pycache__": #skip __pycache__ folder
                continue
            incremental_sync(src_path, dst_path)

# 使用示例
# incremental_sync("path/to/source", "path/to/destination")

def main():

    cfgPath = os.path.join(appDir,"../","toolbox.cfg")
    cfgDict = readIniFile(cfgPath)

    #only for debug
    # try:
    #     import socket
    #     # 获取主机名
    #     hostname = socket.gethostname()
    #     if cfgDict["Toolbox"]["server"].lower()[2:].startswith(hostname.lower()):
    #         print("Local Server path: %s"%cfgDict["Toolbox"]["server"])
    #         return
    # except Exception as e:
    #     pass

    if not os.path.exists(cfgDict["Toolbox"]["server"]):
        print("Server path not found: %s"%cfgDict["Toolbox"]["server"])
        return

    if len(sys.argv)>1 and sys.argv[1].lower() == "force":
        print("force update will remove all files in toolbox folder")
        sync_folders(cfgDict["Toolbox"]["server"],os.path.join(appDir,"../"),mode=1)
    else:
        print("Synch server path: %s"%cfgDict["Toolbox"]["server"])
        sync_folders(cfgDict["Toolbox"]["server"],os.path.join(appDir,"../"),mode=2)
    
    print("finished.")
        
if __name__ == '__main__':
#     test1()
    main()