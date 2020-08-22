# -*- coding:utf-8 -*

# ********************************************
# <editor-fold desc="模块：导入">

# --- 系统
import os

# --- 正则
import re

# --- 配置文件解析
import configparser

# </editor-fold>

# ********************************************
# <editor-fold desc="类：定义">

# 工具方法处理类
class class_tool:

    # 构造函数
    def __init__(self):
        pass

    # 执行操作系统命令
    def os_execute_command_output_resultset(self, str_command):

        # 返回值
        data_return = ""

        # 处理
        data_return = os.popen(str_command).read()

        # 格式化结果集
        if not isinstance(data_return, str):
            data_return.decode("gbk")

        data_return.split("\t")
        data_return = data_return.strip("\n")

        # 返回阶段
        return data_return

    # 从一个字符串中按照一组或者两组索引列表截取目标值，并组成列表返回
    def string_find_substring_list_with_index_list(self, data_origin, index_list_begin, index_list_end=[]):

        # 返回值
        data_return = []

        # 起点槽
        slot_start = 0

        # 终点槽
        slot_end = 0

        # 临时截取值
        slot_sub_string = ""

        # 处理
        for_cursor = 1
        for for_item in index_list_begin:
            if index_list_end == []:

                if for_cursor % 2 == 0:
                    # 偶数字符，确定结束
                    # 显示
                    # print("收尾分隔符 | 一致")
                    # 处理
                    slot_end = for_item
                    # 获得当前截取值
                    slot_sub_string = data_origin[slot_start:slot_end].strip()
                else:
                    slot_start = for_item + 1

            else:
                slot_start = for_item + 1
                slot_end = index_list_end[for_cursor - 1]
                # 获得当前截取值
                slot_sub_string = data_origin[slot_start:slot_end].strip()

            # 显示
            # print("当前截取值【" + slot_sub_string + "】")

            # 赋值返回值
            # --- 如果得到的替换区间字符串不为空，就追加到最终列表中
            if not slot_sub_string.isspace() and slot_sub_string !="":
                data_return.append(slot_sub_string)

            # 自增
            for_cursor += 1

        # 返回阶段
        return data_return

    # 计算某个字符在字符串中的索引位置，并输出列表
    def string_find_char_output_index_list(self, data_string, char):

        # 返回值
        data_return = []

        # 处理
        for index_cursor in range(len(data_string)):
            if data_string[index_cursor] == char:
                data_return.append(index_cursor)

        # 返回阶段
        return data_return

