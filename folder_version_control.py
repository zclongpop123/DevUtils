#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Fri, 02 Sep 2016, 14:16:37
#========================================
import os, re, string, itertools
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
VERSION_PRECISION     = 3

VERSION_MATCH_PATTERN = '(?<=v)\d{{{0}}}$'.format(VERSION_PRECISION)

FIRST_VERSION_FOLDER  = 'v{0}'.format(string.zfill(1, VERSION_PRECISION))



def get_folder_list(path, kWords=None):
    '''
    Get versions and folders in input path...
    Exp:
        001 - D:/test/v001
        002 - D:/test/v002
        ...
    '''
    if not os.path.isdir(path):
        return

    for folder in os.listdir(path):
        version = re.search(VERSION_MATCH_PATTERN, folder)
        if not version:
            continue

        if kWords and not re.search(kWords, folder):
            continue

        yield version.group(), os.path.normpath(os.path.join(path, folder))





def get_version_list(path, kWords=None):
    '''
    Get versions from input path...
    Exp:
        ['001', '002', '003' ... ]
    '''
    versions = dict(get_folder_list(path, kWords)).keys()
    versions.sort(key=lambda v:int(v), reverse=True)

    return versions





def get_last_version(path, kWords=None):
    '''
    Get the last version from input path...
    Exp:
        ['001', '002', '003'] -> '003'
        ['001',   ..., '999'] -> '999'
    '''
    versions = get_version_list(path, kWords)
    versions.append(string.zfill(0, VERSION_PRECISION))

    last_version = max(itertools.imap(int, versions))

    return string.zfill(last_version, VERSION_PRECISION)





def get_next_version(path, kWords=None):
    '''
    Get a new version from input path...
    Exp:
        ['001', '002', '003'] -> '004'
        ['001',   ..., '998'] -> '999'
    '''
    last_version = get_last_version(path, kWords)
    next_version = string.zfill(int(last_version) + 1, VERSION_PRECISION)

    return next_version





def get_versiond_folder(path, version, kWords=None):
    '''
    Get a folder path by input path and input version...
    Exp:
        001 -> D:/test/v001
    '''
    folder = dict(get_folder_list(path, kWords)).get(version, '')
    return folder





def get_last_folder(path, kWords=None):
    '''
    Get the last folder path by input path...
    Exp:
        ['001', ..., '005'] -> D:/test/v005
    '''
    version = get_last_version(path, kWords)
    folder  = get_versiond_folder(path, version, kWords)
    return folder





def get_next_folder(path, kWords=None):
    '''
    Get the new folder path by input path...
    Exp:
        ['001', ..., '005'] -> D:/test/v006
    '''

    last_folder = get_last_folder(path, kWords)

    if last_folder:
        new_v = get_next_version(path, kWords)
        new_f = re.sub(VERSION_MATCH_PATTERN, new_v, os.path.basename(last_folder))

    else:
        new_f = FIRST_VERSION_FOLDER

    folder = os.path.normpath(os.path.join(path, new_f))
    return folder
