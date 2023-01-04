# encoding=utf-8
import time, re, sys, datetime, importlib, os

importlib.reload(sys)


class UtilsBase:
    """基础逻辑层，python算法逻辑 不影响android 或 ios"""

    def __init__(self, driver):
        self.driver = driver

    """xml算法相关"""

    # 传入sizi[0,0][1080,1920] 返回 x,y 中间点
    def get_left_top_right_down_xy(self, size, agrs_x=0.5, args_y=0.5):
        left, top, right, bottom = self.get_left_top_right_down(size)
        x = left + (right - left) * agrs_x
        y = top + (bottom - top) * args_y
        return int(x), int(y)

    # 传入sizi[0,0][1080,1920] 返回 左上右下  left,top,right,down
    def get_left_top_right_down(self, size):
        if type(size) == dict:
            # print('是字典')
            left = size['left']
            right = size['right']
            bottom = size['bottom']
            top = size['top']
            return int(left), int(top), int(right), int(bottom)
        else:
            left_key = size.count('[')
            right_key = size.count(']')
            middle_key = size.count(',')
            # 左
            left = size.rsplit(',')[middle_key - 2]
            left = left.rsplit('[')[left_key - 1]
            # 上
            top = size.rsplit(',')[middle_key - 1]
            top = top.rsplit(']')[0]
            # 右
            right = size.rsplit(',')[middle_key - 1]
            right = right.rsplit('[')[1]
            # 下
            down = size.rsplit(',')[-1]
            down = down.rsplit(']')[0]
            return int(left), int(top), int(right), int(down)

    # 剪切text+size 返回文案 例如 你好[0,0][1080,1920] 返回 你好
    def cut_size(self, text_and_size):
        # 获取[的个数
        left_key = text_and_size.count('[')
        cut = '{}{}'.format('[', text_and_size.rsplit('[')[left_key - 1])
        return text_and_size.rsplit(cut)[0]

    # unicode 转 str 回车
    def u_to_str_enter(self, text):
        return text.replace('&#10;', '\n')

    # 列表去重只保留唯一
    def list_only(self, list_content):
        set1 = set(list_content)
        list_only = list(set1)
        list_only.sort(key=list_content.index)
        return list_only

    # ios通过 xml的type和name进行比较
    def get_type_name_rect(self, type_name_rect_list, type_text=None, name_text=None, type_equal=True, name_equal=True,
                           name_in=None, just_name=None):
        """
        type_text  type等于某个值
        name_text  type等于某个值
        含有某个值  name_equal=False  name_in=True

        """

        result_list = []
        for i in range(len(type_name_rect_list)):
            if just_name == None:
                type_name = type_name_rect_list[i].split('[')[0]
                type = type_name.split('&&')[0]
                name = type_name.split('&&')[1]
                # self.info('---type-name--')
                # self.info(type_name)
                # self.info(type)
                # self.info(name)
            else:
                name = type_name_rect_list[i]

            if type_text == None and name_text != None:
                if name_equal:
                    if name_text == name:
                        result_list.append(type_name_rect_list[i])
                elif name_equal == False and name_in == None:
                    if name_text != name:
                        result_list.append(type_name_rect_list[i])
                elif name_equal == False and name_in != None:
                    if name_text in name:
                        result_list.append(type_name_rect_list[i])

            if type_text != None and name_text == None:
                if type_equal:
                    if type == type_text:
                        result_list.append(type_name_rect_list[i])
                else:
                    if type != type_text:
                        result_list.append(type_name_rect_list[i])

            if type_text != None and name_text != None:
                if type_equal and name_equal:  # 同时相等
                    if type == type_text and name == name_text:
                        result_list.append(type_name_rect_list[i])
                elif not type_equal and name_equal:
                    if type != type_text and name == name_text:
                        result_list.append(type_name_rect_list[i])
                elif type_equal and not name_equal:
                    if type == type_text and name != name_text:
                        result_list.append(type_name_rect_list[i])
                elif not type_equal and not name_equal:
                    if type != type_text and name != name_text:
                        result_list.append(type_name_rect_list[i])
                else:
                    assert '错误' == 'get_type_name_rect 出现了不存在的情况'
        # self.info('---get_type_name_rect---')
        # self.info_list_len(result_list)
        return result_list

    # ios通过 xml的type和name进行比较
    def get_name_rect(self, name_rect_list, name_text, name_equal=True):
        result_list = []
        for i in range(len(name_rect_list)):
            name = name_rect_list[i].split('[')[0]
            if name_equal:  # 同时相等
                if name_text == name:
                    result_list.append(name_rect_list[i])
            else:
                if name_text != name:
                    result_list.append(name_rect_list[i])
        if len(result_list) == 0:
            assert '错误' == 'get_name_rect 没找到需要的内容'
        # self.info('---get_type_name_rect---')
        # self.info_list_len(result_list)
        return result_list

    # ios通过 xml的type和name进行比较
    def get_name_rect_in(self, name_rect_list, name_text, name_in=True):
        result_list = []
        for i in range(len(name_rect_list)):
            name = name_rect_list[i].split('[')[0]
            if name_in:  # 同时相等
                if name_text in name:
                    result_list.append(name_rect_list[i])
            else:
                if name_text not in name:
                    result_list.append(name_rect_list[i])
        if len(result_list) == 0:
            assert '错误' == 'get_name_rect_in 没找到需要的内容'
        return result_list

    # 把含有坐标的name剪成 只含有name 例如  薪火相传[42,197][360,229] 剪成 薪火相传
    def iget_name_rect_cut_rect(self, name_rect):
        name_list = []
        for i in range(len(name_rect)):
            name_list.append(name_rect[i].split('[')[0])
        return name_list

    # 把含有坐标的type 和 name剪成 只含有name 例如  Button&&薪火相传[42,197][360,229] 剪成 薪火相传
    def iget_type_name_rect_get_name(self, name_rect):
        name_list = []
        for i in range(len(name_rect)):
            left, top, right, down = self.get_left_top_right_down(name_rect[i])
            # 组合坐标
            just_size = "[{},{}][{},{}]".format(left, top, right, down)
            # 剪切坐标预留左边内容
            type_name = name_rect[i].split(just_size)[0]
            name = type_name.split('&&')[1]
            name_list.append(name)
        return name_list

    # 去掉rect 保留[之前的部分
    def get_cut_rect(self, xml_list):
        result_list = []
        if type(xml_list) == list:
            for i in range(len(xml_list)):
                left, top, right, down = self.get_left_top_right_down(xml_list[i])
                # 组合坐标
                just_size = "[{},{}][{},{}]".format(left, top, right, down)
                # 剪切坐标预留左边内容
                name = xml_list[i].split(just_size)[0]
                result_list.append(name)
            return result_list
        else:
            left, top, right, down = self.get_left_top_right_down(xml_list)
            # 组合坐标
            just_size = "[{},{}][{},{}]".format(left, top, right, down)
            # 剪切坐标预留左边内容
            name = xml_list.split(just_size)[0]
            return name

    # 去掉重复的内容
    def delet_size_repetition(self, content_list):
        # 上下左右单独剪切出来  例如 央视网[0,101][37,116] 剪切为 [0,101][37,116]
        cut_list = []
        for i in range(len(content_list)):
            left, top, right, down = self.get_left_top_right_down(content_list[i])
            size = "[{},{}][{},{}]".format(left, top, right, down)
            cut_list.append(size)
        # self.info('---cut_list---')
        # self.info(cut_list)
        # 判断上下左右字符串 重复的个数
        cut_dict = {}
        for i in cut_list:
            if cut_list.count(i) > 1:
                cut_dict[i] = cut_list.count(i)

        # self.info('---cut_dict---')
        # self.info(cut_dict)
        # 把重复的内容，去除掉（是一个也不保留，不是去重只留一个）
        delete_key_list = list(cut_dict.keys())

        # self.info('---cut_key---')
        # self.info_list_len(delete_key_list)

        result_list = []
        for i in range(len(content_list)):
            delete = False
            for l in range(len(delete_key_list)):
                if delete_key_list[l] in content_list[i]:
                    delete = True
            if not delete:
                result_list.append(content_list[i])
        return result_list

    """xml通过上下左右计算需要的按键位置"""

    def get_xml_size(self, xml_list, text_equal=None, text_in=None, width=None, height=None, width_height_multiple=2,
                     left=None, top=None,
                     right=None, down=None, count=None):
        """
        xml_list xml列表 需要带坐标
        width, 屏幕宽 默认为0
        height 屏幕高 默认为0
        text_equal= xml_list中需要与text_equal完全相等
        text_in= xml_list中需要包含text_in
        top，right,right,down,  各个方向传入的参数
        count 最后符合条件的数量

        """
        self.info('11')
        self.info("top {} dowm {}".format(top, down))
        result_text_list = []
        result_size_list = []
        value_num = None

        # 筛选相等目标文案数量
        if text_equal != None:
            # self.info('----get_xml_size-text_equal----')
            for i in range(len(xml_list)):
                if text_equal == xml_list[i].split('[')[0]:
                    result_text_list.append(xml_list[i])
            # self.info_list_len(result_text_list)
            if len(result_text_list) == 0:
                assert '错误' == 'get_xml_size 没有text_equal对应的文案'

        # 筛选包含目标文案数量
        if text_in != None:
            # self.info('----get_xml_size-text_in----')
            for i in range(len(xml_list)):
                if text_in in xml_list[i].split('[')[0]:
                    result_text_list.append(xml_list[i])
            # self.info_list_len(result_text_list)
            if len(result_text_list) == 0:
                assert '错误' == 'get_xml_size 没有text_in对应的文案'

        # 筛选后替换目标列表
        if len(result_text_list) > 0:
            # self.info('----result_text_list--to--xml_list---')
            # self.info_list_len(result_text_list)
            xml_list = result_text_list

        self.info('----xml_list----')
        # self.info_list_len(xml_list)
        self.info(len(xml_list))

        # 方向筛选
        result_size_list = xml_list

        if left != None:
            result_size_list = self.get_xml_size_left_top_right_down_screening(result_size_list, 'left', left,
                                                                               width=width, height=height,
                                                                               width_height_multiple=width_height_multiple)
            # self.info('---left_result_list---')
            # self.info_list_len(result_size_list)

        if top != None:
            result_size_list = self.get_xml_size_left_top_right_down_screening(result_size_list, 'top', top,
                                                                               width=width, height=height,
                                                                               width_height_multiple=width_height_multiple)
            # self.info('---top_result_list---')
            # self.info_list_len(result_size_list)
            # self.info('---top_result_list_end---')

        if right != None:
            result_size_list = self.get_xml_size_left_top_right_down_screening(result_size_list, 'right', right,
                                                                               width=width, height=height,
                                                                               width_height_multiple=width_height_multiple)
            # self.info('---right_result_list---')
            # self.info_list_len(result_size_list)

        if down != None:
            result_size_list = self.get_xml_size_left_top_right_down_screening(result_size_list, 'down', down,
                                                                               width=width, height=height,
                                                                               width_height_multiple=width_height_multiple)
            # self.info('---down_result_list---')
            # self.info_list_len(result_size_list)

        self.info('--result_size_list--')
        self.info_list_len(result_size_list)

        # 判断最后得出的数量
        if count == None:
            if len(result_size_list) > 0:

                return result_size_list
            else:
                assert '错误' == 'get_xml_size 最终筛选出符合结果的数量为0'
        else:
            if len(result_size_list) == count:
                return result_size_list
            else:
                assert '错误' == 'get_xml_size 最终筛选出符合结果的数量不一致'

    def get_xml_size_left_top_right_down_screening(self, xml_list, size_one, size_one_args, width=None, height=None,
                                                   width_height_multiple=2):
        check_size_one = 0

        # 拆分参数
        size_one_args_list = size_one_args.rsplit('|')
        # self.info(size_one_args_list)
        # self.info(len(size_one_args_list))
        # 判断传参正确
        if len(size_one_args_list) != 2:
            assert '错误' == '传入size上下左右参数不是|分隔符分隔后的两组'
        # 第一组比较运算符判断
        if size_one_args_list[0] not in ['>', '<', '>=', '<=', '==', '!=']:
            assert '错误' == '传入size上下左右参数第一组不是比较运算符'
        # 第二组校验判断
        if ':' in size_one_args_list[1]:  # 判断含有相对位置比较
            args_two_list = size_one_args_list[1].rsplit(':')
            if len(args_two_list) != 2:  # 校验第一组参数
                assert '错误' == '传入size上下左右参数第二组相对参数不是:分隔符分隔后的两组'
            if args_two_list[0] not in ['width', 'height']:
                assert '错误' == '传入size上下左右参数第二组参数相对参数文案不是width或height '
            if float(args_two_list[1]) > 1.0:
                assert '错误' == '传入size上下左右参数第二组参数相对参数系数没有小于1.0 '
            width_height_args = args_two_list[0]
            args_float = float(args_two_list[1])
            # 计算出要对比的数
            if width_height_args == 'width':
                value_num = width * args_float
            elif width_height_args == 'height':
                value_num = height * args_float
        elif size_one_args_list[1].isdigit():  # 如果是整数就判断
            value_num = int(size_one_args_list[1]) * width_height_multiple  # 乘以系数
        else:
            assert '错误' == '上下左右的 判断，传入了未知的类型 不是正整数，不是width和height相关'

        # self.info('---value_num---')
        # self.info(value_num)

        result_size_list = []
        # #筛选
        for i in range(len(xml_list)):
            left, top, right, down = self.get_left_top_right_down(xml_list[i])
            judge = size_one_args_list[0]
            if size_one == 'left':
                check_size_one = float(left)
            elif size_one == 'right':
                check_size_one = float(right)
            elif size_one == 'top':
                check_size_one = float(top)
            elif size_one == 'down':
                check_size_one = float(down)
            else:
                assert '错误' == '传入的参数不属于 left, top, right, down 其中任何一个'

            # 筛选方案
            if judge == '>':
                # self.info('--check_size_one--')
                # self.info(check_size_one)
                # self.info(value_num)
                if check_size_one * width_height_multiple > value_num:
                    result_size_list.append(xml_list[i])
            elif judge == '<':
                if check_size_one * width_height_multiple < value_num:
                    result_size_list.append(xml_list[i])
            elif judge == '>=':
                if check_size_one * width_height_multiple >= value_num:
                    result_size_list.append(xml_list[i])
            elif judge == '<=':
                if check_size_one * width_height_multiple <= value_num:
                    result_size_list.append(xml_list[i])
            elif judge == '==':
                if check_size_one * width_height_multiple == value_num:
                    result_size_list.append(xml_list[i])
            elif judge == '!=':
                if check_size_one * width_height_multiple != value_num:
                    result_size_list.append(xml_list[i])

        # self.info('---shaixuan---')
        # self.info_list_len(result_size_list)
        return result_size_list

    # 获取的xml 根据从上往下，从左往右排序
    def get_xml_size_sorting(self, xml_list):
        top_list = []
        left_list = []
        for i in range(len(xml_list)):
            left, top, right, down = self.get_left_top_right_down(xml_list[i])
            top_list.append(top)
            left_list.append(left)
        # 高度去重
        top_list = list(set(top_list))
        top_list.sort()
        # 宽度去重
        left_list = list(set(left_list))
        left_list.sort()
        result_list = []
        # 按照先高度再宽度进行排序添加
        for t in range(len(top_list)):
            for l in range(len(left_list)):
                for i in range(len(xml_list)):
                    left, top, right, down = self.get_left_top_right_down(xml_list[i])
                    if top == top_list[t] and left == left_list[l]:
                        result_list.append(xml_list[i])
        return result_list

    """正则表达式"""

    # 日期显示正确，带有年和不带年的
    def data_show_correct_right_year_or_not_year(self, this_data):
        # 例如 2020-12-21 或者 01-12
        assert self.re_match(self.get_re_pattern_data_month_to_day(), this_data) or self.re_match(
            self.get_re_pattern_data_year_to_day(), this_data)

    # 日期正则 月-日
    def get_re_pattern_data_month_to_day(self):
        # 12-05
        return u'[0-9]{2}[-][0-9]{2}'

    # 日期正则 年-月—日
    def get_re_pattern_data_year_to_day(self):
        # 2020-12-05
        return u'[0-9]{4}[-][0-9]{2}[-][0-9]{2}'

    # 时间正则
    def get_re_pattern_time(self):
        # 28:05
        return u'[0-9]{2}[:][0-9]{2}'

    # 时间正则
    def get_re_pattern_year_to_second_time(self):
        # 例子 2020-12-22 19:28:05
        return u'[0-9]{4}[-][0-9]{2}[-][0-9]{2}[ ][0-9]{2}[:][0-9]{2}[:][0-9]{2}'

    # 正则检查feed的拥有者和日期标签
    def re_text_is_data(self, text):
        # 例子 12-03
        assert self.re_match(r'[0,1][0-9][-][0,1,2,3][0-9]', text) or u'小时前' in text or u'天前' in text or self.re_match(
            r'[2][0][2][0][-][0,1][0-9][-][0,1,2,3][0-9]', text)

    # 包含有中文
    def re_text_has_cn(self, text):
        assert re.compile(u'[\u4e00-\u9fa5]').search(text)

    # text是中文
    def re_text_is_chinese(self, text):
        assert self.re_match('[\u4e00-\u9fa5]+', text)

    def re_match(self, pattern, string):
        return re.match(pattern, string)

    def re_match_list(self, pattern, text_list):
        result_list = []
        for i in range(len(text_list)):
            if re.match(pattern, text_list[i]):
                result_list.append(text_list[i])
        if len(result_list) > 0:
            return result_list
        else:
            assert '错误' == '传入的列表中没有找到正则对应的内容'

    # 标题显示正确
    def re_text_is_title(self, text):
        # 标题长度大于某个值
        assert len(text) > 2

    # 显示的是时间
    def re_is_times(self, times):
        assert self.re_match(r'[0-2][0-9][:][0-5][0-9]', times)

    """其他算法"""

    # 当前屏幕显示,
    def is_show_page(self, high_or_wide):
        """元素宽高大小如果小于N证明没有显示在当前屏幕中  """
        N = 10
        if high_or_wide > N:
            return True
        else:
            return False

    # 输入数字得到一个从1开始到num的字符串
    def get_int_str_list(self, num):
        list_one = []
        for i in range(1, num + 1):
            list_one.append(str(i))
        return list_one

    # 判断字符在列表中
    def str_in_list_index(self, str, view_list):
        index = 0
        for i in range(len(view_list)):
            if str in view_list[i]:
                index = i
        return index

    # 判断列表中的字符串都在字符串中
    def list_in_str(self, str_list, str):
        for i in range(len(str_list)):
            if not str_list[i] in str:
                self.info("文案 <{}> 不在标题 <{}> 中 ".format(str_list[i],str))
                assert str_list[i] in str

    # 判断两个列表相同
    def list_is_same(self, list_one, list_two):
        is_same_one = [x for x in list_one if x not in list_two]
        is_same_two = [x for x in list_two if x not in list_one]
        assert len(is_same_one) == len(is_same_two) == 0

    # 判断两个列表的相似度
    def list_similarity(self, this_list, other_list):
        """检查两个列表的相似度"""
        same_all = [x for x in this_list if x in other_list]  # 都存在的元素
        different_all = [y for y in (this_list + other_list) if y not in same_all]  # 都不存在的元素
        this_different = [x for x in this_list if x not in other_list]  # 只在之前页面存在
        other_different = [y for y in other_list if y not in this_list]  # 只在之后页面存在
        same_all_count = len(same_all)  # 相同元素的个数
        different_all_count = len(different_all)  # 不相同元素的个数
        # 相似度
        self.info('---same_al22l_count--')
        self.info(same_all_count)
        self.info(different_all_count)
        similarity = float(same_all_count) / (same_all_count + different_all_count)
        return round(similarity, 3)

    # 判断两个text不相等
    def is_different_text(self, text_one, text_two):
        assert len(text_one) > 0 and len(text_two) > 0
        assert text_one != text_two

    # 把一个列表倒叙输出
    def list_reversed(self, content_list):
        return list(reversed(content_list))

    # 字符串是整数
    def str_is_int(self, text):
        self.info('--str_is_int--')
        self.info(text)
        assert text.isdigit()

    # 字符串是整数
    def str_is_int_bl(self, text):
        self.info('--str_is_int--')
        self.info(text)
        if text.isdigit():
            return True
        else:
            return False

    # 通过字符串拆分一个数组为多个数组,获取第N段
    def str_in_list_cut_more_list(self, content_list, cut_str, num=None):
        from itertools import groupby
        result = [list(g) for k, g in groupby(content_list, lambda x: x == cut_str) if not k]
        # 去掉空元素
        result = [i for i in result if i != '']
        if num != None:  # 如果传入段数就获取第N段
            return result[num - 1]
        else:
            return result

    #列表去重 【排序不变】
    def list_remove_repeat(self,remove_list):
        result_list=[]
        for i, v in enumerate(remove_list):
            if remove_list.index(v) == i:
                result_list.append(v)
        return result_list

    """计数算法"""

    def random_phone_number(self):
        """获取随机的电话号码，1+时间戳共11位"""
        return "1" + str(int(time.time()))

    # 随机出数
    def random(self, num):
        """random  引用有bug No module named path"""
        import random
        return str(random.randint(0, num))

    # 传入整形字符串+1
    def str_add_one(self, text):
        return str(int(text) + 1)

    # 传入整形字符串-1
    def str_minus_one(self, text):
        return str(int(text) - 1)

    """时间算法"""

    def case_time(self):
        """获取用例时间"""
        return str(datetime.datetime.now().strftime('%m-%d_%H:%M:%S'))

    def get_time_time(self):
        return int(time.time())

    def minutes_to_seconds(self, time_now):
        """时间转数字"""
        minute = time_now.rsplit(":")[0]
        second = time_now.rsplit(":")[1]
        return int(minute) * 60 + int(second)

    def int_to_time_minute_second(self, time_int):
        """数字转时间"""
        m, s = divmod(time_int, 60)
        time = "%02d:%02d" % (m, s)
        return time

    # 一个时间包含在另一个时间中
    def time_in_time(self, one_time, all_time):
        # 例子 00:03 in 00：29  3秒钟的时间包含在 29秒钟
        self.info('---time_in_time---')
        self.info(one_time)
        self.info(all_time)
        one_time_second = self.minutes_to_seconds(one_time)
        all_time_second = self.minutes_to_seconds(all_time)
        assert all_time_second >= one_time_second

    def time_in_time_to_times(self, one_time, start_time, end_time):
        self.info('---time_in_time_to_times---')
        self.info(start_time)
        self.info(one_time)
        self.info(end_time)
        start_time_second = self.minutes_to_seconds(start_time)
        one_time_second = self.minutes_to_seconds(one_time)
        end_time_second = self.minutes_to_seconds(end_time)
        self.info(start_time_second)
        self.info(one_time_second)
        self.info(end_time_second)
        assert start_time_second <= one_time_second <= end_time_second

    def get_now_time_add_second_list(self, num):
        time_type = "%Y-%m-%d %H:%M:%S"
        time_list = []
        import datetime
        now_time = datetime.datetime.now()
        for i in range(num):
            time_list.append((now_time + datetime.timedelta(seconds=+i)).strftime(time_type))
        return time_list

    # 判断日期列表是倒序排序
    def date_sequence_down(self, date_list):
        from datetime import datetime
        format_pattern = '%m-%d'
        for i in range(len(date_list)):
            if i == len(date_list) - 1:
                return
            difference = (datetime.strptime(date_list[i], format_pattern) - datetime.strptime(date_list[i + 1],
                                                                                              format_pattern))
            # 倒序，上一个的时间大于等于下一个的时间。
            if difference.days >= 0:
                self.info('------shijiandaoxu----')
                self.info(date_list[i])
                self.info(date_list[i + 1])
                assert True
            else:
                assert '错误' == '时间排序错误,没有倒序排序'

    # 获取上个月
    def get_last_month_cn(self):
        """获取当前月份的第一天"""
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        if month > 1 and month < 10:
            month = month - 1
            month = "0{}".format(month)
        # 如果是1月份就返回是上一年的12月
        if month == 1:
            month = "12"
            year = year - 1
        return "{}年{}月".format(year, month)

    # 获取当前时间 小时：分：秒
    def get_time_year_to_second(self):
        return self.get_now_time("%Y-%m-%d %H:%M:%S")

    # 获取当前时间 小时：分：秒
    def get_time_year_to_minute(self):
        return self.get_now_time("%Y-%m-%d %H:%M")

    # 获取当前时间汉字 小时：分：秒
    def get_time_year_to_second_cn(self):
        return self.get_now_time("%Y年%m月%d日 %H:%M:%S")

    # 获取当前时间汉字 小时：分：秒
    def get_time_year_to_minute_cn(self):
        return self.get_now_time("%Y年%m月%d日 %H:%M")

    # 获取当前时间汉字
    def get_time_year_to_month_cn(self):
        return self.get_now_time("%Y年%m月")

    # 获取上个月时间
    def get_time_year_to_month_last_month_cn(self):
        today = datetime.date.today()
        first = today.replace(day=1)
        last_month = first - datetime.timedelta(days=1)
        return last_month.strftime("%Y年%m月")

    # 获取当前时间 小时：分：秒
    def get_time_hour_and_minute_second(self):
        return self.get_now_time("%H:%M:%S")

    # 获取当前时间 小时：分：秒
    def get_time_year_to_second(self):
        return self.get_now_time("%Y-%m-%d %H:%M:%S")

    # 获取当前时间
    def get_time_hour_and_minute(self):
        return self.get_now_time("%H:%M")

    def get_now_time(self, formate):
        """
        %Y-%m-%d %H:%M:%S 格式化成2016-03-20 11:45:39形式
        %a %b %d %H:%M:%S %Y 格式化成Sat Mar 28 22:24:24 2016形式
        """
        now_time = time.strftime(formate, time.localtime())
        return now_time

    # 终端命令
    def shell_back(self, shell_content):
        return os.popen(shell_content).readlines()

    def info(self, text):
        """打印日志"""
        try:
            self.driver.info("<" + str(text) + ">")
        except:
            print("<" + str(text) + ">")

    def info_list(self, content_list):
        """打印列表内容的日志"""
        try:
            for i in range(len(content_list)):
                self.driver.info("<" + str(content_list[i]) + ">")
        except:
            for i in range(len(content_list)):
                print("<" + str(content_list[i]) + ">")

    def info_list_len(self, content_list):
        """打印列表内容的日志"""
        try:
            for i in range(len(content_list)):
                self.driver.info("<{}>".format(content_list[i]))
            self.driver.info(len(content_list))
        except:
            for i in range(len(content_list)):
                print("<{}>".format(content_list[i]))
            print(len(content_list))

    def sleep(self, times):
        """睡眠"""
        time.sleep(times)