# 配置文件处理类
class class_config:

    # 类：构造函数
    def __init__(self, config_file_name):

        # 对象
        # --- 对象：配置文件操纵
        self.class_obj_configparser = configparser.ConfigParser(
            allow_no_value=False
        )

        # --- 对象：工具
        self.class_obj_tool = class_tool()

        # 变量

        # 处理
        self.class_obj_configparser.read(
            filenames=config_file_name,
            encoding="utf-8"
        )

    # config file | 扩充方法 | 替换语法
    # --- replace_by | os_command | 用操作系统的执行结果替换
    # --- replace_by | config_file | 用配置文件的其他参数的值替换
    def config_file_plus_replace(self, data_origin, sign_begin, sign_end, replace_by=""):
        # 返回值
        data_return = ""

        # 验证：语法 | 分隔符是否成对出现
        # --- 计算值
        count_sign_begin = str(data_origin).count(sign_begin)
        count_sign_end = str(data_origin).count(sign_end)
        # --- 结论
        # 语法是否正确 | 默认不正确
        isOk_grammar = False

        # 等待替换的列表
        replacement = ""

        if sign_begin == sign_end:
            # 收尾分隔符 | 相同

            # 任选一个计数，是否是偶数
            if count_sign_begin % 2 == 0:

                # 显示
                # print("输出信息：语法 | 替换语法中的替换字符【必须】成对出现 ---> 满足")

                # 赋值：语法是否正确
                isOk_grammar = True

            else:
                print("输出信息：语法 | 替换语法中的替换字符【必须】成对出现 ---> 不满足")
        else:
            # 收尾分隔符 | 不相同

            if count_sign_begin == count_sign_end:
                # 显示
                # print("输出信息：语法 | 替换语法中的替换字符【必须】成对出现 ---> 满足")

                # 赋值：语法是否正确
                isOk_grammar = True

            else:
                print("输出信息：语法 | 替换语法中的替换字符【必须】成对出现 ---> 不满足")

                sign_miss_count = abs(count_sign_begin-count_sign_end)

                if count_sign_begin > count_sign_end:
                    print("----> 缺少｛标记替换位｝结束的字符：" + str(sign_miss_count) + "个")
                else:
                    print("----> 缺少｛标记替换位｝开始的字符：" + str(sign_miss_count) + "个")

        # 处理：到这里，配置文件的扩展语法｛替换｝的语法就应该没问题了
        if isOk_grammar:
            # 语法正确后开始处理

            # 获取字符串中，特定字符的索引列表
            # 由于前面语法检测通过，所以这个列表一定是偶数个成员
            # 但是，根据收尾分隔符的不同，这个列表的最终呈现也会不同

            # 获取等待替换的列表

            # 替换符号相同
            if sign_begin == sign_end:
                # 相同的时候随便写哪个字符参与计算，都没关系
                char_index_list = self.class_obj_tool.string_find_char_output_index_list(
                    data_string=data_origin,
                    char=sign_begin
                )

                # 处理
                replacement = self.class_obj_tool.string_find_substring_list_with_index_list(
                    data_origin=data_origin,
                    index_list_begin=char_index_list
                )

            # 替换符号不同
            else:
                # 替换符号不同的时候，要分起始字符和结束字符两条列表
                char_index_list_begin = self.class_obj_tool.string_find_char_output_index_list(
                    data_string=data_origin,
                    char=sign_begin
                )
                char_index_list_end = self.class_obj_tool.string_find_char_output_index_list(
                    data_string=data_origin,
                    char=sign_end
                )

                # 处理
                replacement = self.class_obj_tool.string_find_substring_list_with_index_list(
                    data_origin=data_origin,
                    index_list_begin=char_index_list_begin,
                    index_list_end=char_index_list_end
                )

            # 处理等待替换的列表
            for replace_item in replacement:

                # 显示
                # print("==========")
                # print(replace_item)

                # 变量
                sed_old = sign_begin + replace_item + sign_end

                sed_new = ""
                sed_new_part_middle = ""

                # 获取新值
                if replace_by == "os_command":
                    # 以操作系统的命令的结果集替换 | 命令结果集最好控制在一行以内
                    os_command_result = self.class_obj_tool.os_execute_command_output_resultset(
                        str_command=replace_item
                    )
                    # 显示
                    # print("【" + os_command_result + "】")
                    # 赋值
                    sed_new_part_middle = os_command_result

                elif replace_by == "config_file":
                    # 用配置文件的其他的【Section】中的【Key】的值替换
                    # --- 当前的代码版本，仅支持从当前配置文件获取值

                    # 如果是这种情况，则数据的格式为：section.key

                    # 验证语法
                    if '.' in replace_item:
                        if replace_item.count('.') == 1:
                            # 语法正确，可以做正事了
                            current_name_section = replace_item.split('.')[0]
                            current_name_key = replace_item.split('.')[1]

                            sed_new_part_middle = self.configparser_do_search_value_with_section_key(
                                name_section=current_name_section,
                                name_key=current_name_key,
                                is_Transfer=True
                            )
                        else:
                            print("@@@@ 引用配置文件的参数的语法【错误】")
                            print("----> 过多的访问操作符")
                    else:
                        print("@@@@ 引用配置文件的参数的语法【错误】")
                        print("----> 没有访问操作符")

                # 准备替换
                if sed_new_part_middle != "":
                    # 替换后的值
                    sed_new = sed_new_part_middle

                    # 显示
                    # print("旧的：" + sed_old)
                    # print("新的：" + sed_new)

                    # 执行替换
                    data_return = str(data_origin).replace(
                        sed_old,
                        sed_new
                    )

                else:
                    print("@@@@ 我并不知道要替换成什么 @@@@")

        else:
            print("@@@@ 请先修正语法问题 @@@@")

        # 返回阶段
        return data_return

    # configparser | 查找方法 | 获取某个｛section｝中的｛key｝的值
    def configparser_do_search_value_with_section_key(self, name_section, name_key, is_Transfer):

        # 返回值
        data_return = ""

        # 处理
        # ======================
        # 原始数据
        data_origin = self.class_obj_configparser.get(
            section=name_section,
            option=name_key
        )

        # 判断：是否需要转义处理
        if is_Transfer:

            # 转义完成后的数据
            data_transfer_after = data_origin

            # 处理：转换操作
            # --------------------------

            # 配置文件的参数引用
            while "@" in data_transfer_after:
                data_transfer_after = self.config_file_plus_replace(
                    data_origin=data_transfer_after,
                    sign_begin="@",
                    sign_end="@",
                    replace_by="config_file"
                )

            # 操作系统命令
            while "`" in data_transfer_after:
                data_transfer_after = self.config_file_plus_replace(
                    data_origin=data_transfer_after,
                    sign_begin="`",
                    sign_end="`",
                    replace_by="os_command"
                )

                # 显示
                # print("#################")
                # print(data_transfer_after)

            # --------------------------

            # 通过赋值，传递给函数返回值
            data_return = data_transfer_after

        else:
            data_return = data_origin

        # ======================

        # 返回阶段
        return data_return

# </editor-fold>

# ********************************************
# <editor-fold desc="主函数">
# if __name__ == "__main__":
#
#     # %%%%%%%%%%%%%%%%%%
#     # print("样例：<你好，世界>")
#
#     obj_config = class_config(
#         config_file_name="config.cfg"
#     )
#
#     hostname = obj_config.configparser_do_search_value_with_section_key(
#         name_section="os",
#         name_key="hostname",
#         is_Transfer=True
#     )
#
#     print("===============")
#     print(hostname)

# </editor-fold>

# ********************************************
# 结束阶段
# ********************************************
# Finished