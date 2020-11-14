#!/usr/bin/env python3
# Made By UTS
# Write Python code in Chinese, you can understand it at a glance

import logging
import os
import re
import sys
import time

logging.basicConfig(level=logging.DEBUG, format=' %(levelname)s - %(asctime)s - %(message)s')


# logging.disable(logging.CRITICAL)

def indentation(code_str):
    indentation_finder = re.compile(r'^(\s*)?(.*)')
    code_in = indentation_finder.search(code_str)
    indentation_num = int((len(code_in[1])) / 4)
    return [indentation_num, code_in[2]]


def cpy_while(code_str, file_name, indentation):
    if code_str.startswith('当') and '时执行' in code_str:
        code_str = code_str.replace('时执行', '')
        code_str = code_str.replace('大于等于', ' >= ')
        code_str = code_str.replace('小于等于', ' <= ')
        code_str = code_str.replace('大于', ' > ')
        code_str = code_str.replace('小于', ' < ')
        code_str = code_str.replace('不等于', '!=')
        code_str = code_str.replace('等于', ' == ')
        code_str = code_str.replace('且', ' and ')
        code_str = code_str.replace('或', ' or ')
        code_str = code_str.replace('真', ' True ')
        code_str = code_str.replace('假', ' False ')
        code_str = code_str.replace('为', ' == ')
        code_str = code_str.replace('在', ' in ')
        code_str = code_str.replace('不在', ' not in ')
        code_str = code_str.replace('不为', ' not ')
        code_str = code_str.replace('：', ':')
        code_str = code_str.replace('变量', '_')
        logging.debug(f'while循环预编译: {code_str}')
        file_code = open(file_name, 'a')
        file_code.write(indentation * '    ' + 'while ' + code_str[1:] + "\n")
        file_code.close()
        return True


def cpy_import(code_str, file_name, indentation):
    if code_str.startswith('导入模块'):
        if '重命名为' in code_str and '，' not in code_str:
            code_str = code_str.replace('导入模块', 'import ')
            code_str = code_str.replace('重命名为', ' as ')
            logging.debug(f"导入模块预写入: {code_str}")
            file_code = open(file_name, 'a')
            file_code.write(indentation * '    ' + code_str + "\n")
            file_code.close()
            return True
        else:
            code_str = code_str.replace('导入模块', 'import ')
            code_str = code_str.replace('，', ', ')
            logging.debug(f"导入模块预写入: {code_str}")
            file_code = open(file_name, 'a')
            file_code.write(indentation * '    ' + code_str + "\n")
            file_code.close()
            return True
    else:
        return False

def cpy_conversion(code_str, file_name, indentation):
    if code_str.startswith('格式化'):
        if '保存到' in code_str:
            return True
        else:
            find_re  = re.compile(r'格式化(.*)为(字符串|浮点数|整数)', re.DOTALL)
            code_str = find_re.sub(r'\1 = \2(\1)', code_str)
            code_str = code_str.replace('字符串', 'str')
            code_str = code_str.replace('浮点数', 'float')
            code_str = code_str.replace('整数', 'int')
            code_str = code_str.replace('变量', '_')
            file_code = open(file_name, 'a')
            file_code.write(indentation * '    ' + code_str + "\n")
            file_code.close()
            return True
    else:
        return False



def cpy_print(code_str, file_name, indentation):
    logging.debug(f'传递的值为: {code_str}')
    if code_str.startswith('格式化输出'):
        print_re = re.compile(r'^格式化输出\'(.*)\'$', re.DOTALL)
        print_code = print_re.search(code_str)
        file_code = open(file_name, 'a')
        logging.debug("写入"+indentation * '    ' + 'print(' + print_code.group(1) + ")")
        file_code.write(indentation * ' ' + 'print(r' + print_code.group(1) + ")\n")
        file_code.close()
        return True
    elif code_str.startswith('输出'):
        values_re = re.compile(r'变量(.*)', re.DOTALL)
        code_str = code_str.replace('加', ' + ')
        code_str = code_str.replace('减', ' - ')
        code_str = code_str.replace('乘', ' * ')
        code_str = code_str.replace('除', ' / ')
        code_str = code_str.replace('等于', ' = ')
        code_str = code_str.replace('输出', '')
        code_str = code_str.replace('，', ',')
        code_str = values_re.sub(r'_\1', code_str)
        file_code = open(file_name, 'a')
        logging.debug(f"编译后代码为: {code_str}")
        file_code.write(indentation * '    ' + 'print(' + code_str + ")\n")
        file_code.close()
        return True
    else:
        return False


