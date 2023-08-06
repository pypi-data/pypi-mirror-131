"""
模拟 linux split 功能
文件拆分+合并
"""
import os


def split_file(file_name, size, out_name):
    """
    文件拆分
    :param file_name: 输入文件
    :param size: 单个文件大小（字节）
    :param out_name: 输出文件（shx-num结尾）
    :return:
    """
    with open(file_name, 'rb') as f1:
        count = 10
        while True:
            res = f1.read(size)
            if res == b'':
                break
            with open(f'{out_name}.shx{count}', 'wb') as f2:
                f2.write(res)
            print(f'------->out_name:{out_name}.shx{count}')
            count += 1


def merge_file(input_re_name, path, out_name):
    """
    文件合并
    :param input_re_name: shx-num 结尾的文件名前缀+‘*’（例 ：aaa.txt*）
    :param path: shx-num 结尾的文件所在的目录
    :param out_name: 输出文件
    :return:
    """
    file_list = get_list(input_re_name, path)
    for file_name in file_list:
        print('--------->Running...')
        with open(file_name, 'rb') as f1:
            for line in f1:
                with open(out_name, 'ab') as f2:
                    f2.write(line)
    print('--------->Complete!')


def get_list(input_re_name, path):
    """
    获取 shx-num 结尾文件列表
    :param input_re_name: shx-num 结尾的文件名前缀+‘*’（例 ：aaa.txt*）
    :param path: shx-num 结尾的文件所在的目录
    :return: 需要合并文件列表
    """
    file_list = os.listdir(path)
    file_list = sorted([i for i in file_list if i.startswith(input_re_name.strip('*')) and i.find('shx') != -1])
    print(f'---->file_list:{file_list}')
    return file_list


# if __name__ == '__main__':
    # txt 测试
    # split_file(r'aaa.txt', 60, 'aaa.txt')
    # merge_file('aaa.txt*', r'../split_file', 'bbb.txt')

    # zip 测试
    # split_file(r'test.zip',4*1024*1024,'test_split.zip')
    # merge_file('test_split.zip*',r'../split_file','test_merge.zip')

    # res = sorted(['aa15','aa52','aa45','aa17','aa19','aa12','aa29','aa31'])
    # print(res)
