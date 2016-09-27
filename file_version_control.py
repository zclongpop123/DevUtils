#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Thu, 01 Sep 2016, 14:14:10
#========================================
import os, re, string, itertools
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
VERSION_PRECISION     = 3

DEFAULT_FILE_EXT      = 'ma'

VERSION_MATCH_PATTERN = '(?<=v)\d{{{0}}}(?=\.)'.format(VERSION_PRECISION)

FIRST_VERSION_FILE    = 'Name_v{0}.{1}'.format(string.zfill(1, VERSION_PRECISION), DEFAULT_FILE_EXT)





def get_file_version(filePath):
    '''
    Get file's version...
    Exp:
        D:/test/name_v001.ma - 001
        D:/test/name_v002.ma - 002
        ...
    '''
    version = re.search(VERSION_MATCH_PATTERN, os.path.basename(filePath))
    if version:
        return version.group()





def get_file_list(path, kWords=None, ext=None):
    '''
    Get versions and files in input path...
    Exp:
        001 - D:/test/name_v001.ma
        002 - D:/test/name_v002.ma
        ...
    '''
    if not os.path.isdir(path):
        return

    files = os.listdir(path)
    for f in files:
        if kWords and not re.search(kWords, f):
            continue

        if ext and not re.search('{0}$'.format(ext), f):
            continue

        version = get_file_version(f)
        if not version:
            continue

        yield version, os.path.normpath(os.path.join(path, f))





def get_version_list(path, kWords=None, ext=None):
    '''
    Get versions from input path...
    Exp:
        ['001', '002', '003' ... ]
    '''
    versions = dict(get_file_list(path, kWords, ext)).keys()
    versions.sort(key=lambda v:int(v), reverse=True)

    return versions





def get_last_version(path, kWords=None, ext=None):
    '''
    Get the last version from input path...
    Exp:
        ['001', '002', '003'] -> '003'
        ['001',   ..., '999'] -> '999'
    '''
    versions = get_version_list(path, kWords, ext)
    versions.append(string.zfill(0, VERSION_PRECISION))

    last_version = max(itertools.imap(int, versions))

    return string.zfill(last_version, VERSION_PRECISION)





def get_next_version(path, kWords=None, ext=None):
    '''
    Get a new version from input path...
    Exp:
        ['001', '002', '003'] -> '004'
        ['001',   ..., '998'] -> '999'
    '''
    last_version = get_last_version(path, kWords, ext)
    next_version = string.zfill(int(last_version) + 1, VERSION_PRECISION)

    return next_version





def get_versiond_file(path, version, kWords=None, ext=None):
    '''
    Get a file path by input path and input version...
    Exp:
        001 -> D:/test/name_v001.ma
    '''
    filePath = dict(get_file_list(path, kWords, ext)).get(version, '')
    return filePath





def get_last_file(path, kWords=None, ext=None):
    '''
    Get the last file path by input path...
    Exp:
        ['001', ..., '005'] -> D:/test/name_v005.ma
    '''
    version  = get_last_version(path, kWords, ext)
    filePath = get_versiond_file(path, version, kWords, ext)
    return filePath





def get_next_file(path, kWords=None, ext=None):
    '''
    Get the new file path by input path...
    Exp:
        ['001', ..., '005'] -> D:/test/name_v006.ma
    '''
    last_file = get_last_file(path, kWords, ext)

    if last_file:
        new_v = get_next_version(path, kWords, ext)
        new_f = re.sub(VERSION_MATCH_PATTERN, new_v, os.path.basename(last_file))

    else:
        new_f = FIRST_VERSION_FILE
        if ext:
            new_f = FIRST_VERSION_FILE.replace(DEFAULT_FILE_EXT, ext)

    filePath = os.path.normpath(os.path.join(path, new_f))
    return filePath