def cpy_math(code_str, file_name, indentation):
    if code_str.startswith('计算'):
        values_re = re.compile(r'变量(\w+)')
        code_str = code_str.replace('加', ' + ')
        code_str = code_str.replace('减', ' - ')
        code_str = code_str.replace('乘', ' * ')
        code_str = code_str.replace('除', ' / ')
        code_str = code_str.replace('等于', ' = ')
        code_str = values_re.sub(r'_\1', code_str)
        logging.debug(f'计算代码为: {code_str}')
        file_code = open(file_name, 'a')
        file_code.write(indentation * '    ' + code_str[2:] + "\n")
        file_code.close()
        return True
    elif '自加' in code_str:
        values_re = re.compile(r'变量(\w+)')
        code_str = code_str.replace('自加', ' += ')
        code_str = values_re.sub(r'_\1', code_str)
        logging.debug(f'计算代码为: {code_str}')
        file_code = open(file_name, 'a')
        file_code.write(indentation * '    ' + code_str + "\n")
        file_code.close()
        return True
    elif '自减' in code_str:
        values_re = re.compile(r'变量(\w+)')
        code_str = code_str.replace('自减', ' -= ')
        code_str = values_re.sub(r'_\1', code_str)
        logging.debug(f'计算代码为: {code_str}')
        file_code = open(file_name, 'a')
        file_code.write(indentation * '    ' + code_str + "\n")
        file_code.close()
        return True
    elif '自乘' in code_str:
        values_re = re.compile(r'变量(\w+)')
        code_str = code_str.replace('自乘', ' *= ')
        code_str = values_re.sub(r'_\1', code_str)
        logging.debug(f'计算代码为: {code_str}')
        file_code = open(file_name, 'a')
        file_code.write(indentation * '    ' + code_str + "\n")
        file_code.close()
        return True
    elif '自除' in code_str:
        values_re = re.compile(r'变量(\w+)')
        code_str = code_str.replace('自除', ' /= ')
        code_str = values_re.sub(r'_\1', code_str)
        logging.debug(f'计算代码为: {code_str}')
        file_code = open(file_name, 'a')
        file_code.write(indentation * '    ' + code_str + "\n")
        file_code.close()
        return True
    else:
        return False


def create_variable(code_str, file_name, indentation):
    if code_str.startswith('创建变量'):
        if '值为' in code_str or '为' in code_str:
            input_re = re.compile(r'用户输入((\"|\')+.*(\"|\')+)?')
            code_str = input_re.sub(r'input(\1)', code_str)
            i = 0
            flag = True
            while i < len(code_str) and flag:
                if code_str[i] == '值' and code_str[i+1] == '为':
                    flag = False
                else:
                    i += 1
            file_code = open(file_name, 'a')
            file_code.write(indentation * '    ' + '_' + code_str[4:i] + ' = ' + code_str[i+2:] + "\n")
            file_code.close()
            return True
        else:
            file_code = open(file_name, 'a')
            file_code.write(indentation * '    ' + '_' +code_str[4:] + ' = None' + "\n")
            file_code.close()
            return True
    elif code_str.startswith('更新变量'):
        if '值为' in code_str:
            input_re = re.compile(r'用户输入(\"|\'.*\"|\')?')
            code_str = input_re.sub(r'input(\1)', code_str)
            i = 0
            flag = True
            while i < len(code_str) and flag:
                if code_str[i] == '值' and code_str[i+1] == '为':
                    flag = False
                else:
                    i += 1
            file_code = open(file_name, 'a')
            file_code.write(indentation * '    ' + '_' + code_str[4:i] + ' = ' + code_str[i+2:] + "\n")
            file_code.close()
            return True
        else:
            return False
    else:
        return False




def cpy_if_elif_else(code_str, file_name, indentation):
    if code_str.startswith('如果'):
        code_str = code_str.replace('如果', 'if ')
        code_str = code_str.replace('大于等于', ' >= ')
        code_str = code_str.replace('小于等于', ' <= ')
        code_str = code_str.replace('大于', ' > ')
        code_str = code_str.replace('小于', ' < ')
        code_str = code_str.replace('不等于', '!=')
        code_str = code_str.replace('等于', ' == ')
        code_str = code_str.replace('且', ' and ')
        code_str = code_str.replace('或', ' or ')
        code_str = code_str.replace('真', ' True ')
        code_str = code_str.replace('假', ' False ')
        code_str = code_str.replace('为', ' == ')
        code_str = code_str.replace('在', ' in ')
        code_str = code_str.replace('不在', ' not in ')
        code_str = code_str.replace('不为', ' not ')
        code_str = code_str.replace('：', ':')
        code_str = code_str.replace('变量', '_')
        file_code = open(file_name, 'a')
        file_code.write(indentation * '    ' + code_str +"\n")
        file_code.close()
        return True
    elif code_str.startswith('否则如果'):
        code_str = code_str.replace('否则如果', 'elif ')
        code_str = code_str.replace('大于等于', ' >= ')
        code_str = code_str.replace('小于等于', ' <= ')
        code_str = code_str.replace('大于', ' > ')
        code_str = code_str.replace('小于', ' < ')
        code_str = code_str.replace('不等于', '!=')
        code_str = code_str.replace('等于', ' == ')
        code_str = code_str.replace('且', ' and ')
        code_str = code_str.replace('或', ' or ')
        code_str = code_str.replace('真', ' True ')
        code_str = code_str.replace('假', ' False ')
        code_str = code_str.replace('为', ' == ')
        code_str = code_str.replace('在', ' in ')
        code_str = code_str.replace('不在', ' not in ')
        code_str = code_str.replace('不为', ' not ')
        code_str = code_str.replace('：', ':')
        code_str = code_str.replace('变量', '_')
        file_code = open(file_name, 'a')
        file_code.write(indentation * '    ' + code_str + "\n")
        file_code.close()
        return True
    elif code_str.startswith('否则'):
        code_str = code_str.replace('否则', 'else ')
        code_str = code_str.replace('大于等于', ' >= ')
        code_str = code_str.replace('小于等于', ' <= ')
        code_str = code_str.replace('大于', ' > ')
        code_str = code_str.replace('小于', ' < ')
        code_str = code_str.replace('不等于', '!=')
        code_str = code_str.replace('等于', ' == ')
        code_str = code_str.replace('且', ' and ')
        code_str = code_str.replace('或', ' or ')
        code_str = code_str.replace('真', ' True ')
        code_str = code_str.replace('假', ' False ')
        code_str = code_str.replace('为', ' == ')
        code_str = code_str.replace('在', ' in ')
        code_str = code_str.replace('不在', ' not in ')
        code_str = code_str.replace('不为', ' not ')
        code_str = code_str.replace('：', ':')
        code_str = code_str.replace('变量', '_')
        file_code = open(file_name, 'a')
        file_code.write(indentation * '    ' + code_str + "\n")
        file_code.close()
        return True

