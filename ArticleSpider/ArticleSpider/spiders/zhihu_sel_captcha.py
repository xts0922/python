# -*- coding: utf-8 -*-
import re
import json
import datetime
import time
try:
    import urlparse as parse
except:
    from urllib import parse

import scrapy
from scrapy.loader import ItemLoader
from items import ZhihuQuestionItem, ZhihuAnswerItem
from selenium.webdriver.common.keys import Keys


class ZhihuSpider(scrapy.Spider):
    name = "zhihu_sel"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com/']

    #question的第一页answer的请求url
    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}"

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    custom_settings = {
        "COOKIES_ENABLED": True
    }

    def parse(self, response):
        """
        提取出html页面中的所有url 并跟踪这些url进行一步爬取
        如果提取的url中格式为 /question/xxx 就下载之后直接进入解析函数
        """
        pass

    def parse_question(self, response):
        #处理question页面， 从页面中提取出具体的question item
       pass

    def parse_answer(self, reponse):
        pass

    def start_requests(self):
        from selenium import webdriver
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.chrome.options import Options

        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        #chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        #browser = webdriver.Chrome(executable_path="E:/chromedriver/chromedriver_win32/chromedriver.exe",  chrome_options=chrome_options)
        browser = webdriver.Chrome(executable_path="E:/chromedriver/chromedriver_win32/chromedriver.exe")
        import time
        try:
            browser.maximize_window() #将窗口最大化防止定位错误
        except:
            pass
        browser.get("https://www.zhihu.com/signin")
        logo_element = browser.find_element_by_class_name("SignFlowHeader")
        # y_relative_coord = logo_element.location['y']
        browser_navigation_panel_height = browser.execute_script('return window.outerHeight - window.innerHeight;')
        browser_navigation_panel_height = 71
        time.sleep(5)
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(Keys.CONTROL + "a")
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
            "xxx")

        browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + "a")
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys(
            "xxx")

        browser.find_element_by_css_selector(
            ".Button.SignFlow-submitButton").click()
        time.sleep(15)
        from mouse import move, click
        # move(800, 400 ,True)
        # actions = ActionChains(browser)
        # actions.move_to_element(browser.find_element_by_css_selector(
        #     ".Button.SignFlow-submitButton"))
        # actions.click(browser.find_element_by_css_selector(
        #     ".Button.SignFlow-submitButton"))
        # actions.perform()
        # actions.move_to_element_with_offset(browser.find_element_by_css_selector(
        #     ".Button.SignFlow-submitButton"), 30, 30).perform()
        #chrome的版本问题有两种解决方案
        #1. 自己启动chrome(推荐) 可以防止chromedriver被识别，因为chromedriver出现的一些js变量可以被服务器识别出来
        #2. 使用chrome60(版本)

        # 先判断是否登录成功
        login_success = False
        while not login_success:
            try:
                notify_element = browser.find_element_by_class_name("Popover PushNotifications AppHeader-notifications")
                login_success = True
            except:
                pass

            try:
                #查询是否有英文验证码
                english_captcha_element = browser.find_element_by_class_name("Captcha-englishImg")
            except:
                english_captcha_element = None
            try:
                # 查询是否有中文验证码
                chinese_captcha_element = browser.find_element_by_class_name("Captcha-chineseImg")
            except:
                chinese_captcha_element = None

            if chinese_captcha_element:
                y_relative_coord = chinese_captcha_element.location['y']
                y_absolute_coord = y_relative_coord + browser_navigation_panel_height
                x_absolute_coord = chinese_captcha_element.location['x']
                # x_absolute_coord = 842
                # y_absolute_coord = 428

                """
                保存图片
                1. 通过保存base64编码
                2. 通过crop方法
                """
                # 1. 通过保存base64编码
                base64_text = chinese_captcha_element.get_attribute("src")
                import base64
                code = base64_text.replace('data:image/jpg;base64,', '').replace("%0A", "")
                # print code
                fh = open("yzm_cn.jpeg", "wb")
                fh.write(base64.b64decode(code))
                fh.close()

                from zheye import zheye
                z = zheye()
                positions = z.Recognize("yzm_cn.jpeg")

                pos_arr = []
                if len(positions) == 2:
                    if positions[0][1] > positions[1][1]:
                        pos_arr.append([positions[1][1], positions[1][0]])
                        pos_arr.append([positions[0][1], positions[0][0]])
                    else:
                        pos_arr.append([positions[0][1], positions[0][0]])
                        pos_arr.append([positions[1][1], positions[1][0]])
                else:
                    pos_arr.append([positions[0][1], positions[0][0]])

                if len(positions) == 2:
                    first_point = [int(pos_arr[0][0] / 2), int(pos_arr[0][1] / 2)]
                    second_point = [int(pos_arr[1][0] / 2), int(pos_arr[1][1] / 2)]

                    move((x_absolute_coord + first_point[0]), y_absolute_coord + first_point[1])
                    click()

                    move((x_absolute_coord + second_point[0]), y_absolute_coord + second_point[1])
                    click()

                else:
                    first_point = [int(pos_arr[0][0] / 2), int(pos_arr[0][1] / 2)]

                    move((x_absolute_coord + first_point[0]), y_absolute_coord + first_point[1])
                    click()

                browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                    Keys.CONTROL + "a")
                browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                    "xxx")

                browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + "a")
                browser.find_element_by_css_selector(".SignFlow-password input").send_keys(
                    "xxx")
                browser.find_element_by_css_selector(
                    ".Button.SignFlow-submitButton").click()
                browser.find_element_by_css_selector(
                    ".Button.SignFlow-submitButton").click()

            if english_captcha_element:
                # 2. 通过crop方法
                # from pil import Image
                # image = Image.open(path)
                # image = image.crop((locations["x"], locations["y"], locations["x"] + image_size["width"],
                #                     locations["y"] + image_size["height"]))  # defines crop points
                #
                # rgb_im = image.convert('RGB')
                # rgb_im.save("D:/ImoocProjects/python_scrapy/coding-92/ArticleSpider/tools/image/yzm.jpeg",
                #             'jpeg')  # saves new cropped image
                # # 1. 通过保存base64编码
                base64_text = english_captcha_element.get_attribute("src")
                import base64
                code = base64_text.replace('data:image/jpg;base64,', '').replace("%0A", "")
                # print code
                fh = open("yzm_en.jpeg", "wb")
                fh.write(base64.b64decode(code))
                fh.close()

                from tools.yundama_requests import YDMHttp
                yundama = YDMHttp("da_ge_da1", "dageda", 3129, "40d5ad41c047179fc797631e3b9c3025")
                code = yundama.decode("yzm_en.jpeg", 5000, 60)
                while True:
                    if code == "":
                        code = yundama.decode("yzm_en.jpeg", 5000, 60)
                    else:
                        break

                browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[3]/div/div/div[1]/input').send_keys(code)

                browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                    Keys.CONTROL + "a")
                browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                    "xxx")

                browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + "a")
                browser.find_element_by_css_selector(".SignFlow-password input").send_keys(
                    "xxx")
                submit_ele = browser.find_element_by_css_selector(".Button.SignFlow-submitButton")
                browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()

            time.sleep(10)
            try:
                notify_element = browser.find_element_by_class_name("Popover PushNotifications AppHeader-notifications")
                login_success = True

                Cookies = browser.get_cookies()
                print(Cookies)
                cookie_dict = {}
                import pickle
                for cookie in Cookies:
                    # 写入文件
                    # 此处大家修改一下自己文件的所在路径
                    f = open('./ArticleSpider/cookies/zhihu/' + cookie['name'] + '.zhihu', 'wb')
                    pickle.dump(cookie, f)
                    f.close()
                    cookie_dict[cookie['name']] = cookie['value']
                browser.close()
                return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]
            except:
                pass

        print("yes")
