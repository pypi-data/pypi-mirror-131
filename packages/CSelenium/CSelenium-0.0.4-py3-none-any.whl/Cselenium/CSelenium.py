# coding=utf-8
'''

                mySelenium
作者：LX
开始时间: 2021.12.15
更新时间: 2021.12.20
简化原生selenium操作,以更简短的方式对元素定位
使代码看起来更加清晰.
特点：
    代码简洁,
    代码具有及联操作


author: LX
Start Time: 2021.12.15
UpdateTime: 2021.12.18
Simplify native Selenium operations to locate elements in a shorter manner
Make the code look cleaner.
characteristics:
    Clean code,
    Code has and associated operations
---------------------------------------------------------------
Directions for use
    # 初始化 Initialize
    cs = ChromeSelenium()
    # 打开网页 open Url
    cs.get(url)
    # 等待时间  Waiting time
    cs.wait(2)
    # 关闭网页  Close Url
    cs.quit()
'''

import os
import sys
import time
import random
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.switch_to import SwitchTo
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from .Language import Language

Lan = Language.L

'''
    谷歌selenium
'''


# 操作步骤类
class Steps:
    def __init__(self):
        '''
        {
            url:[操作步骤]
        }
        '''
        self.__step_list={}  # type:{str:list}
        self.__language_list = ["Chinese","English"]
        self.__language = "Chinese"

    # 设置语言
    def setLanguage(self,language:str="Chinese"):
        self.__language = language

    def language(self) -> str:
        return self.__language

    # 判断网址是否存在
    # Determine if the url exists
    def isUrl(self,url:str):
        if url in self.__step_list:
            return True
        return False

    # 添加步骤
    # Add the driver
    def addStep(self,url:str,text:str):
        if not self.isUrl(url):
            self.__step_list[url] = list()
        self.__step_list[url].append(text)

    # 输出步骤
    # The output step
    def pintStep(self):
        for k,v in self.__step_list.items():
            print(k,"--")
            for i in v:
                print("         -->",i)