if __name__ == '__main__':
    file_lists = os.listdir('.')
    file_lists_str = str(file_lists)
    true_file_lists = []
    true_files_re = re.compile(r'^cpy_(\w+).txt$')

    print("开始搜寻编译文件……")
    logging.info(f"当前文件列表{file_lists_str}")

    for file in file_lists:
        true_file_re = true_files_re.search(file)
        try:
            true_file = true_file_re.group()
            true_file_lists.append(true_file)
        except AttributeError:
            true_file = None
        logging.debug(f"当前文件{file},正则表达式{true_file_re},文件{true_file}")

    true_file_lists_str = str(true_file_lists)
    logging.info(f"文件列表{true_file_lists_str}")

    file_len = str(len(true_file_lists))
    print(f'搜寻到可编译文件数量为{file_len}.')

    if 'cpy_main.txt' not in true_file_lists:
        print('请输入主程序名称...')
        main_file_name = input('Name: ')
        if main_file_name in true_file_lists:
            compile_file_name = main_file_name.split('.')[0] + '.py'
        else:
            print('无法寻找到指定文件!!!')
            logging.critical(f'输入的文件名称{main_file_name}无法在预编译文件找到!')
            sys.exit()
    else:
        main_file_name = 'cpy_main.txt'
        compile_file_name = 'cpy_main.py'

    logging.info(f'主程序文件为{main_file_name},编译文件名为{compile_file_name}')

    for file_name in true_file_lists:
        file_write_name = file_name.split('.')[0] + '.py'
        logging.debug(f'当前预编译文件名称为{file_write_name}')
        file = open(file_write_name, 'w')
        file.close()

    for file_name in true_file_lists:
        file = open(file_name, 'r')
        code_list = file.readlines()
        i = 1
        file_write_name = file_name.split('.')[0] + '.py'
        logging.debug(f'当前预编译文件名称为{file_write_name}')
        for code in code_list:
            if code == '\n':
                print(f'Line{i}: 不能输入空白行')
                sys.exit()
            logging.info("当前编译代码为: {%s}..." % code)
            code_indentation_code_txt_list = indentation(code)
            logging.info(
                "当前返回的缩进数量为" + str(code_indentation_code_txt_list[0]) + ", 代码文本为{" + str(
                    code_indentation_code_txt_list[1]) + "}...")
            if cpy_print(code_indentation_code_txt_list[1], file_write_name, code_indentation_code_txt_list[0]):
                logging.info('写入成功')
                continue
            elif create_variable(code_indentation_code_txt_list[1], file_write_name, code_indentation_code_txt_list[0]):
                logging.info('写入成功')
                continue
            elif cpy_math(code_indentation_code_txt_list[1], file_write_name, code_indentation_code_txt_list[0]):
                logging.info('写入成功')
                continue
            elif cpy_if_elif_else(code_indentation_code_txt_list[1], file_write_name, code_indentation_code_txt_list[0]):
                logging.info('写入成功')
                continue
            elif cpy_conversion(code_indentation_code_txt_list[1], file_write_name, code_indentation_code_txt_list[0]):
                logging.info('写入成功')
                continue
            elif cpy_import(code_indentation_code_txt_list[1], file_write_name, code_indentation_code_txt_list[0]):
                logging.info('写入成功')
                continue
            elif cpy_while(code_indentation_code_txt_list[1], file_write_name, code_indentation_code_txt_list[0]):
                logging.info('写入成功')
                continue
            else:
                file_write = open(file_write_name, 'a')
                file_write.write(code_indentation_code_txt_list[1]+"\n")
                file_write.close()
                logging.info('写入成功')

    print('编译成功...')
    time.sleep(1)
    print('输出编译后文件内容...')
    time.sleep(1)
    print("\n"+compile_file_name.center(23, '*'))
    print("***********************\n")

    os.system('python3 ' + compile_file_name)

    print("\n***********************\n***********************\n")
    print('Done.')
