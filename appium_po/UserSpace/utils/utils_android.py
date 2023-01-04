# encoding=utf-8
import uiautomator2 as u2
import time, re, sys, importlib
from appium_po.UserSpace.utils.utils_base import UtilsBase
# from airtest.core.api import *

importlib.reload(sys)

# 项目路径
project_path = '/Users/liujiang/C/Deyes_C/'
# 包名

pageage_name = None
pageage_name_id = None
phone_height = 0
phone_width = 0

# 缓存数据
device_id = ''
# device_id
XiaoMiMix2 = 'fab8bf23'

"""手机适配相关"""
# 手机y坐标点击系数。 正常是0.5 小于0.5向上点击 大于0.5向下点击
OPPOFind7 = 'ced50f61'
click_phone_list_add_args_y = {OPPOFind7: 0.4}  # 0ppoFind7手机 Y坐标按系数增加
click_phone_list_add_num_y = {OPPOFind7: 50}  # 0ppoFind7手机坐标按照 帧率增加


class UtilsAndroid(UtilsBase):
    search_one = 0.1  # 搜索等待时长
    search_two = 0.2  # 搜索等待时长
    search_short = 0.3  # 搜索等待时长
    search_short_five = 0.6  # 搜索等待时长
    search_one_second = 1.0  # 搜索等待时长
    search_three_time = 2.5  # 搜索等待时长
    search_long_time = 5  # 搜索等待时长
    show_time_out = 5  # id 显示时长 （秒）
    show_time_out_long = 15  # id 显示时长 （秒）
    show_time_out_so_long = 30  # id 显示时长 （秒）

    def __init__(self, driver):
        self.driver = driver

    """驱动相关"""

    # 获取uiautomator2驱动
    def get_uiautomator_driver(self):
        return u2.connect_usb(self.get_devices_id())

    # # 初始化airtest
    # def get_airtest_driver(self):
    #     connect_device("Android:///")

    """airtest"""

    def air_click_img(self, img):
        self.air_click_img_times(img, 3)

    # def air_click_img_times(self, img, times):
    #     self.get_airtest_driver()
    #     pos = loop_find(Template(img), timeout=times)
    #     G.DEVICE.touch(pos)

    """手机适配相关"""

    def save_android_pageage_name(self, name):
        global pageage_name, pageage_name_id
        pageage_name = name
        pageage_name_id = "{}:id/".format(pageage_name)

    def get_android_pageage_name(self):
        return pageage_name

    # def get_phone_click_y(self, args_y):
    #     if self.get_devices_id() in click_phone_list_add_args_y.keys():
    #         # Y纵向增加百分比
    #         return args_y + args_y * click_phone_list_add_args_y[self.get_devices_id()]
    #     else:
    #         return args_y

    def get_phone_click_add_y(self, num_y):
        if self.get_devices_id() in click_phone_list_add_num_y.keys():
            add_y = num_y + click_phone_list_add_num_y[self.get_devices_id()]
            self.info('---add_y---')
            self.info(num_y)
            self.info(add_y)
            # Y纵向增加百分比
            return add_y
        else:
            return num_y

    """基础"""

    # 获取deviceId
    def get_devices_id(self):
        global device_id
        if len(device_id) == 0:
            device_id = self.driver.deviceId
        return device_id

    # 获取手机高
    def get_height(self):
        """uiautomator2"""
        global phone_height
        if phone_height != 0:
            # Utils(self.driver).info('---yiyou-height---')
            # Utils(self.driver).info(phone_height)
            return phone_height
        else:
            d = self.get_uiautomator_driver()
            # Utils(self.driver).info('---wu-height---')
            phone_height = d.info['displayHeight']
            # Utils(self.driver).info(phone_height)
            return phone_height

    # 获取手机高
    def get_width(self):
        """uiautomator2"""
        global phone_width
        if phone_width != 0:
            # Utils(self.driver).info('---yiyou-width---')
            # Utils(self.driver).info(phone_width)
            return phone_width
        else:
            d = self.get_uiautomator_driver()
            # Utils(self.driver).info('---wu-width---')
            phone_width = d.info['displayWidth']
            # Utils(self.driver).info(phone_width)
            return phone_width

    def clear_app(self):
        """清除数据"""
        d = self.get_uiautomator_driver()
        d.app_clear(pageage_name)

    def android_kill_app(self):
        d = self.get_uiautomator_driver()
        d.app_stop(pageage_name)

    def back(self):
        """点击手机返回按钮"""
        d = self.get_uiautomator_driver()
        d.press("back")

    def screen_on(self):
        """点亮屏幕"""
        d = self.get_uiautomator_driver()
        d.screen_on()

    # 打开手机通知栏
    def open_notification(self):
        d = self.get_uiautomator_driver()
        d.open_notification()

    def get_id(self, id):
        """加工传入的id"""
        # 如果传入的id中含有'/' 应该是原生id，就不需要加包名了
        if type(id) == str:
            if '/' in id:
                return id
            else:
                return pageage_name_id + id
        list = []
        if type(id) == tuple:
            for i in range(len(id)):
                if '/' in id[i]:
                    list.append(id[i])
                    continue
                else:
                    list.append(pageage_name_id + id[i])
        return list

    """二次封装"""

    def not_show_id(self, *id):
        """uiautomator2"""
        # d = self.get_uiautomator_driver()
        # for i in range(len(id)):
        #     id = self.get_id(id[i])
        #     Utils(self.driver).info(id)
        #     assert not d(resourceId=str(id)).exists
        self.not_show_id_time_args(self.search_three_time, *id)

    def not_show_id_short(self, *id):
        """uiautomator2"""
        self.not_show_id_time_args(self.search_one, *id)

    # 不显示文案,传入超时参数
    def not_show_id_time_args(self, time_out, *id):
        """deyes"""
        # self.driver.assertNotExists(text=text)
        """uiautomator2"""
        # deyes 不显示文案功能无法实现
        d = self.get_uiautomator_driver()
        for i in range(len(id)):
            id = self.get_id(id[i])
            for l in range(int(time_out * 10)):
                if d(resourceId=str(id)).exists:
                    self.sleep(0.1)
                else:
                    break
            assert not d(resourceId=str(id)).exists

    # 显示id,传入单个参数
    def show_id(self, *id):
        # 页面多个重复的id时show_id校验会报错
        # id = self.get_id(id)
        # if type(id) == str:  # 如果只是1个id 就等待id的出现
        #     self.driver.wait(resourceId=id)
        # else:  # 如果不是1个id 就等待第一个id的出现
        #     self.driver.wait(resourceId=id[0]) # 有时候wait方法不好用
        #     self.driver_assertExistsXpathsId(id)
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        if type(id) == str:  # 如果是1个id 直接校验
            self.info(id)
            assert d(resourceId=id).wait(timeout=self.show_time_out)
        else:  # 如果是一组id 遍历校验
            for i in range(len(id)):
                self.info(id[i])
                assert d(resourceId=id[i]).wait(timeout=self.show_time_out)
                # 如果id显示就校验。如果id不显示就抓取xml再次校验
                # if d(resourceId=id[i]).wait(timeout=self.show_time_out):
                #     return
                # else:
                #     self.show_xml_id(id[i])

    # 显示文案中的某一个即可
    def show_any_id(self, *id):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        for i in range(len(id)):
            if i == 0:
                timeout = 2.0
            else:
                timeout = 0.1
            if d(resourceId=id[i]).wait(timeout=timeout):
                self.info(id[i])
                return
        assert '错误' == 'any字符串都不正确 {}'.format(*id)

    def show_xml_id(self, id):
        """通过获取页面布局判断id是否存在"""
        xml = self.get_xml()
        id = self.get_id(id)
        xpath = 'resource-id="%s"' % id
        self.info('---xpath_id---')
        self.info(xpath)
        assert xpath in xml

    # 显示 id 和对应的 text
    def show_id_text(self, ids, text):
        id = self.get_id(ids)
        self.info('{} -- {}'.format(id, text))
        for l in range(10):
            all = str(self.get_xml()).rsplit('\n')
            for i in range(len(all)):
                if 'text="{}"'.format(text) in all[i] and 'resource-id="{}"'.format(id) in all[i]:
                    return
        # 判断成功
        assert '错误' == '找不到对应的 id{} 和 text{}'.format(ids, text)

    # 显示 id 和对应的 text含有字段
    def show_id_str_in_text(self, ids, text):
        id = self.get_id(ids)
        self.info('{} -- {}'.format(id, text))
        for l in range(10):
            all = str(self.get_xml()).rsplit('\n')
            for i in range(len(all)):
                if 'text=' in all[i] and 'resource-id="{}"'.format(id) in all[i]:
                    # 获取文案
                    all_text = str(re.findall(r'text=["\'](.*?)["\']', all[i])[0])
                    if text in all_text:
                        self.info('--text_in_all_text--')
                        self.info(text)
                        self.info(all_text)
                        return
        # 判断成功
        assert '错误' == '找不到对应的 id{} 中含有文案text{}'.format(ids, text)

    # 显示文案，传入单个参数
    def show_text(self, *text):
        self.show_text_time_args(self.show_time_out, *text)

    # 显示文案，传入单个参数
    def show_text_long_time(self, *text):
        self.show_text_time_args(self.show_time_out_long, *text)

    # 显示文案，传入单个参数
    def show_text_so_long_time(self, *text):
        self.show_text_time_args(self.show_time_out_so_long, *text)

    # 显示文案，传入单个参数,和超时时间
    def show_text_time_args(self, time_out, *text_or_desc):
        # self.driver.wait(text=text[0])
        # self.driver_assertExistsXpathsText(*text)
        """uiautomator2"""
        # d = self.get_uiautomator_driver()
        # 获取当前页面所有text和desc内容
        text_or_desc_list = self.get_xml_args_dict('text-desc')
        # self.info('--text_or_desc_list--')
        # self.info_list(text_or_desc_list)
        for i in range(len(text_or_desc)):
            # if type(text_or_desc[i]) == str or type(text_or_desc[i]) == unicode:  # 如果是1个id 直接校验
            if type(text_or_desc[i]) == str:  # 如果是1个id 直接校验
                self.info(text_or_desc[i])
                text_or_desc_list = self.show_text_or_desc_wait(text_or_desc[i], text_or_desc_list, time_out)
                # assert d(text=text_or_desc[i]).wait(timeout=time_out)
            elif type(text_or_desc[i]) == list:  # 如果是一组text 遍历校验
                for l in range(len(text_or_desc[i])):
                    self.info(text_or_desc[i][l])
                    text_or_desc_list = self.show_text_or_desc_wait(text_or_desc[i][l], text_or_desc_list,
                                                                    time_out)
                    # assert d(text=text_or_desc[i][l]).wait(timeout=time_out)
            else:
                self.info(text_or_desc[i])
                self.info(type(text_or_desc[i]))
                assert '错误' == 'show_text_传入的是未知的类型'

    # def show_text_or_desc(self,text_or_desc):
    # Utils(self.driver).info(text_or_desc)
    # text_or_desc_list = self.get_xml_args_dict('text-desc')
    # self.show_text_or_desc_wait(text_or_desc,text_or_desc_list,self.search_short_five)

    # 检查text_or_desc显示并传入等待超时时间
    def show_text_or_desc_wait(self, text_or_desc, text_or_desc_list, time_out):
        # time_out * 2  一次搜索大约0.5秒
        for i in range(int(time_out * 2)):
            if self.text_or_desc_in_list_boolean(text_or_desc, text_or_desc_list):
                return text_or_desc_list
            else:
                self.sleep(0.01)
                # 如果找不到就重新获取界面text_or_desc再次验证
                text_or_desc_list = self.get_xml_args_dict('text-desc')
        assert '错误' == 'show_text_or_desc没有找到对应的内容'.format(text_or_desc)

    # 检查text_or_desc 是否在 list中 如果在就返回Ture 否则返回 False
    def text_or_desc_in_list_boolean(self, text_or_desc, text_or_desc_list):
        for i in range(len(text_or_desc_list)):
            if text_or_desc == text_or_desc_list[i]:
                return True
        if '\n' in text_or_desc:
            # 兼容 &#10; 转\n 情况
            for i in range(len(text_or_desc_list)):
                if '&#10;' in text_or_desc_list[i]:
                    new_text = text_or_desc_list[i].replace('&#10;', '\n')
                    # Utils(self.driver).info('--&#10;--')
                    # Utils(self.driver).info(text_or_desc_list[i])
                    # Utils(self.driver).info(new_text)
                    if text_or_desc == new_text:
                        return True
        elif '&#10;' in text_or_desc:
            # 兼容 \n转&#10;  情况
            for i in range(len(text_or_desc_list)):
                if '\n' in text_or_desc_list[i]:
                    new_text = text_or_desc_list[i].replace('\n', '&#10;')
                    # Utils(self.driver).info('--huiche_huanhang--')
                    # Utils(self.driver).info(text_or_desc_list[i])
                    # Utils(self.driver).info(new_text)
                    if text_or_desc == new_text:
                        return True
        return False

    def xpath_text_or_desc_boolean(self, text_or_desc, return_bounds=False):
        text_or_desc_bounds = self.get_xml_args_dict('text-desc-bounds', time_out=0.1)
        # self.info('--text_or_desc_bounds--')
        # self.info_list(text_or_desc_bounds)
        for i in range(len(text_or_desc_bounds)):
            if text_or_desc == self.cut_size(text_or_desc_bounds[i]):
                if return_bounds:
                    return True, text_or_desc_bounds[i]
                else:
                    return True
        if '\n' in text_or_desc:
            # 兼容 &#10; 转\n 情况
            for i in range(len(text_or_desc_bounds)):
                if '&#10;' in text_or_desc_bounds[i]:
                    new_text = self.cut_size(text_or_desc_bounds[i].replace('&#10;', '\n'))
                    if text_or_desc == new_text:
                        if return_bounds:
                            return True, text_or_desc_bounds[i]
                        else:
                            return True
        elif '&#10;' in text_or_desc:
            # 兼容 \n转&#10;  情况
            for i in range(len(text_or_desc_bounds)):
                if '\n' in text_or_desc_bounds[i]:
                    new_text = self.cut_size(text_or_desc_bounds[i].replace('\n', '&#10;'))
                    if text_or_desc == new_text:
                        if text_or_desc == new_text:
                            if return_bounds:
                                return True, text_or_desc_bounds[i]
                            else:
                                return True
        if return_bounds:
            return False, ''
        else:
            return False

        # """uiautomator2"""
        # d = self.get_uiautomator_driver()
        # for i in range(len(desc)):
        #     if type(desc[i]) == str or type(desc[i]) == unicode:  # 如果是1个id 直接校验
        #         Utils(self.driver).info(desc[i])
        #         assert d.xpath("//*[@content-desc='{}']".format(desc[i])).wait(timeout=time_out)
        #     elif type(desc[i]) == list:  # 如果是一组text 遍历校验
        #         for l in range(len(desc[i])):
        #             Utils(self.driver).info(desc[i][l])
        #             assert d.xpath("//*[@content-desc='{}']".format(desc[i][l])).wait(timeout=time_out)
        #     else:
        #         Utils(self.driver).info(desc[i])
        #         Utils(self.driver).info(type(desc[i]))
        #         assert '错误' == 'show_desc_传入的是未知的类型'

    # 字符串中含有对应的内容
    def show_str_list_in_text(self, list_text):
        self.info('--show_str_in_text_list--')
        self.info_list(list_text)
        for i in range(int(self.search_short_five * 10)):
            result_list = []
            text_bounds = self.get_xml_args_dict('text-bounds')
            for i in range(len(text_bounds)):
                result_list_has = 0
                for l in range(len(list_text)):
                    if list_text[l] in text_bounds[i]:
                        result_list_has += 1
                if result_list_has == len(list_text):
                    result_list.append(self.cut_size(text_bounds[i]))
            if len(result_list) > 0:
                break
        self.info('--show_str_in_text--')
        self.info(len(result_list))
        self.info_list(result_list)
        assert len(result_list) > 0

    # 显示文案中的某一个即可，3秒循环
    def show_any_just_text_short(self, *text):
        self.show_any_just_text_args(1, 1, *text)

    # 显示文案中的某一个即可，3秒循环
    def show_any_just_text(self, *text):
        self.show_any_just_text_args(1, 3, *text)

    # 显示文案中的某一个即可，15秒循环遍历
    def show_any_just_text_long_time(self, *text):
        self.show_any_just_text_args(5, 3, *text)

    # 显示文案中的某一个即可
    def show_any_just_text_args(self, num, time, *text):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        for i in range(num):
            for i in range(len(text)):
                if i == 0:
                    timeout = time
                else:
                    timeout = 0.1
                # if type(text[i]) == str or type(text[i]) == unicode:  # 如果是1个id 直接校验
                if type(text[i]) == str:  # 如果是1个id 直接校验
                    if d(text=text[i]).wait(timeout=timeout):
                        self.info(text[i])
                        return
                elif type(text[i]) == list:  # 如果是一组text 遍历校验:
                    for l in range(len(text[i])):
                        if d(text=text[i][l]).wait(timeout=timeout):
                            self.info(text[i][l])
                            return
                else:
                    self.info(text[i])
                    assert '错误' == '传入的是未知类型'
        assert '错误' == 'any字符串都不正确 {}'.format(*text)

    # 显示文案中的某一个即可，3秒循环
    def show_any_text_short(self, *text):
        self.show_any_text_args(1, 1, *text)

    # 显示文案中的某一个即可，3秒循环
    def show_any_text(self, *text):
        self.show_any_text_args(1, 3, *text)

    # 显示文案中的某一个即可，6秒循环遍历
    def show_any_text_two_time(self, *text):
        self.show_any_text_args(2, 3, *text)

    # 显示文案中的某一个即可，15秒循环遍历
    def show_any_text_long_time(self, *text):
        self.show_any_text_args(5, 3, *text)

    # 显示文案中的某一个即可
    def show_any_text_args(self, num, time, *text):
        """uiautomator2"""
        # d = self.get_uiautomator_driver()
        for i in range(num):
            for i in range(len(text)):
                # if type(text[i]) == str or type(text[i]) == unicode:  # 如果是1个id 直接校验
                if type(text[i]) == str:  # 如果是1个id 直接校验
                    if self.search_text_one(text[i]):
                        self.info(text[i])
                        return
                elif type(text[i]) == list:  # 如果是一组text 遍历校验:
                    for l in range(len(text[i])):
                        if self.search_text_one(text[i][l]):
                            self.info(text[i][l])
                            return
                else:
                    self.info(text[i])
                    assert '错误' == '传入的是未知类型'
        assert '错误' == 'any字符串都不正确 {}'.format(*text)

    # 检查页面存在正则表达式对应的文字
    def show_re_text(self, re_pattern):
        return self.show_re_text_class_name(re_pattern, 'android.widget.TextView')

    # 检查页面存在正则表达式对应的文字
    def show_re_img_text(self, re_pattern):
        return self.show_re_text_class_name(re_pattern, 'android.widget.ImageView')

    # 检查页面存在正则表达式对应的文字
    def show_re_view_text(self, re_pattern):
        return self.show_re_text_class_name(re_pattern, 'android.view.View')

    # 检查页面存在正则表达式对应的文字
    def show_re_text_or_desc(self, re_pattern):
        return self.show_re_text_class_name(re_pattern, 'text-desc')

    # 检查页面有对应的view的文案
    def show_view_text(self, text):
        self.info('--show_view_text--')
        self.info(text)
        get_text_list = self.get_xml_args_dict('android.view.View')
        self.info('--get_text_list--')
        self.info_list(get_text_list)
        for i in range(len(get_text_list)):
            if text == get_text_list[i]:
                return
        assert '错误' == '页面中的android.view.View中没有对应的文案{}'.format(text)

    # 检查页面存在正则表达式对应的文字,传入获取参数
    def show_re_text_class_name(self, re_pattern, class_name):
        text_list = []
        for i in range(int(self.search_short_five * 10)):
            # 获取页面所有文案
            get_text_list = self.get_xml_args_dict(class_name)
            # Utils(self.driver).info('-----all-xml---')
            # Utils(self.driver).info(class_name)
            # Utils(self.driver).info_list(get_text_list)
            # Utils(self.driver).info('-----all-xml-end---')
            for i in range(len(get_text_list)):
                # 待匹配的字符串转为unicode类型
                # u_text = unicode(get_text_list[i], "utf-8")
                u_text = get_text_list[i]
                # 判断是否符合正则表达式
                if self.re_match(re_pattern, u_text):
                    text_list.append(get_text_list[i])
            # 如果有匹配的正则就退出，没有就等0.1秒重新采集校验
            if len(text_list) != 0:
                self.info('----zengze-show---')
                self.info_list(text_list)
                return text_list
            else:
                self.sleep(0.1)
        assert '错误' == '没有匹配的正则的字符串'.format(re_pattern)

    # 显示文案，传入单个参数
    def show_only_text(self, text):
        d = self.get_uiautomator_driver()
        d(text=text).wait(timeout=5.0)

    def show_text_ui(self, text):
        d = self.get_uiautomator_driver()
        assert d(text=text).exists

    # 不显示文案
    def not_show_text(self, *text):
        self.not_show_text_time_args(self.search_three_time, *text)

    # 不显示文案
    def not_show_text_so_short_time(self, *text):
        self.not_show_text_time_args(self.search_one, *text)

    # 不显示文案
    def not_show_text_short_time(self, *text):
        self.not_show_text_time_args(self.search_short_five, *text)

    # 不显示文案
    def not_show_text_long_time(self, *text):
        self.not_show_text_time_args(self.show_time_out, *text)

    # 不显示文案,传入超时参数
    def not_show_text_time_args(self, time_out, *text):
        """deyes"""
        # self.driver.assertNotExists(text=text)
        """uiautomator2"""
        # deyes 不显示文案功能无法实现
        d = self.get_uiautomator_driver()
        for i in range(len(text)):
            # Utils(self.driver).info('----not_show--')
            # Utils(self.driver).info(text[i])
            # if type(text[i]) == str or type(text[i]) == unicode:
            if type(text[i]) == str:
                # Utils(self.driver).info('----not_show_str--')
                self.info(text[i])
                for l in range(int(time_out * 10)):
                    if d(text=text[i]).exists:
                        self.sleep(0.1)
                    else:
                        break
                assert not d(text=text[i]).exists
            elif type(text[i]) == list:
                for n in range(len(text[i])):
                    # Utils(self.driver).info('----not_show_str_list--')
                    self.info(text[i][n])
                    for l in range(int(time_out * 10)):
                        if d(text=text[i][n]).exists:
                            self.sleep(0.1)
                        else:
                            break
                    assert not d(text=text[i][n]).exists
            else:
                assert '错误' == 'not_show_text_传入的是未知的类型'

    # 不显示文案
    def not_show_desc(self, *desc):
        self.not_show_desc_time_args(self.search_short_five, *desc)

    # 不显示文案,传入超时参数
    def not_show_desc_time_args(self, time_out, *desc):
        """deyes"""
        # self.driver.assertNotExists(text=text)
        """uiautomator2"""
        # deyes 不显示文案功能无法实现
        d = self.get_uiautomator_driver()
        for i in range(len(desc)):
            # Utils(self.driver).info('----not_show--')
            # Utils(self.driver).info(text[i])
            # if type(desc[i]) == str or type(desc[i]) == unicode:
            if type(desc[i]) == str:
                # Utils(self.driver).info('----not_show_str--')
                self.info(desc[i])
                for l in range(int(time_out * 10)):
                    if d(description=desc[i]).exists:
                        self.sleep(0.1)
                    else:
                        break
                assert not d(description=desc[i]).exists
            elif type(desc[i]) == list:
                for n in range(len(desc[i])):
                    # Utils(self.driver).info('----not_show_str_list--')
                    self.info(desc[i][n])
                    for l in range(int(time_out * 10)):
                        if d(description=desc[i][n]).exists:
                            self.sleep(0.1)
                        else:
                            break
                    assert not d(description=desc[i][n]).exists
            else:
                assert '错误' == 'not_show_desc_传入的是未知的类型'

    # 不显示对应属性的文案，文案和坐标完全一致
    def not_show_text_info(self, text_info):
        """deyes"""
        # self.driver.assertNotExists(text=text)
        """uiautomator2"""
        # deyes 不显示文案功能无法实现
        d = self.get_uiautomator_driver()
        assert not d(text=text_info).exists

    # 显示文案,传入列表参数
    def show_text_list(self, test_list):
        # self.driver.wait(text=test_list[0])
        # self.driver_assertExistsXpathsList(test_list)
        # 当 一个页面出现两个相同的text时，该方法会报错
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        assert d(text=test_list[0]).wait(timeout=self.show_time_out)
        for i in range(len(test_list)):
            self.info(test_list[i])
            assert d(text=test_list[i]).exists

    def show_package(self, package):
        d = self.get_uiautomator_driver()
        self.info(package)
        assert d(packageName=package).wait(timeout=self.search_three_time)

    def show_class_name(self, class_name):
        d = self.get_uiautomator_driver()
        self.info(class_name)
        assert d(className=class_name).wait(timeout=self.show_time_out)

    def not_show_class_name(self, class_name):
        d = self.get_uiautomator_driver()
        assert not d(className=class_name).wait(timeout=self.search_short_five)

    def is_focusable_id(self, id):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        assert d(resourceId=id).info['focusable']

    def not_focusable_id(self, id):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        assert not d(resourceId=id).info['focusable']

    def is_focusable_text(self, text):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        assert d(text=text).info['focusable']

    def not_focusable_text(self, text):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        assert not d(text=text).info['focusable']

    # id是selected状态
    def is_selected_id(self, id):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        assert d(resourceId=id).info['selected']

    def not_selected_id(self, id):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        assert not d(resourceId=id).info['selected']

    # id是selected状态
    def is_selected_id_num(self, id, num):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        assert d(resourceId=id)[num].info['selected']

    # 所有id都是selected状态
    def is_selected_id_all(self, id):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        d(resourceId=id).wait(timeout=1.0)
        id_count = d(resourceId=id).count
        for i in range(id_count):
            assert d(resourceId=id)[i].info['selected']

    def is_selected_text(self, text, is_desc=False):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        if is_desc:
            assert d(description=text).info['selected']
        else:
            assert d(text=text).info['selected']

    # id是checked状态
    def is_checked_id(self, id):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        assert d(resourceId=id).info['checked']

    # id是checked状态
    def not_checked_id(self, id):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        assert not d(resourceId=id).info['checked']

    # id是checked状态
    def is_enabled_id(self, id):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        assert d(resourceId=id).info['enabled']

    # id不是checked状态
    def not_enabled_id(self, id):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        assert not d(resourceId=id).info['enabled']

    # text是checked状态
    def is_enabled_text(self, text, is_desc=False):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        if is_desc:
            assert d(description=text).info['enabled']
        else:
            assert d(text=text).info['enabled']

    # text是checked状态
    def is_enabled_desc(self, desc):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        assert d(text=desc).info['enabled']

    # text不是checked状态
    def not_enabled_text(self, text, is_desc=False):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        if is_desc:
            assert not d(description=text).info['enabled']
        else:
            assert not d(text=text).info['enabled']

    # id是checked状态
    def is_clickable_id(self, id):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        assert d(resourceId=id).info['clickable']

        # id不是checked状态

    def not_clickable_id(self, id):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        assert not d(resourceId=id).info['clickable']

        # text是checked状态

    def is_clickable_text(self, text, is_desc=False):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        if is_desc:
            assert d(description=text).info['clickable']
        else:
            assert d(text=text).info['clickable']

    # text不是checked状态
    def not_clickable_text(self, text, is_desc=False):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        if is_desc:
            assert not d(description=text).info['enabled']
        else:
            assert not d(text=text).info['clickable']

    # toast显示正确
    def show_toast(self, text):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        toast = d.toast.get_message(5.0, default="")
        self.info('---toast---')
        self.info(text)
        self.info(toast)
        # 判断toast 是否正确
        # toast_reslut = text in toast
        self.info(text in toast)
        assert text in toast

    # toast不显示
    def not_show_toast(self):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        assert not d.toast.get_message(2.0, default="")

    def two_toast_wait(self):
        self.sleep(10)

    """----------点击--------"""

    # 点击id
    def click(self, id):
        # id = self.get_id(id)
        # self.info(id)
        # self.driver.waitClick(resourceId=id)
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        self.info('--click_id-<{}>-'.format(id))
        d(resourceId=id).click()

    # 点击id
    def click_any_id(self, *id):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        self.info('--click_any_id--')
        if type(id) == str:  # 如果是1个id 直接校验
            if d(resourceId=id).wait(timeout=self.search_three_time):
                self.info(id)
                d(resourceId=id).click()
                return
        else:  # 如果是一组id 遍历校验
            for i in range(len(id)):
                self.info(id[i])
                if d(resourceId=id[i]).wait(timeout=self.search_three_time):
                    d(resourceId=id[i]).click()
                    return

    # 点击id的具体位置
    def click_offset(self, id, wide, high):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        self.info('--click_offset--')
        self.info(id)
        d(resourceId=id).wait(timeout=self.show_time_out)
        d(resourceId=id).click(offset=(wide, high))

    # 点击相同id的第N个
    def click_num(self, id, num):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        num = num - 1
        self.info('--click_num-<{}>_<{}>-'.format(id, num))
        d(resourceId=id)[num].wait(timeout=self.show_time_out)
        d(resourceId=id)[num].click()

    # 点击id uiautomator2方法
    def click_id_ui2(self, id):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        d(resourceId=id).click()

    def click_xy(self, left, top, right, bottom, wide, height):
        """uiautomator2"""
        left = int(left)
        top = int(top)
        right = int(right)
        bottom = int(bottom)
        d = self.get_uiautomator_driver()
        # 计算xy
        x = (left + (right - left) / 2.0) / wide * self.get_width()
        y = (top + (bottom - top) / 2.0) / height * self.get_height()
        # Utils(self.driver).info('xxxxxxxxxxxxxxx')
        # Utils(self.driver).info(x)
        # Utils(self.driver).info(y)
        d.click(x, y)

    def click_just_xy(self, x, y):
        """uiautomator2"""
        if x < 1:
            x = x * self.get_width()
        if y < 1:
            y = y * self.get_height()
        d = self.get_uiautomator_driver()
        d.click(x, y)

    def click_xy_bounds(self, bounds, args_x=0.5, args_y=0.5):
        # 手机适配Y的参数 个别手机Y需要下调
        # args_y = self.get_phone_click_y(args_y)
        # Utils(self.driver).info('---args_y--')
        # Utils(self.driver).info(args_y)
        x, y = self.get_left_top_right_down_xy(bounds, args_x, args_y)
        y = self.get_phone_click_add_y(y)  # 增加Y点击位置
        self.click_just_xy(x, y)

    def long_click_xy_bounds(self, bounds, args_x=0.5, args_y=0.5):
        # 手机适配Y的参数 个别手机Y需要下调
        # args_y = self.get_phone_click_y(args_y)
        # Utils(self.driver).info('---args_y--')
        # Utils(self.driver).info(args_y)
        x, y = self.get_left_top_right_down_xy(bounds, args_x, args_y)
        y = self.get_phone_click_add_y(y)  # 增加Y点击位置
        self.swipe_args(x, y, x, y)

    def click_class_name(self, class_name):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        d(className=class_name).click()

    def click_desc(self, desc, wide=0.5, high=0.5):
        d = self.get_uiautomator_driver()
        self.info(desc)
        d(description=desc).click(offset=(wide, high))

    # 点击文案
    def click_just_text(self, text):
        # self.driver.waitClick(text=text)
        # 正文页已经收藏后，点击取消收藏文案无效
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        self.info(text)
        d(text=text).wait(timeout=self.show_time_out)
        d(text=text).click()

    def click_just_any_text(self, *text):
        d = self.get_uiautomator_driver()
        if type(text) == str:  # 如果是1个id 直接校验
            if d(text=text).wait(timeout=self.show_time_out):
                self.info(text)
                d(text=text).click()
                return
        else:  # 如果是一组id 遍历校验
            for i in range(len(text)):
                self.info(text[i])
                if d(text=text[i]).wait(timeout=self.show_time_out):
                    self.info(text[i])
                    d(text=text[i]).click()
                    return

    # 点击文案
    def click_text(self, text_or_desc, agrs_x=0.5, agrs_y=0.5):
        # self.driver.waitClick(text=text)
        # 正文页已经收藏后，点击取消收藏文案无效
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        self.info('--click_text_or_desc--')
        self.info(text_or_desc)
        # 兼容text和desc
        bl, bounds = self.search_text_or_desc_times(text_or_desc, self.search_short_five, True)
        if bl:
            self.click_xy_bounds(bounds, agrs_x, agrs_y)
            return
        assert '错误' == '没找到对应的desc文案 {}'.format(text_or_desc)

    # 点击文案的具体位置
    def click_text_offset(self, text, wide, high):
        # self.driver.waitClick(text=text)
        # 正文页已经收藏后，点击取消收藏文案无效
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        d(text=text).wait(timeout=self.show_time_out)
        d(text=text).click(offset=(wide, high))

    # 点击相同文案的第N个
    def click_text_num(self, text, num):
        # self.driver.waitClick(text=text)
        # 正文页已经收藏后，点击取消收藏文案无效
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        d(text=text).wait(timeout=self.show_time_out)
        d(text=text)[num - 1].click()

    # 点击正则匹配出来的第一个文案
    def click_re_text(self, re_pattern):
        return self.click_re_text_num(re_pattern, 0, 'text-desc')

    # 点击字符串中含有对应的内容
    def click_str_list_in_text(self, list_text, num=-1):
        self.info('--click_str_in_text_list--')
        self.info_list(list_text)
        result_list = []
        for i in range(int(self.search_short_five * 10)):
            result_list.clear()
            text_bounds = self.get_xml_args_dict('text-desc')
            for i in range(len(text_bounds)):
                result_list_has = 0
                for l in range(len(list_text)):
                    if list_text[l] in text_bounds[i]:
                        result_list_has += 1
                if result_list_has == len(list_text):
                    result_list.append(self.cut_size(text_bounds[i]))
            if len(result_list) > 0:
                break
        self.info('--click_str_in_text--')
        self.info(len(result_list))
        self.info_list(result_list)
        assert len(result_list) > 0
        if num == -1:
            self.click_text(result_list[0])
        else:
            self.click_text(result_list[num - 1])

    # 点击正则匹配出来的第N个文案
    def click_re_text_num(self, re_pattern, num, class_name):
        text_list = []
        for i in range(int(self.search_short_five * 10)):
            # 获取页面所有文案
            get_text_list = self.get_xml_args_dict(class_name)
            for i in range(len(get_text_list)):
                # 待匹配的字符串转为unicode类型
                # u_text = unicode(get_text_list[i], "utf-8")
                u_text = get_text_list[i]
                # 判断是否符合正则表达式
                if self.re_match(re_pattern, u_text):
                    text_list.append(get_text_list[i])
            # 如果有匹配的正则就退出，没有就等0.1秒重新采集校验
            if len(text_list) != 0:
                self.info('----zengze-click---')
                self.info(text_list[num])
                self.click_text(text_list[num])
                return text_list[num]
            else:
                self.sleep(0.1)
        assert '错误' == '没有匹配的正则的字符串'.format(re_pattern)

    # 点击文案中的某一个即可
    def click_any_text(self, *text_or_desc):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        for i in range(len(text_or_desc)):
            if i == 0:
                timeout = 3.0
            else:
                timeout = 0.1
            # if type(text_or_desc[i]) == str or type(text_or_desc[i]) == unicode:  # 如果是1个id 直接校验
            if type(text_or_desc[i]) == str:  # 如果是1个id 直接校验
                # 兼容text和desc
                bl, bounds = self.search_text_or_desc_times(text_or_desc[i], self.search_short_five, True)
                if bl:
                    self.info(text_or_desc[i])
                    self.click_xy_bounds(bounds)
                    return
            elif type(text_or_desc[i]) == list:  # 如果是一组text 遍历校验:
                for l in range(len(text_or_desc[i])):
                    bl, bounds = self.search_text_or_desc_times(text_or_desc[i][l], self.search_short_five, True)
                    if bl:
                        self.info(text_or_desc[i][l])
                        self.click_xy_bounds(bounds)
                        return
            else:
                self.info(text_or_desc[i])
                assert '错误' == '传入的是未知类型'
        assert '错误' == 'any字符串都不正确 {}'.format(*text_or_desc)

    # 点击文案中的某一个即可
    def click_any_just_text(self, *text):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        for i in range(len(text)):
            if i == 0:
                timeout = 3.0
            else:
                timeout = 0.1
            # if type(text[i]) == str or type(text[i]) == unicode:  # 如果是1个id 直接校验
            if type(text[i]) == str:  # 如果是1个id 直接校验
                if d(text=text[i]).wait(timeout=timeout):
                    d(text=text[i]).click()
                    self.info(text[i])
                    return
            elif type(text[i]) == list:  # 如果是一组text 遍历校验:
                for l in range(len(text[i])):
                    if d(text=text[i][l]).wait(timeout=timeout):
                        d(text=text[i][l]).click()
                        self.info(text[i][l])
                        return
            else:
                self.info(text[i])
                assert '错误' == '传入的是未知类型'
        assert '错误' == 'any字符串都不正确 {}'.format(*text)

    # 双击屏幕中心店
    def double_click(self):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        d.double_click(0.5, 0.5, 0.1)

    def click_center(self):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        d.click(0.5, 0.5)

    def click_img(self, num=0):
        # self.driver.click(className='android.widget.ImageView')
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        d(className='android.widget.ImageView')[num].click()

    def click_edit_text(self):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        d(className='android.widget.EditText').click()

    def click_view_view(self, num):
        # self.driver.click(className='android.widget.ImageView')
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        d(className='android.view.View')[num].click()

    # 输入内容
    def just_input(self, text):
        """deyes方法"""
        # self.driver.inputText(data=text)
        """uiautomator2"""
        # 输入调用deyes封装方法无法实现，先直接调用uiautomator2方法
        # d = self.driver.uiauClient.uiautoSession
        d = self.get_uiautomator_driver()
        d.send_keys(text)

    def input_clean(self):
        d = self.get_uiautomator_driver()
        d.clear_text()

    # 输入内容并点击
    def input_click(self, text):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        d.send_keys(text)
        d.send_action("search")

    # def search_desc(self, text_or_desc, return_bounds=False):
    #     return self.search_text_or_desc_times(text_or_desc, self.search_two, return_bounds)

    # 搜索文案是否存在，如果存在就返回，如果不存在就循环搜索0.5秒仍然没有搜索到就返回
    def search_text_or_desc_times(self, text_or_desc, times, return_bounds=False):
        text_or_desc = str(text_or_desc)
        # 如果是单纯超找就显示查找打点
        if not return_bounds:
            self.info('--search_text_or_desc---')
            self.info(text_or_desc)
        bl = False
        for i in range(int(times * 10)):
            if return_bounds:
                bl, bounds = self.xpath_text_or_desc_boolean(text_or_desc, return_bounds)
            else:
                bl = self.xpath_text_or_desc_boolean(text_or_desc, return_bounds)

            if bl:
                if return_bounds:
                    return bl, bounds
                else:
                    return bl
            else:
                time.sleep(0.1)  # 循环等待0.1秒
        if return_bounds:
            return bl, ''
        else:
            return bl

    def search_just_text(self, text):
        return self.search_text_times(text, self.search_short)

    def search_just_text_one(self, text):
        return self.search_text_times(text, self.search_one)

    def search_just_text_three_time(self, text):
        return self.search_text_times(text, self.search_short_five)

    def search_text(self, text):
        # return self.search_text_times(text, self.search_short)
        return self.search_text_or_desc_times(text, self.search_two)

    def search_text_one(self, text):
        return self.search_text_or_desc_times(text, self.search_one)

    def search_text_three_time(self, text):
        return self.search_text_or_desc_times(text, self.search_short_five)

    # 搜索文案是否存在，如果存在就返回，如果不存在就循环搜索0.5秒仍然没有搜索到就返回
    def search_text_times(self, text, times):
        # bl = False
        # for i in range(int(times * 10)):
        #     bl = self.driver.exists(text=text)
        #     if bl:
        #         return bl
        #     else:
        #         time.sleep(0.1)  # 循环等待0.1秒
        # return bl
        d = self.get_uiautomator_driver()
        for i in range(int(times * 10)):
            bl = d(text=text).exists
            if bl:
                return bl
            else:
                time.sleep(0.1)  # 循环等待0.1秒
        return bl

    # 如果找打就点击
    def search_text_click(self, text):
        d = self.get_uiautomator_driver()
        bl = False
        for i in range(int(self.search_short * 10)):
            bl = d(text=text).exists
            if bl:
                self.click_text(text)
                return bl
            else:
                time.sleep(0.1)  # 循环等待0.1秒
        return bl

    # 找到classname
    def search_class_name(self, class_name):
        d = self.get_uiautomator_driver()
        for i in range(int(self.search_two * 10)):
            bl = d(className=class_name).exists
            if bl:
                return bl
            else:
                time.sleep(0.1)  # 循环等待0.1秒
        return bl

    # 搜索id 0.5搜索时长
    def search_id(self, id):
        return self.search_id_time(id, self.search_short)

    def search_id_short(self, id):
        return self.search_id_time(id, self.search_one)

    # 搜索id 3秒时长
    def search_id_one_second(self, id):
        return self.search_id_time(id, self.search_one_second)

    # 搜索id 3秒时长
    def search_id_three_time(self, id):
        return self.search_id_time(id, self.search_three_time)

    # 搜索id 3秒时长
    def search_id_long_time(self, id):
        return self.search_id_time(id, self.search_long_time)

    # 搜索id 传入时长
    def search_id_time(self, id, times):
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        for i in range(int(times * 10)):
            if d(resourceId=id).exists:
                self.info('----search_true---{}-'.format(id))
                return True
            else:
                time.sleep(0.1)  # 循环等待0.1秒
        self.info('----search_false---{}-'.format(id))
        return False

    # 搜索id 并点击
    def search_id_click(self, id):
        self.search_id_click_time(id, self.search_short)

    # 搜索id 并点击 传入时长
    def search_id_click_time(self, id, times):
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        for i in range(int(times * 10)):
            bl = d(resourceId=id).exists
            if bl == True:
                self.click(id)
                return bl
            else:
                time.sleep(0.1)  # 循环等待0.1秒
        return bl

    def search_str_in_text(self, list_text, return_bounds=False):
        return self.search_str_in_text_agrs(list_text, self.search_two, return_bounds)

    def search_str_in_text_three(self, list_text, return_bounds=False):
        return self.search_str_in_text_agrs(list_text, self.search_short_five, return_bounds)

    # 搜索含有传入列表中包含的所有字符串
    def search_str_in_text_agrs(self, list_text, times, return_bounds=False):
        for i in range(int(times * 10)):
            result_list = []
            result_bounds_list = []
            text_bounds = self.get_xml_args_dict('text-bounds')
            for i in range(len(text_bounds)):
                result_list_has = 0
                for l in range(len(list_text)):
                    if list_text[l] in text_bounds[i]:
                        result_list_has += 1
                if result_list_has == len(list_text):
                    result_bounds_list.append(text_bounds[i])
                    result_list.append(self.cut_size(text_bounds[i]))
        self.info('--search_str_in_text--')
        self.info(len(result_list))
        self.info_list(result_list)
        if return_bounds:
            if len(result_list) == 0:
                return False, ''
            else:
                return True, result_bounds_list[0]
        else:
            if len(result_list) == 0:
                return False
            else:
                return True

    def search_package(self, package):
        return self.search_package_times(package, self.search_one_second)

    def search_package_times(self, package, times):
        d = self.get_uiautomator_driver()
        for i in range(int(times * 10)):
            bl = d(packageName=package).exists
            if bl:
                return bl
            else:
                time.sleep(0.1)  # 循环等待0.1秒
        return bl

    """滑动"""

    # class_name 从右往左滑动
    def swipe_class_name_swipe_right_to_left(self, class_name, num=1):
        top, left, right, bottom = self.get_class_name_bounds_four_args(class_name)
        y = int(top) + int((bottom - top) / 2)
        for i in range(num):
            self.swipe_args(right - 2, y, left + 2, y)

    # 滑动返回
    def swipe_back(self):
        y = int(self.get_height() / 2)
        x1 = 0
        x2 = self.get_width()
        self.swipe_args(x1, y, x2, y)

    # # 滑动从左往右
    def swipe_left_right(self):
        y = int(self.get_height() / 2)
        x1 = 10
        x2 = self.get_width() - 10
        self.swipe_args(x1, y, x2, y)

    # 滑动从左往右
    def swipe_right_left(self):
        y = int(self.get_height() / 2)
        x1 = self.get_width() - 10
        x2 = 10
        self.swipe_args(x1, y, x2, y)

    def swipe_args(self, x1, y1, x2, y2, times=0.3):
        # self.driver.swipe((x1, y1), (x2, y2))
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        d.swipe(x1, y1, x2, y2, duration=times)

    def swipe_top_or_down_args_num(self, agrs_1, args_2, all, count):
        for i in range(count):
            self.swipe_top_or_down_args(agrs_1, args_2, all)

    def swipe_top_or_down_args(self, agrs_1, args_2, all):
        """纵向滑动，输入比例  agrs_1 起始比例，agrs_2 结束比例，all总比例"""
        y1 = int(self.get_height() / all * agrs_1)
        y2 = int(self.get_height() / all * args_2)
        x = int(self.get_width() / 2)
        self.info('---swipe---')
        self.info(y1)
        self.info(y2)
        self.info(x)
        self.swipe_args(x, y1, x, y2)

    def swipe_top_or_down_num(self, y1, y2):
        """纵向滑动，输入起始纵向值y1,结束纵向值y2"""
        x = int(self.get_width() / 2)
        self.swipe_args(x, y1, x, y2)

    def swipe_right_to_left_args_y(self, y=0):
        """横向滑动，从右往左滑动，给一个y的纵坐标的值"""
        if y == 0:
            y == int(self.get_height() / 2)
        x1 = self.get_width() - 50
        x2 = 50
        self.swipe_args(x1, y, x2, y)

    def swipe_left_to_right_args_y(self, y=0):
        """横向滑动，从右往左滑动，给一个y的纵坐标的值"""
        if y == 0:
            y == int(self.get_height() / 2)
        x1 = 50
        x2 = self.get_width() - 50
        self.swipe_args(x1, y, x2, y)

    def swipe_right_to_left(self, left=None, top=None, right=None, bottom=None):
        """从右往左滑动，四个坐标"""
        if left == None and top == None and right == None and bottom == None:
            x1 = self.get_width() * 0.9
            x2 = self.get_width() * 0.1
            y = self.get_height() * 0.5
            self.swipe_args(x1, y, x2, y)
        else:
            y = int(top) + int((bottom - top) / 2)
            self.swipe_args(right - 10, y, left + 10, y)

    def swipe_right_to_left_num(self, times, left=None, top=None, right=None, bottom=None):
        """从右往左滑动，N次"""
        for i in range(times):
            self.swipe_right_to_left(left, top, right, bottom)
            self.sleep(0.2)

    def swipe_left_to_right(self, left=None, top=None, right=None, bottom=None):
        """从左往右滑动，四个坐标"""
        if left == None and top == None and right == None and bottom == None:
            x1 = self.get_width() * 0.1
            x2 = self.get_width() * 0.9
            y = self.get_height() * 0.5
            self.swipe_args(x1, y, x2, y)
        else:
            y = int(top) + int((bottom - top) / 2)
            self.swipe_args(left + 10, y, right - 10, y)

    def swipe_left_to_right_num(self, times, left=None, top=None, right=None, bottom=None):
        """从右往左滑动，N次"""
        for i in range(times):
            self.swipe_left_to_right(left, top, right, bottom)
            self.sleep(0.2)

    def swipe_up_to_down(self, left=None, top=None, right=None, bottom=None):
        """从上往下滑动，四个坐标"""
        if left == None and top == None and right == None and bottom == None:
            x = self.get_width() * 0.5
            y1 = self.get_height() * 0.2
            y2 = self.get_height() * 0.8
            self.swipe_args(x, y1, x, y2)
        else:
            x = int(left) + int((right - left) / 2)
            self.swipe_args(x, top + 10, x, bottom - 10)

    def swipe_down_to_up(self, left=None, top=None, right=None, bottom=None):
        """从下往上滑动，四个坐标"""
        if left == None and top == None and right == None and bottom == None:
            x = self.get_width() * 0.5
            y1 = self.get_height() * 0.8
            y2 = self.get_height() * 0.2
            self.swipe_args(x, y1, x, y2)
        else:
            x = int(left) + int((right - left) / 2)
            self.swipe_args(x, bottom - 10, x, top + 10)

    def swipe_scroll_view_down_to_up(self):
        self.swipe_class_name_up_and_down('android.widget.ScrollView', 'down_to_up')

    def swipe_class_name_up_and_down(self, class_name, up_or_down):
        """传入classname 并且纵向滑动"""
        bounds = self.get_class_name_bounds(class_name)
        left, top, right, bottom = self.get_left_top_right_down(bounds)
        x = left + int((right - left) / 2)
        if up_or_down == 'up_to_down':
            self.swipe_args(x, top + 1, x, bottom - 1)
        elif up_or_down == 'down_to_up':
            self.swipe_args(x, bottom - 300, x, top + 1)
        else:
            assert '错误' == '传入的参数错误{}'.format(up_or_down)

    # 拖拽
    def drag(self, sx, sy, ex, ey):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        d.drag(sx, sy, ex, ey, 0.5)

    # 滑动从一个text滑动到另一个text
    def swipe_text_to_text(self, text, text_one):
        bounds = self.get_text_bounds(text)
        x1 = bounds['left'] + (bounds['right'] - bounds['left']) / 2
        y1 = bounds['top'] + (bounds['bottom'] - bounds['top']) / 2
        bounds_one = self.get_text_bounds(text_one)
        x2 = bounds_one['left'] + (bounds_one['right'] - bounds_one['left']) / 2
        y2 = bounds_one['top'] + (bounds_one['bottom'] - bounds_one['top']) / 2
        self.info('-----------')
        self.info(x1)
        self.info(y1)
        self.info(x2)
        self.info(y2)
        # 拖拽
        self.drag(x1, y1, x2, y2)
        # self.swipe_args(x1, y1, x2, y2)

    # 退拽文案到id 从下往上
    def swipe_text_to_id_down_to_up(self, text, id):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        text_bounds = self.get_text_bounds(text)
        id_bounds = self.get_id_bounds(id)
        self.swipe_top_or_down_num(text_bounds['top'], id_bounds['bottom'])

    # 退拽文案到id 从上往下
    def swipe_text_to_id_up_to_down(self, text, id):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        text_bounds = self.get_text_bounds(text)
        id_bounds = self.get_id_bounds(id)
        self.swipe_top_or_down_num(text_bounds['bottom'], id_bounds['top'])

    # 以id的中心点为Y，从右往左滑动整个屏幕的宽
    def swipe_id_right_to_left_wide(self, id):
        bounds = self.get_id_bounds(id)
        # self.info('--swipe---')
        # self.info(bounds)
        left, top, right, down = self.get_left_top_right_down(bounds)
        y = top + int((down - top) / 2)
        x1 = self.get_width() - 10
        x2 = 10
        # self.info(x1)
        # self.info(x2)
        # self.info(y)
        self.info('--swipe--- bounds <{}> x1<{}> x2 <{}> y <{}>'.format(bounds, x1, x2, y))
        self.swipe_args(x1, y, x2, y)

    # 获取id的上下左右，从下滑动到上
    def swipe_id_down_to_up(self, id, num=0):
        bounds = self.get_id_bounds(id)
        left, top, right, down = self.get_left_top_right_down(bounds)
        y1 = down
        y2 = top
        x = left + (right - left) / 2
        self.info('--swipe--- bounds <{}> x<{}> y1 <{}> y2 <{}>'.format(bounds, x, y1 - num, y2))
        self.swipe_args(x, y1 - num, x, y2)

    # 以text的中心点为Y，从右往左滑动整个屏幕的宽
    def swipe_text_right_to_left_wide(self, text, is_desc=False):
        bounds = self.get_text_bounds(text, is_desc)
        # self.info('--swipe---')
        # self.info(bounds)
        left, top, right, down = self.get_left_top_right_down(bounds)
        y = top + int((down - top) / 2)
        x1 = self.get_width() - 10
        x2 = 10
        # self.info(x1)
        # self.info(x2)
        # self.info(y)
        self.info('--swipe--- bounds <{}> x1<{}> x2 <{}> y <{}>'.format(bounds, x1, x2, y))
        self.swipe_args(x1, y, x2, y)

    # 滑动文案到高度
    def swipe_text_down_to_up_height_percent(self, text, percent,down_to_up=True):
        bounds = self.get_text_bounds(text)
        left, top, right, down = self.get_left_top_right_down(bounds)
        x = self.get_width() * 0.5
        y2=self.get_height() * percent
        if down_to_up:
            if down < y2:
                return False
        else:
            if down > y2:
                return False
        self.swipe_args(x, top, x, y2)
        return True


    """<-----获取----->"""

    # 获取className对应的文案
    def get_class_name_text(self, class_name, num=0):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        return d(className=class_name)[num].info['text']
        # 获取className对应的文案

    def get_class_name_bounds_four_args(self, class_name, num=0):
        """uiautomator2"""
        bounds = self.get_class_name_bounds(class_name, num)
        top = bounds['top']
        left = bounds['left']
        right = bounds['right']
        bottom = bounds['bottom']
        return top, left, right, bottom

    def get_class_name_bounds(self, class_name, num=0):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        if num == 0:
            return d(className=class_name).info['bounds']
        else:
            return d(className=class_name)[num].info['bounds']

    def get_class_name_all_text(self, class_name):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        test_list = []
        count = d(className=class_name).count
        for i in range(count):
            text = d(className=class_name)[i].info['text']
            if len(text) > 0:  # 有内容
                self.info(text)
                test_list.append(text)
        return test_list

    # 获取id对应的文案
    def get_id_text(self, id):
        """deyes"""
        # return self.driver.getTextByAttr(resourceId=self.package + id)
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        self.info(id)
        d(resourceId=id).wait(timeout=self.show_time_out)
        return d(resourceId=id).info['text']

    # 获取多个相同id对应的所有文案
    def get_id_texts(self, id):
        """deyes"""
        # return self.driver.getTextByAttr(resourceId=self.package + id)
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        test_list = []
        d(resourceId=id).wait(timeout=self.show_time_out)
        count = d(resourceId=id).count
        for i in range(count):
            text = d(resourceId=id)[i].info['text']
            self.info(text)
            test_list.append(text)
        return test_list

    # 获取相同id的第N个text
    def get_id_text_num(self, id, num):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        d(resourceId=id).wait(timeout=self.show_time_out)
        count = d(resourceId=id).count
        for i in range(count):
            text = d(resourceId=id)[i].info['text']
            if (i + 1) == num:
                self.info(text)
                return text

    # 获取id对应的文案
    def get_id_text_bount(self, id):
        """deyes"""
        # return self.driver.getTextByAttr(resourceId=self.package + id)
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        return d(resourceId=id).info['text']

    # 获取android.widget.EditText的文案
    def get_edit_text(self):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        return self.get_class_name_text("android.widget.EditText")
        # return d(className="android.widget.EditText").info['text']

    # 获取id对应的同级别的子类的文案(传入参数)
    def get_id_sibling_child_text(self, id, sibling_className):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        return d(resourceId=pageage_name_id + id).sibling(className=sibling_className).child(
            className='android.widget.TextView').info['text']

    def get_class_name_child_text(self, class_name, num=0):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        d(className=class_name).wait(timeout=self.show_time_out)
        count = d(className=class_name).child(className='android.widget.TextView').count
        if num >= 0 and num <= count:
            text = d(className=class_name).child(className='android.widget.TextView')[num].info['text']
        elif num < 0 and num >= -count:
            text = d(className=class_name).child(className='android.widget.TextView')[count + num].info['text']
        else:
            assert '错误' == '传入的num越界了，超过了总数'
        # 获取子类的个数
        return text

    def get_class_name_child_bounds(self, class_name, num=0):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        d(className=class_name).wait(timeout=self.show_time_out)
        count = d(className=class_name).child(className='android.widget.TextView').count
        if num >= 0 and num <= count:
            text = d(className=class_name).child(className='android.widget.TextView')[num].info['bounds']
        elif num < 0 and num >= -count:
            text = d(className=class_name).child(className='android.widget.TextView')[count + num].info['bounds']
        else:
            assert '错误' == '传入的num越界了，超过了总数'
        # 获取子类的个数
        return text

    # 获取对应id下的所有相同text的子类
    def get_id_child_all_text(self, id):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        test_list = []
        # 获取子类的个数
        count = d(resourceId=pageage_name_id + id).child(
            className='android.widget.TextView').count
        # 获取所有子类的个数保存到列表
        for i in range(count):
            text = d(resourceId=pageage_name_id + id).child(
                className='android.widget.TextView')[i].info['text']
            test_list.append(text)
        return test_list

    # 获取对应id下的所有子类的view 的 text
    def get_id_child_all_view_text(self, id):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        test_list = []
        d(resourceId=id).wait(timeout=self.show_time_out)
        # 获取子类的个数
        count = d(resourceId=id).sibling(className='android.view.View').child(className='android.view.View').count
        self.info('---child_view_count---')
        self.info(count)
        # 获取所有子类的个数保存到列表
        for i in range(count):
            text = d(resourceId=id).sibling(className='android.view.View').child(className='android.view.View')[i].info[
                'text']
            test_list.append(text)
        return test_list

    # 获取class 是androidx.recyclerview.widget.RecyclerView 的所有子text
    def get_class_name_recycler_view_child_all_text(self):
        return self.get_class_name_child_all_text('androidx.recyclerview.widget.RecyclerView')

    # 获取对应classname下的所有子类的text
    def get_class_name_child_all_text(self, class_name):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        test_list = []
        d(className=class_name).wait(timeout=self.show_time_out)
        # 获取子类的个数
        count = d(className=class_name).child(className='android.widget.TextView').count
        # 获取所有子类的个数保存到列表
        for i in range(count):
            text = d(className=class_name).child(className='android.widget.TextView')[i].info['text']
            test_list.append(text)
        return test_list

    # 获取对应classname 下的所有子类的view 的 text
    def get_class_name_child_all_view_text(self, class_name):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        test_list = []
        d(className=class_name).wait(timeout=self.show_time_out)
        # 获取子类的个数
        count = d(className=class_name).child(className='android.view.View').count
        # 获取所有子类的个数保存到列表
        for i in range(count):
            text = d(className=class_name).child(className='android.view.View')[i].info['text']
            test_list.append(text)
        return test_list

    # 获取对应id下的所有相同text的子类
    def get_id_sibling_child_all_text(self, id, sibling_className):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        test_list = []
        # 获取子类的个数
        count = d(resourceId=pageage_name_id + id).sibling(className=sibling_className).child(
            className=sibling_className).count
        # 获取所有子类的个数保存到列表
        for i in range(count):
            text = d(resourceId=pageage_name_id + id).sibling(className=sibling_className).child(
                className='android.widget.TextView')[i].info['text']
            test_list.append(text)
        return test_list

    def get_text_view(self):
        # return self.driver.getTextByAttr(className="android.widget.TextView")
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        return self.get_class_name_text("android.widget.TextView")

    # 获取id的数量
    def get_id_count(self, id):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        return d(resourceId=id).count

    # 获取text的数量
    def get_text_count(self, text):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        return d(text=text).count

    # 获取text的数量
    def get_class_name_count(self, class_name):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        return d(className=class_name).count

    # 获取id对应的边界
    def get_id_bounds(self, id):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        return d(resourceId=id).info['bounds']

    # 获取id对应的边界
    def get_id_bounds_num(self, id, num):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        id = self.get_id(id)
        num = num - 1
        return d(resourceId=id)[num].info['bounds']

    def get_text_bounds(self, text, is_desc=False):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        if is_desc:
            return d(description=text).info['bounds']
        else:
            return d(text=text).info['bounds']

    def get_text_bounds_num(self, text, num, is_desc=False):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        if is_desc:
            return d(description=text)[num].info['bounds']
        else:
            return d(text=text)[num].info['bounds']

    #获取文字的高
    def get_text_height(self, text, is_desc=False):
        bounds = self.get_text_bounds(text,is_desc)
        left,top,right,down=self.get_left_top_right_down(bounds)
        return down-top

    # 获取文字的宽
    def get_text_width(self, text, is_desc=False):
        bounds = self.get_text_bounds(text,is_desc)
        left,top,right,down=self.get_left_top_right_down(bounds)
        return right-left

    #获取id的高
    def get_id_height(self, id):
        bounds = self.get_id_bounds(id)
        left,top,right,down=self.get_left_top_right_down(bounds)
        return down-top

    #获取id的宽
    def get_id_width(self, id):
        bounds = self.get_id_bounds(id)
        left,top,right,down=self.get_left_top_right_down(bounds)
        return right-left


    # 获取class是 android.view.View 的文案
    def get_view_view_text(self, num):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        return self.get_class_name_text("android.view.View", num)
        # 传入参数获取对应参数的个数

    def get_count(self, args):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        if args == 'android.widget.ImageView':
            return d(className='android.widget.ImageView').count
        if args == 'android.view.View':
            return d(className='android.view.View').count

    # 获取ImageView的个数
    def get_img_count(self):
        return self.get_count('android.widget.ImageView')

    # 获取viewView的个数
    def get_view_count(self):
        return self.get_count('android.view.View')

    # 获取toast内容
    def get_toast(self):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        return d.toast.get_message(5.0, 10.0, "default message")

    """底层方法"""
    #
    # # xpath 定位多个id
    # def driver_assertExistsXpathsId(self, args):
    #     pageDom = self.driver.uiauClient.getPageDom()
    #     for i in range(len(args)):
    #         self.driver.info(args[i])
    #         _node = self.driver.uiauClient.getNodeDom(
    #             xpath=u"//*[@resource-id='%s']/.." % str(args[i]),
    #             pageDom=pageDom)
    #         if _node is None:
    #             raise Exception(u"xpath 对应的内容不存在 " + str(args[i]))

    # # xpath 定位多个id
    # def driver_assertExistsXpathsText(self, *args):
    #     pageDom = self.driver.uiauClient.getPageDom()
    #     for i in range(len(args)):
    #         self.driver.info(args[i])
    #         _node = self.driver.uiauClient.getNodeDom(xpath=u"//*[@text='%s']/.." % args[i],
    #                                                   pageDom=pageDom)
    #         if _node is None:
    #             raise Exception(u"z 对应的内容不存在 " + str(args[i]))
    #
    # # xpath  定位1个文案 或一个列表文案
    # def driver_assertExistsXpathsList(self, xpaths):
    #     pageDom = self.driver.uiauClient.getPageDom()
    #     if type(xpaths) == list:
    #         for xpath in xpaths:
    #             self.driver.info(xpath)
    #             _node = self.driver.uiauClient.getNodeDom(xpath=u"//*[@text='%s']/.." % xpath, pageDom=pageDom)
    #             if _node is None:
    #                 raise Exception(u"xpath 对应的内容不存在 " + str(xpath))
    #     else:
    #         self.driver.info(xpaths)
    #         _node = self.driver.uiauClient.getNodeDom(xpath=u"//*[@resource-id='%s']/.." % xpaths, pageDom=pageDom)
    #         if _node is None:
    #             raise Exception(u"xpath 对应的内容不存在 " + str(xpaths))

    # # xpath  定位1个文案 或一个列表文案
    # def xpath_desc_time_args(self, time_out, desc):
    #     for i in range(int(time_out * 10)):
    #         pageDom = self.driver.uiauClient.getPageDom()
    #         _node = self.driver.uiauClient.getNodeDom(xpath=u"//*[@content-desc='%s']/.." % desc, pageDom=pageDom)
    #         if _node is None:
    #             self.sleep(0.1)
    #         else:
    #             return
    #     assert '错误' == "xpath 对应的内容不存在 {}".format(str(desc))

    """ocr相关"""

    def click_ocr(self, text):
        self.driver.click(ocrPath={"tags": {"tag": text}, "expr": "tag()"})

    def show_ocr(self, text):
        assert self.driver.exists(ocrPath={"tags": {"tag": text}, "expr": "tag()"})

    """xml相关"""

    # def get_xml_file(self):
    #     # from src import os
    #     # from src.iniDefs_base import IniBase_Cls
    #     driver = self.get_devices_id()
    #     return os.path.join(IniBase_Cls.TmpDir, 'xml_{}_temporary.txt'.format(driver))
    #     # return "{}casetree/UserSpace/data/xml_{}_temporary.txt".format(project_path, driver)
    #     # return "{}casetree/UserSpace/data/xml_{}_temporary.txt".format(project_path, driver)

    # 获取当前页面的xml
    def get_xml(self):
        """uiautomator2"""
        d = self.get_uiautomator_driver()
        return d.dump_hierarchy()

    # 通过xlm 获取时间的文案 00：00
    def get_xml_time_text(self):
        result_list = self.get_xml_args_dict('android.widget.TextView')
        time_text = ''
        for i in range(len(result_list)):
            if ":" in result_list[i]:
                time_text = result_list[i]
                return time_text
        assert '错误' == '当前页面没有 : '

    # 获取当前页面的xml并保存到临时的txt文件
    def creat_page_xml_to_txt(self):
        # h获取xml
        xml = self.get_xml()
        # 获取路径
        file = self.get_xml_file()
        # 写入xml
        with open(file, 'w') as f:
            f.write(str(xml))
        """有BUG需要两次写入才OK"""
        # h获取xml
        xml = self.get_xml()
        # 获取路径
        file = self.get_xml_file()
        # 写入xml
        with open(file, 'w') as f:
            f.write(str(xml))

    # 读取保存xml的文件
    def read_xml_file(self):
        file = self.get_xml_file()
        with open(file, 'r') as f:
            content = f.readlines()
        return content

    # 获取含有某个字符串的text
    def get_str_in_text_all(self, str):
        return self.get_str_in_text_all_args(str, 'text-desc')

    # 获取含有某个字符串的text
    def get_str_in_text_all_view_view(self, str):
        return self.get_str_in_text_all_args(str, 'android.view.View')

    # 获取含有某个字符串的text
    def get_str_in_text_all_img_view(self, str):
        return self.get_str_in_text_all_args(str, 'android.widget.ImageView')

    # 获取含有某个字符串的text
    def get_str_in_text_all_args(self, str, class_name):
        text_list = []
        for i in range(int(self.search_three_time * 10)):
            # 获取页面所有文案
            get_text_list = self.get_xml_args_dict(class_name)
            for i in range(len(get_text_list)):
                if str in get_text_list[i]:
                    text_list.append(get_text_list[i])
            if len(text_list) != 0:
                return text_list
            else:
                self.sleep(0.1)
        assert '错误' == '没有找到任何含有字符串{}的文案'.format(str)

    def get_xml_view_view_just_bounds(self):
        return self.get_xml_args_dict('android.view.View-just-bounds')

    def get_xml_view_view(self, time_out=0.1):
        return self.get_xml_args_dict('android.view.View', time_out)

    def get_xml_ids_bounds(self):
        return self.get_xml_args_dict('id')

    def get_text_desc(self):
        return self.get_xml_args_dict('text-desc')

    # 获取classname是android.widget.ScrollView的坐标
    def get_scroll_view_bounds(self):
        return self.get_class_name_bounds('android.widget.ScrollView')

    def get_xml_id_args_dict(self, id, args):
        id = self.get_id(id)
        self.show_id(id)
        self.creat_page_xml_to_txt()
        result_list = []
        all = self.read_xml_file()
        for i in range(len(all)):
            if args == 'bounds':
                if ('text=' in all[i]) and (('resource-id="{}"'.format(id) in all[i])) and (
                        'com.android.systemui:id' not in all[i]):  # 如果本行没有text=就不筛选,如果有系统id就不筛选
                    bounds = str(re.findall(r'bounds="(.*?)"', all[i])[0])
                    if len(bounds) > 0:
                        result_list.append(bounds)
            if args == 'text':
                if ('text=' in all[i]) and (('resource-id="{}"'.format(id) in all[i])) and (
                        'com.android.systemui:id' not in all[i]):  # 如果本行没有text=就不筛选,如果有系统id就不筛选
                    text = str(re.findall(r'text=["\'](.*?)["\']', all[i])[0])
                    if len(text) > 0:
                        result_list.append(text)
            if args == 'text-bounds':
                if ('text=' in all[i]) and (('resource-id="{}"'.format(id) in all[i])) and (
                        'com.android.systemui:id' not in all[i]):  # 如果本行没有text=就不筛选,如果有系统id就不筛选
                    text = str(re.findall(r'text=["\'](.*?)["\']', all[i])[0])
                    bounds = str(re.findall(r'bounds="(.*?)"', all[i])[0])
                    if len(text) > 0:
                        result_list.append(text + bounds)
        return result_list

    # 获取xml文件的参数，传入内容
    def get_xml_args_dict(self, args, time_out=0.1):
        for i in range(int(time_out * 10)):  # N秒循环超时
            self.creat_page_xml_to_txt()
            all = self.read_xml_file()
            result_list = []
            for i in range(len(all)):
                if args == 'text':
                    if ('text=' in all[i]) and (pageage_name in all[i]):  # 如果本行没有text=就不筛选,如果有系统id就不筛选
                        text = str(re.findall(r'text=["\'](.*?)["\']', all[i])[0])
                        if len(text) > 0:
                            result_list.append(text)
                if args == 'text-bounds':
                    if ('text=' in all[i]) and (pageage_name in all[i]):  # 如果本行没有text=就不筛选,并且pageage=cn.cntvnews
                        text = str(re.findall(r'text=["\'](.*?)["\']', all[i])[0])
                        bounds = str(re.findall(r'bounds="(.*?)"', all[i])[0])
                        if len(text) > 0:
                            result_list.append(text + bounds)
                if args == 'id':
                    if ('text=' in all[i]) and (pageage_name in all[i]):  # 如果本行没有text=就不筛选,如果有系统id就不筛选
                        id = str(re.findall(r'resource-id=["\'](.*?)["\']', all[i])[0])
                        if len(id) > 0:
                            result_list.append(id)
                if args == 'android.widget.TextView':
                    if ('text=' in all[i]) and (pageage_name in all[i]) and (
                            'android.widget.TextView' in all[i]):  # 如果本行没有text=就不筛选,如果有系统id就不筛选
                        text = str(re.findall(r'text=["\'](.*?)["\']', all[i])[0])
                        if len(text) > 0:
                            result_list.append(text)
                if args == 'android.widget.TextView-bounds':
                    if ('text=' in all[i]) and (pageage_name in all[i]) and (
                            'android.widget.TextView' in all[i]):  # 如果本行没有text=就不筛选,如果有系统id就不筛选
                        text = str(re.findall(r'text=["\'](.*?)["\']', all[i])[0])
                        bounds = str(re.findall(r'bounds="(.*?)"', all[i])[0])
                        if len(text) > 0:
                            result_list.append(text + bounds)
                if args == 'android.view.View':
                    if ('text=' in all[i]) and (pageage_name in all[i]) and (
                            'android.view.View' in all[i]):
                        text = str(re.findall(r'text=["\'](.*?)["\']', all[i])[0])
                        desc = str(re.findall(r'content-desc=["\'](.*?)["\']', all[i])[0])
                        if len(text) > 0:
                            result_list.append(text)
                        elif len(desc) > 0:
                            result_list.append(desc)
                if args == 'android.widget.ImageView':
                    if ('text=' in all[i]) and (pageage_name in all[i]) and (
                            'android.widget.ImageView' in all[i]):
                        text = str(re.findall(r'text=["\'](.*?)["\']', all[i])[0])
                        desc = str(re.findall(r'content-desc=["\'](.*?)["\']', all[i])[0])
                        if len(text) > 0:
                            result_list.append(text)
                        elif len(desc) > 0:
                            result_list.append(desc)
                if args == 'android.widget.ImageView-desc':
                    if (pageage_name in all[i]) and ('content-desc="' in all[i]) and (
                            'android.widget.ImageView' in all[i]):
                        desc = str(re.findall(r'content-desc=["\'](.*?)["\']', all[i])[0])
                        if len(desc) > 0:
                            result_list.append(desc)
                if args == 'android.widget.ImageView-bounds':
                    if ('text=' in all[i]) and (pageage_name in all[i]) and (
                            'android.widget.ImageView' in all[i]):
                        bounds = str(re.findall(r'bounds="(.*?)"', all[i])[0])
                        if len(bounds) > 0:
                            result_list.append(bounds)
                if args == 'android.view.View-bounds':
                    if ('text=' in all[i]) and (pageage_name in all[i]) and (
                            'android.view.View' in all[i]):
                        text = str(re.findall(r'text=["\'](.*?)["\']', all[i])[0])
                        desc = str(re.findall(r'content-desc=["\'](.*?)["\']', all[i])[0])
                        bounds = str(re.findall(r'bounds="(.*?)"', all[i])[0])
                        if len(text) > 0:
                            result_list.append(text + bounds)
                        elif len(desc) > 0:
                            result_list.append(desc + bounds)
                if args == 'android.view.View-just-bounds':
                    if ('text=' in all[i]) and (pageage_name in all[i]) and (
                            'android.view.View' in all[i]):
                        bounds = str(re.findall(r'bounds="(.*?)"', all[i])[0])
                        if len(bounds) > 0:
                            result_list.append(bounds)
                if args == 'android.widget.ScrollView':
                    if ('text=' in all[i]) and (pageage_name in all[i]) and (
                            'android.widget.ScrollView' in all[i]):
                        bounds = str(re.findall(r'bounds="(.*?)"', all[i])[0])
                        if len(bounds) > 0:
                            result_list.append(bounds)
                if args == 'android.view.ViewGroup':
                    if (pageage_name in all[i]) and ('android.view.ViewGroup' in all[i]):
                        bounds = str(re.findall(r'bounds="(.*?)"', all[i])[0])
                        if len(bounds) > 0:
                            result_list.append(bounds)
                if args == 'android.widget.LinearLayout':
                    if (pageage_name in all[i]) and ('android.widget.LinearLayout' in all[i]):
                        bounds = str(re.findall(r'bounds="(.*?)"', all[i])[0])
                        if len(bounds) > 0:
                            result_list.append(bounds)
                if args == 'desc-bounds':
                    if (pageage_name in all[i]) and ('content-desc="' in all[i]):
                        desc = str(re.findall(r'content-desc=["\'](.*?)["\']', all[i])[0])
                        bounds = str(re.findall(r'bounds="(.*?)"', all[i])[0])
                        if len(text) > 0:
                            result_list.append(desc + bounds)
                if args == 'text-desc-bounds':
                    if (pageage_name in all[i]) and ('content-desc="' in all[i]) and ('text="' in all[i]):
                        desc = str(re.findall(r'content-desc=["\'](.*?)["\']', all[i])[0])
                        text = str(re.findall(r'text=["\'](.*?)["\']', all[i])[0])
                        bounds = str(re.findall(r'bounds="(.*?)"', all[i])[0])
                        if len(text) > 0:
                            result_list.append(text + bounds)
                        elif len(desc) > 0:
                            result_list.append(desc + bounds)
                if args == 'text-desc':
                    if (pageage_name in all[i]) and ('content-desc="' in all[i]) and ('text="' in all[i]):
                        desc = str(re.findall(r'content-desc=["\'](.*?)["\']', all[i])[0])
                        text = str(re.findall(r'text=["\'](.*?)["\']', all[i])[0])
                        if len(text) > 0:
                            result_list.append(text)
                        elif len(desc) > 0:
                            result_list.append(desc)
            # self.info('-----------xml_result_list-----------')
            # self.info_list_len(result_list)
            if len(result_list) == 0:
                # self.info('-----------xml_result_list_again----------')
                self.sleep(0.1)
            else:
                return result_list
        self.info('----get_xml_args_dict 没有找到任何内容传出空数组----')
        return []

    # 获取xml文件的参数，传入内容,空值也返回
    def get_xml_args_dict_and_empty(self, args):
        self.creat_page_xml_to_txt()
        result_list = []
        all = self.read_xml_file()
        for i in range(len(all)):
            if args == 'android.view.View-bounds':
                if ('text=' in all[i]) and (pageage_name in all[i]) and (
                        'android.view.View' in all[i]):
                    text = str(re.findall(r'text=["\'](.*?)["\']', all[i])[0])
                    bounds = str(re.findall(r'bounds="(.*?)"', all[i])[0])
                    result_list.append(text + bounds)
            if args == 'android.view.View-desc-bounds':
                if ('content-desc="' in all[i]) and (pageage_name in all[i]) and ('android.view.View' in all[i]):
                    desc = str(re.findall(r'content-desc=["\'](.*?)["\']', all[i])[0])
                    bounds = str(re.findall(r'bounds="(.*?)"', all[i])[0])
                    result_list.append(desc + bounds)
        return result_list

    # 点击第N个传入的有内容的参数
    def click_view_view_has_text_num(self, num):
        count = 0
        self.creat_page_xml_to_txt()
        result_list = []
        all = self.read_xml_file()
        # # 检查界面显示含有文案的view的数量，如果数量小于num,就等待再获取
        for i in range(len(all)):
            if ('text=' in all[i]) and (pageage_name in all[i]) and (
                    'android.view.View' in all[i]):
                text = str(re.findall(r'text=["\'](.*?)["\']', all[i])[0])
                bounds = str(re.findall(r'bounds="(.*?)"', all[i])[0])
                if len(text) > 0:
                    count = count + 1
                    if count == num:
                        self.info('===11===')
                        self.info(text)
                        self.info(bounds)
                        left, top, right, bottom = self.get_left_top_right_down(bounds)
                        self.click_xy(left, top, right, bottom, 1080, 1920)
                        return
        assert '错误' == '当前页面android.view.View获取的数量小于传入的num数量'

    # size 是在当前屏幕显示
    def is_size_show_screen(self, size):
        # 获取上下左右
        self.info(size)
        left, top, right, down = self.get_left_top_right_down(size)
        if left >= 0 and right <= self.get_width() and top >= 0 and down <= self.get_height() and right - left > 10 and down - top > 10:
            pass
        else:
            assert '错误' == '元素没有在当前页面显示'

    # """adb 相关"""
    #
    def get_adb_response(self, adb_content):
        """把adb 命令的内容返回"""
        return self.driver.adbShell(adb_content)