class ChromeSelenium:

    # 模拟键盘的key 例如: ChromeSelenium.Key.BACKSPACE
    # The key of the simulated keyboard. example: ChromeSelenium.Key.BACKSPACE
    Key = Keys

    def __init__(self,url:str=None,is_interface:bool=True,
                 info_tracking:bool=False,wait_time:int=1,
                 driver:WebDriver=None):
        '''

        :param url: 网址
        :is_interface:无界面
        info_tracking:信息追踪
        :param wait_time: 等待时间
        :param driver: 支持将原生selenium驱动对象转换成ChromeSelenium对象
        url
        Waiting time
        Support for converting native Selenium driver objects into ChromeSelenium objects
        '''
        # 驱动 drive
        if driver:
            self.setDriver(driver)
        else:
            if is_interface:
                self.__drive = webdriver.Chrome()
            else:
                chrome_options = Options()
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
                self.__drive = webdriver.Chrome(chrome_options=chrome_options)

        # 元素对象  The element object
        self.__ele = None  # type:WebElement
        # 历史url  Url history
        self.__his_url = []
        # 弹窗对象  alter object
        self.__alter_obj = None  #type:SwitchTo
        # 下标 index
        self.__index = -1
        # 追踪
        self.__tracking = info_tracking
        # 记录操作步骤类 Record the action step class
        self.__steps = Steps()
        if url:
            self.get(url,wait_time)

    # 设置语言
    def setLanguage(self,language:str="Chinese"):
        self.__steps.setLanguage(language)

    # 是否追踪输出
    def __is_trackingOut(self,st):
        if self.__tracking:
            print("         -->",st)
        self.__steps.addStep(self.currentUrl, st)

    # 返回当前时间 Return current time
    @property
    def currentTime(self) -> str:
        '''
        返回当前时间
        Return current time
        :return: str
        '''
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 设置驱动 Set the drive
    def setDriver(self,driver:WebDriver):
        '''
        设置驱动
        :param driver: 支持将原生selenium驱动对象转换成ChromeSelenium对象
        :return: self
        Set the drive
        Support for converting native Selenium driver objects into ChromeSelenium objects
        '''
        self.__drive = driver
        return self

    # 设置文档元素 Setting document Elements
    def setEle(self,ele:WebElement):
        '''
        设置文档元素
        :param ele: 支持将原生selenium文档对象转换成ChromeSelenium文档对象
        :return: self
        Setting document Elements
        Support for converting native Selenium driver objects into ChromeSelenium objects
        '''
        self.__ele = ele
        return self

    # 返回原始驱动对象Returns the original driver object
    @property
    def driver(self) -> WebDriver:
        '''
        Returns the original driver object
        :return: selenium
        '''
        return self.__drive

    # 当前操作的url  Url of the current operation
    @property
    def currentUrl(self)->str:
        '''
        当前操作的url
        :return: str
        Url of the current operation
        '''
        if self.allUrl():
            return self.allUrl()[-1]
        return ""

    # 打开网页  open Url
    def get(self,url:str="",wait_time:int=1):
        '''

        :param url: url
        :param wait_time: 等待时间
        :return: self
        url
        wait time
        '''
        self.__drive.get(url)
        # 加入url
        self.__his_url.append(url)
        # 记录打
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,url)
        if self.__tracking:
            print(st,"--")
        self.__steps.addStep(self.currentUrl, st)
        time.sleep(wait_time)
        return self

    # 输入键 Enter key
    def send_keys(self,*value):
        '''

        :param text: 文本
        :return: self
        text
        '''

        self.getEle().send_keys(*value)
        # 记录步骤
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime, value)
        self.__is_trackingOut(st)
        return self

    # 点击 click
    def click(self):
        '''
        点击
        :return: self
        click
        '''
        self.getEle().click()
        # 记录步骤
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime)
        self.__is_trackingOut(st)
        return self

    # 强制等待 Mandatory waiting
    def wait(self,wait_time=0):
        '''
        强制等待
        :param wait_time: 时间
        :return:
        Mandatory waiting
        '''
        # 记录步骤
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,wait_time)
        self.__is_trackingOut(st)
        time.sleep(wait_time)
        return self

    # 隐试等待
    def implicitly_wait(self,wait_time=4):
        '''
        隐试等待
        :param wait_time: 时间
        :return: self
        implicit wait
        '''
        # 记录步骤
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime, wait_time)
        self.__is_trackingOut(st)
        self.__drive.implicitly_wait(wait_time)
        return self

    # def eleWait(self,max_wait_time:int=10):
        # WebDriverWait(self.__drive,max_wait_time).until()

    # 输出步骤 output step
    def pintStep(self) -> None:
        '''
        output step
        :return: None
        '''
        self.__steps.pintStep()

    # 清除 clear
    def clear(self):
        '''
        清除
        :return: self
        clear
        '''
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime)
        self.__is_trackingOut(st)

        self.__ele.clear()
        return self

    # 获取元素文本 Get element text
    @property
    def text(self) -> str:
        '''
        获取元素文本
        :return: self
        Get element text
        '''
        t = self.getEle().text
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,t)
        self.__is_trackingOut(st)
        return t

    @property
    def value(self):
        v = self.getEle().get_attribute("value")
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime, v)
        self.__is_trackingOut(st)
        return v

    # 自动获取值
    @property
    def autoValue(self) -> [str,dict]:
        t = self.text
        v = self.value
        if t == v:
            return v
        elif t and v:
            return {"text":t,"value":v}
        elif t:
            return t
        else:
            return v


    # 提交submit
    def submit(self):
        '''
        提交
        :return: self
        submit
        '''
        self.getEle().submit()
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime)
        self.__is_trackingOut(st)
        return self

    # 返回所有get访问过到url  Returns all gets visited to the URL
    def allUrl(self)->list:
        '''
        返回所有get访问过到url
        :return: list
        Returns all gets visited to the URL
        '''
        return self.__his_url

    # 网页标题 page title
    @property
    def title(self) -> str:
        '''
        网页标题
        :return: str
         page title
        '''
        title_ = self.__drive.title
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,
                                                                                 title_)
        self.__is_trackingOut(st)
        return title_

    # 元素长度
    @property
    def len(self)->int:
        '''
        元素长度
        :return: int
        len
        '''
        if isinstance(self.getEle(),WebDriverWait):
            return 1
        if isinstance(self.getEle(),list):
            return len(self.getEle())

    # 窗口最大化 Window maximization
    def maxWin(self):
        '''
        窗口最大化
        :return: self
        Window maximization
        '''
        self.__drive.maximize_window()
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime)
        self.__is_trackingOut(st)
        return self

    # 窗口最小化 Window minimization
    def minWin(self):
        '''
        窗口最小化
        :return: self
        Window minimization
        '''
        self.__drive.minimize_window()
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime)
        self.__is_trackingOut(st)
        return self

    # 设置窗口大小 Setting window size
    def resize(self,w:int,h:int):
        '''
        设置窗口大小
        :param w: 宽度
        :param h: 高度
        :return: self
        Setting window size
        Width
        height
        '''
        self.__drive.set_window_size(w,h)
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,w,h)
        self.__is_trackingOut(st)
        return self

    # 处理框架 Processing framework
    def frame(self):
        '''
        处理框架
        :return: self
        Processing framework
        '''
        self.__drive.switch_to.frame(self.getEle())
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime)
        self.__is_trackingOut(st)
        return self

    # 切换默认文档 Switching between default documents
    def defaultContent(self):
        '''
        切换默认文档
        :return: self
        Switching between default documents
        '''
        self.__drive.switch_to.default_content()
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime)
        self.__is_trackingOut(st)
        return self

    # 切换到父框架(上一层) Switch to parent frame (previous layer)
    def parentFrame(self):
        '''
        切换到父框架(上一层)
        :return: self
        Switch to parent frame (previous layer)
        '''
        self.__drive.switch_to.parent_frame()
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime)
        self.__is_trackingOut(st)
        return self

    # 处理弹窗 Handle the pop-up
    def alert(self):
        '''
        处理弹窗
        :return: self
        Handle the pop-up
        '''
        self.__alter_obj = self.__drive.switch_to.alert  #type: SwitchTo
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime)
        self.__is_trackingOut(st)
        return self

    # 接收弹窗 Receive the pop-up
    def alertOK(self):
        '''
        接收弹窗
        :return: self
        Receive the pop-up
        '''
        if self.__alter_obj:
            self.__alter_obj.accept()
            # 接收完弹窗立刻清除
            self.__alter_obj = None
            st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime)
            self.__is_trackingOut(st)
        return self

    # 取消弹窗 Cancel the popup window
    def alertNO(self):
        '''
        取消弹窗
        :return: self
        Cancel the popup window
        '''
        if self.__alter_obj:
            self.__alter_obj.dismiss()
            # 接收完弹窗立刻清除
            self.__alter_obj = None
            st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime)
            self.__is_trackingOut(st)
        return self

    # 获取弹窗文本 Gets popover text
    @property
    def alertText(self)->str:
        '''
        获取弹窗文本
        :return: str
        Gets popover text
        '''
        if self.__alter_obj:
            st = '{} 获取alert弹窗文本:[{}]'.format(self.currentTime,self.__alter_obj.text)
            self.__steps.addStep(self.currentUrl, st)
            return self.__alter_obj.text

    # 快照 snapshot
    def save_screenshot(self,image_name:str=None,path:str=None,suffix:str="png"):
        '''
        快照
        :param image_name:图片名称
        :param path:路径
        :param suffix:后缀
        :return:
        snapshot
        '''
        temp = self.currentTime
        if path:
            if image_name:
                file = os.path.join(path,image_name+"."+suffix)
                self.__drive.get_screenshot_as_file(file)
            else:
                file = os.path.join(path, temp + "." + suffix)
                self.__drive.get_screenshot_as_file(file)
        else:
            if image_name:
                file = os.path.join(os.path.dirname(__file__),image_name+"."+suffix)
                self.__drive.get_screenshot_as_file(file)
            else:
                file = os.path.join(os.path.dirname(__file__), temp + "." + suffix)
                self.__drive.get_screenshot_as_file(file)
        # 记录步骤
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,file)
        self.__is_trackingOut(st)
        return self

    # 模版 template
    def __posTemplate(self,by,value,text:str=None,wait_time:int=0,is_press=False):
        '''

        :param by: 匹配方式
        :param value:值
        :param text: 输入文本
        :param wait_time: 等待时间
        :param is_press: 是否按下
        :return:
        '''
        self.__ele = self.__drive.find_element(by, value)
        if text:
            self.__ele.send_keys(text)
        if is_press:
            self.__ele.click()
        if wait_time>0:
            # self.implicitly_wait(wait_time)
            time.sleep(wait_time)

    # 多匹配
    def __posTemplates(self,by,value,wait_time:int=0):
        self.__ele = self.__drive.find_elements(by, value)

        if wait_time>0:
            # self.implicitly_wait(wait_time)
            time.sleep(wait_time)

    # 返回当查找元素当对象
    def getEle(self) -> [list,WebElement]:
        return self.__ele

    # 元素大小
    @property
    def eleSize(self) -> dict:
        return self.__ele.size

    # 元素宽度
    @property
    def eleWidth(self)->int:
        return self.eleSize["width"]

    # 元素高度
    @property
    def eleHeight(self)->int:
        return self.eleSize["height"]

    # 返回元素属性值
    def eleAttr(self,attribute,index:int=0) -> str:

        if isinstance(self.__ele,WebElement):
            value = self.__ele.get_attribute(attribute)
            st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime, value)
            self.__is_trackingOut(st)
            return value
        if isinstance(self.__ele,list):
            value = self.__ele[index].get_attribute(attribute)
            st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime, value)
            self.__is_trackingOut(st)
            return value

    # 检查元素到可见性
    @property
    def eleIs_Displayed(self) -> bool:
        return self.__ele.is_displayed()

    # 元素绝对位置
    def absElePos(self)->dict:
        value = self.getEle().location
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime, value)
        self.__is_trackingOut(st)
        return value

    # 元素绝对位置x
    def abaX(self)->int:
        return self.absElePos()["x"]

    # 元素当绝对位置y
    def abaY(self) -> int:
        return self.absElePos()["y"]

    # 多窗口切换
    def moreWins(self,i:int):
        win_handles = self.__drive.window_handles
        # 定位到窗口
        self.__drive.switch_to.window(win_handles[i])
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime)
        self.__is_trackingOut(st)
        return self

    # 切换到下一个窗口
    def nextWin(self):
        win_handles = self.__drive.window_handles
        win_handles_len = len(win_handles)
        current_win=self.__drive.current_window_handle
        index = win_handles.index(current_win)
        index+=1
        if index < win_handles_len:
            self.moreWins(index)
            st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,
                                                                                     self.__drive.title)
            self.__is_trackingOut(st)
        return self

    # 切换到上一个窗口
    def onWin(self):
        win_handles = self.__drive.window_handles
        current_win = self.__drive.current_window_handle
        index = win_handles.index(current_win)
        index -= 1
        if index >= 0:
            self.moreWins(index)
            st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,
                                                                                     self.__drive.title)
            self.__is_trackingOut(st)
        return self

    # id定位
    def id(self,value,text:str=None,wait_time:int=0,is_press=False):
        self.__posTemplate(by=By.ID,
                           value=value,
                           text=text,
                           wait_time=wait_time,
                           is_press=is_press)
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,
                                                                                 value)
        self.__is_trackingOut(st)
        return self

    # XPATH查找
    def xpath(self,value,text:str=None,wait_time:int=0,is_press=False):
        self.__posTemplate(by=By.XPATH,
                           value=value,
                           text=text,
                           wait_time=wait_time,
                           is_press=is_press)
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,
                                                                                 value)
        self.__is_trackingOut(st)
        return self

    # css查找
    def css(self,value,text:str=None,wait_time:int=0,is_press=False):
        self.__posTemplate(by=By.CLASS_NAME,
                           value=value,
                           text=text,
                           wait_time=wait_time,
                           is_press=is_press)
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,
                                                                                 value)
        self.__is_trackingOut(st)
        return self

    # TAG_NAME查找
    def tagName(self,value,text:str=None,wait_time:int=0,is_press=False):
        self.__posTemplate(by=By.TAG_NAME,
                           value=value,
                           text=text,
                           wait_time=wait_time,
                           is_press=is_press)
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,
                                                                                 value)
        self.__is_trackingOut(st)
        return self

    # LINK_TEXT查找
    def linkText(self,value,text:str=None,wait_time:int=0,is_press=False):
        self.__posTemplate(by=By.LINK_TEXT,
                           value=value,
                           text=text,
                           wait_time=wait_time,
                           is_press=is_press)
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,
                                                                                 value)
        self.__is_trackingOut(st)
        return self

    # NAME查找
    def name(self,value,text:str=None,wait_time:int=0,is_press=False):
        self.__posTemplate(by=By.NAME,
                           value=value,
                           text=text,
                           wait_time=wait_time,
                           is_press=is_press)
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,
                                                                                 value)
        self.__is_trackingOut(st)
        return self

    # PARTIAL_LINK_TEXT查找
    def partialLineText(self,value,text:str=None,wait_time:int=0,is_press=False):
        self.__posTemplate(by=By.PARTIAL_LINK_TEXT,
                           value=value,
                           text=text,
                           wait_time=wait_time,
                           is_press=is_press)
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,
                                                                                 value)
        self.__is_trackingOut(st)
        return self

    # XPATH查找 多匹配
    def xpaths(self,value,wait_time:int=0):
        self.__posTemplates(by=By.XPATH,
                            value=value,
                            wait_time=wait_time)
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,
                                                                                 value)
        self.__is_trackingOut(st)
        return self

    # css查找 多匹配
    def csss(self,value,wait_time:int=0):
        self.__posTemplates(by=By.CSS_SELECTOR,
                            value=value,
                            wait_time=wait_time)
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,
                                                                                 value)
        self.__is_trackingOut(st)
        return self

    # TAG_NAME查找 多匹配
    def tagNames(self,value,wait_time:int=0):
        self.__posTemplates(by=By.TAG_NAME,
                            value=value,
                            wait_time=wait_time)
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,
                                                                                 value)
        self.__is_trackingOut(st)
        return self

    # LINK_TEXT查找 多匹配
    def linkTexts(self,value,wait_time:int=0):
        self.__posTemplates(by=By.LINK_TEXT,
                            value=value,
                            wait_time=wait_time)
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,
                                                                                 value)
        self.__is_trackingOut(st)
        return self

    # NAME查找 多匹配
    def names(self,value,wait_time:int=0):
        self.__posTemplates(by=By.NAME,
                            value=value,
                            wait_time=wait_time)
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,
                                                                                 value)
        self.__is_trackingOut(st)
        return self

    # PARTIAL_LINK_TEXT查找 多匹配
    def partialLineTexts(self,value,wait_time:int=0):
        self.__posTemplates(by=By.PARTIAL_LINK_TEXT,
                            value=value,
                            wait_time=wait_time)
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,
                                                                                 value)
        self.__is_trackingOut(st)
        return self

    # 执行脚本
    def exec_script(self,js:str,*args):
        self.__drive.execute_script(js,*args)
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,
                                                                                 js)
        self.__is_trackingOut(st)
        return self

    # 执行异步脚本
    def exec_async_script(self,js,*args):
        self.__drive.execute_async_script(js,args)
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,
                                                                                 js)
        self.__is_trackingOut(st)
        return self

    # 网页源码
    def source(self,encoding=None)->str:
        if encoding:
            return BeautifulSoup(self.__drive.page_source , "html.parser").prettify(encoding)
        return BeautifulSoup(self.__drive.page_source , "html.parser").prettify()

    # 浏览器后退
    def back(self):
        self.__drive.back()
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime)
        self.__is_trackingOut(st)
        return self

    # 浏览器前进
    def forward(self):
        self.__drive.forward()
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime)
        self.__is_trackingOut(st)
        return self

    # 刷新
    def refresh(self):
        self.__drive.refresh()
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime)
        self.__is_trackingOut(st)
        return self

    # 按住左键不放
    def mouseClick_and_hold(self):
        ActionChains(self.__drive).click_and_hold(self.__ele).perform()
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime)
        self.__is_trackingOut(st)
        return self

    # 在某个元素位置松开左键
    def mouseRelease(self):
        ActionChains(self.__drive).release(self.__ele).perform()
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime)
        self.__is_trackingOut(st)
        return self

    # 双击鼠标左键
    def mouseDoubleClick(self):
        ActionChains(self.__drive).double_click(self.__ele).perform()
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime)
        self.__is_trackingOut(st)
        return self

    # 点击鼠标右键
    def mouseRightClick(self):
        ActionChains(self.__drive).context_click(self.__ele).perform()
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime)
        self.__is_trackingOut(st)
        return self

    # 鼠标移动
    def mouseOffset(self,x:int,y:int):
        ActionChains(self.__drive).move_by_offset(x,y).perform()
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,x,y)
        self.__is_trackingOut(st)
        return self

    # 鼠标移动到某个元素
    def mouseToElement(self):
        ActionChains(self.__drive).move_to_element(self.__ele).perform()
        return self

    # 拖拽元素在到其它元素
    def mouseDrag_And_Drop(self,target):
        ActionChains(self.__drive).drag_and_drop(self.__ele,target).perform()
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime)
        self.__is_trackingOut(st)
        return self

    # 将鼠标移动到距某个元素多少距离的位置
    def mouseMove_To_Element_With_Offset(self,x:int,y:int):
        ActionChains(self.__drive).move_to_element_with_offset(self.__ele,x,y).perform()
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,x,y)
        self.__is_trackingOut(st)
        return self

    # 拖拽到某个坐标然后松开
    def mouseDrag_And_By_Offset(self,x:int,y:int):
        ActionChains(self.__drive).drag_and_drop_by_offset(self.__ele,x,y).perform()
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,x,y)
        self.__is_trackingOut(st)
        return self

    # 模拟Key按下
    def simulationKeyDown(self,key:Key,ele:WebElement=None):
        if ele:
            ActionChains(self.__drive).key_down(key,ele).perform()
        elif self.__ele:
            ActionChains(self.__drive).key_down(key, self.__ele).perform()
        else:
            ActionChains(self.__drive).key_down(key).perform()
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,key)
        self.__is_trackingOut(st)
        return self

    # 模拟Key释放
    def simulationKeyUp(self, key: Key,ele:WebElement=None):
        if ele:
            ActionChains(self.__drive).key_up(key,ele).perform()
        elif self.__ele:
            ActionChains(self.__drive).key_up(key, self.__ele).perform()
        else:
            ActionChains(self.__drive).key_up(key).perform()
        ActionChains(self.__drive).key_up(key).perform()
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,key)
        self.__is_trackingOut(st)
        return self

    # 通过下标 匹配select菜单
    def selectIndex(self,index:int=0):
        Select(self.__ele).select_by_index(index)
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,index)
        self.__is_trackingOut(st)
        return self

    # 通过文本 匹配select菜单
    def selectVisText(self, text: str):
        Select(self.__ele).select_by_visible_text(text)
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime, text)
        self.__is_trackingOut(st)
        return self

    # 通过select菜单里面的value匹配
    def selectValue(self,value):
        Select(self.__ele).select_by_value(value)
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime, value)
        self.__is_trackingOut(st)
        return self

    # 滚动条
    def scroll(self,value:int=0):
        scroll_js = "document.documentElement.scrollTop={}".format(value)
        self.exec_script(scroll_js)
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime, value)
        self.__is_trackingOut(st)
        return self

    # 滚动条到底端
    def scrollBottom(self):
        self.scroll(10000)
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime)
        self.__is_trackingOut(st)
        return self

    # 滚动条到顶端
    def scrollTop(self):
        self.scroll(0)
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime)
        self.__is_trackingOut(st)
        return self

    # 滚动条向左移动
    def scrollLeftValue(self, value: int):
        js = "window.scrollTo(0,{})".format(value)
        self.exec_script(js)
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime,value)
        self.__is_trackingOut(st)
        return self

    # 滚动条向右移动
    def scrollRightValue(self, value: int):
        js = "window.scrollTo({},0)".format(value)
        self.exec_script(js)
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime, value)
        self.__is_trackingOut(st)
        return self

    # 滚动条向左移动
    def scrollLeft(self):
        self.scrollLeftValue(10000)
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime)
        self.__is_trackingOut(st)
        return self

    # 滚动条向右移动
    def scrollRight(self):
        self.scrollRightValue(10000)
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime)
        self.__is_trackingOut(st)
        return self

    # 处理checkbox 全选
    def checkboxAll(self):
        '''
        select all checkbox
        :return:
        '''
        for e in self.getEle():
            e = e  # type:ChromeSelenium
            e.click()
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime)
        self.__is_trackingOut(st)
        return self

    # 关闭浏览器
    def quit(self):
        st = Lan[self.__steps.language()][sys._getframe().f_code.co_name].format(self.currentTime)
        self.__is_trackingOut(st)
        self.__drive.quit()

    # 模拟下标
    def __getitem__(self, item):
        return self.getEle()[item]

    def __len__(self):
        if isinstance(self.getEle(),WebDriverWait):
            return 1
        if isinstance(self.getEle(),list):
            return len(self.getEle())

    def __iter__(self):
        return self

    def __next__(self):
        self.__index += 1
        if self.__index >= self.len:
            raise StopIteration()  # 触发异常,停止迭代
        else:
            return self.getEle()[self.__index]


