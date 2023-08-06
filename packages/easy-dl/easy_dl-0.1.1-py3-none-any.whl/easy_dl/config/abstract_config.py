class AbstractConfig:
    '''
    初始化配置，接受三种参数:
    1. 类
    2. json 文件
    3. dict 参数字典
    '''
    def __init__(self) -> None:
        '''
        接收参数配置，并合并
        '''
        pass

    def parse(self):
        '''
        调用argparse，使得可以与用户进行交互
        '''
        pass

    def __str__(self):
        '''
        打印配置信息
        '''
        pass