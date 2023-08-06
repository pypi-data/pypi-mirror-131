[TOC]
### CSelenium
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

UpdateTime: 2021.12.20

Simplify native Selenium operations to locate elements in a shorter manner
Make the code look cleaner.

characteristics:

    Clean code,
    Code has and associated operations
```python
from Cselenium.CSelenium import ChromeSelenium

def test1():
    cs = ChromeSelenium()
    cs.get("http://www.baidu.com")
    cs.wait(2)
    cs.quit()


def test2():
    cs = ChromeSelenium()
    cs.get("http://www.baidu.com")
    cs.id("kw").send_keys("hello world")
    cs.wait(2)
    cs.quit()


def test3():
    cs = ChromeSelenium()
    cs.get("http://www.baidu.com")
    cs.id("kw").send_keys("hello world")
    cs.id("su").click()
    cs.wait(2)
    cs.quit()
```