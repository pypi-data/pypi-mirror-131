import re

'''
解析配置参数，接受三种参数:
1. 类对象
2. json 文件
3. dict 参数字典
返回包含参数属性的对象
'''

def from_dict(dic):
    pass

def from_json(path):
    pass

def config_setup(config):
    if isinstance(config,object):
        return config
    elif isinstance(config,'str'):
        pass
    elif isinstance(config,dict):
        pass
    else:
        raise NotImplementedError
    
def strconfig(config:object):
    attrs=[]
    for name in dir(config):
        if callable(getattr(config, name)):continue
        if re.match('__.*__',name):continue
        attrs.append(name)
    
    s = '\n# ----------------------------parameters table--------------------------- #\n'
    for name in attrs:
        s += f'{name}: {getattr(config, name)}\n'
    s += '# ------------------------------------------------------------------------ #'
    return s