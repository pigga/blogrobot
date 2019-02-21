#! /usr/bin/env python  
# -*- coding:utf-8 -*-  
# ====#====#====#====
# __author__ = "Yannis"  
# FileName: *.py  
# Version:1.0.0
# ====#====#====#====
import time
import random
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import requests
from io import BytesIO
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
"""
作者：星星在线
来源：CSDN
原文：https://blog.csdn.net/wuqing942274053/article/details/80425709
版权声明：本文为博主原创文章，转载请附上博文链接！

goolge drive的地址 http://chromedriver.storage.googleapis.com/index.html
"""


class CNBlogSelenium(object):
    def __init__(self, user_name, pwd):
        self.user_name = user_name
        self.pwd = pwd
        opt = webdriver.ChromeOptions()
        # 设置无头模式，调试的时候可以注释这句
        # opt.set_headless()
        self.driver = webdriver.Chrome(executable_path=r"/usr/lib/chromedriver", chrome_options=opt)
        self.driver.set_window_size(1440, 900)

        # 拼接图片
        def mosaic_image(self, image_url, location):
            resq = requests.get(image_url)
            file = BytesIO(resq.content)
            img = Image.open(file)
            image_upper_lst = []
            image_down_lst = []
            for pos in location:
                if pos[1] == 0:
                    # y值==0的图片属于上半部分，高度58
                    image_upper_lst.append(
                        img.crop((abs(pos[0]), 0, abs(pos[0]) + 10, 58)))
                else:
                    # y值==58的图片属于下半部分
                    image_down_lst.append(img.crop(
                        (abs(pos[0]), 58, abs(pos[0]) + 10, img.height)))

            x_offset = 0
            # 创建一张画布，x_offset主要为新画布使用
            new_img = Image.new("RGB", (260, img.height))
            for img in image_upper_lst:
                new_img.paste(img, (x_offset, 58))
                x_offset += img.width

            x_offset = 0
            for img in image_down_lst:
                new_img.paste(img, (x_offset, 0))
                x_offset += img.width

            return new_img

    def visit_login(self):
        self.driver.get("https://passport.cnblogs.com/user/signin")
        WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="input1"]')))
        username = self.driver.find_element_by_xpath('//*[@id="input1"]')
        username.clear()
        username.send_keys(self.user_name)
        WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="input2"]')))
        password = self.driver.find_element_by_xpath('//*[@id="input2"]')
        password.clear()
        password.send_keys(self.pwd)
        WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="signin"]')))
        signin = self.driver.find_element_by_xpath('//*[@id="signin"]')
        signin.click()
        WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="geetest_radar_tip_content"]')))
        geetest = self.driver.find_element_by_xpath('//*[@class="geetest_radar_tip_content"]')
        geetest.click()
        # 点击滑动验证码后加载图片需要时间
        time.sleep(3)
        self.analog_move()
        # self.driver.quit()

    def analog_move(self):
        distance = self.screenshot_processing()
        element = self.driver.find_element_by_xpath(
            '//*[@class="geetest_slider_button"]')
        self.start_move(distance, element)

        # 判断是否登录成功
        tip_btn = self.driver.find_element_by_xpath('//*[@id="tip_btn"]')
        if tip_btn.text.find("登录成功") == -1:
            WebDriverWait(self.driver, 3, 0.5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@class="geetest_reset_tip_content"]')))
            reset_btn = self.driver.find_element_by_xpath(
                '//*[@class="geetest_reset_tip_content"]')
            # 判断是否需要重新打开滑块框
            if reset_btn.text.find("重试") != -1:
                reset_btn.click()
            else:
                time.sleep(1)
            # 刷新滑块验证码图片
            refresh_btn = self.driver.find_element_by_xpath(
                '//*[@class="geetest_refresh_1"]')
            refresh_btn.click()
            time.sleep(0.5)

            # 重新进行截图、分析、计算、拖动处理
            self.analog_move()
        else:
            print("登录成功")

    # 判断颜色是否相近
    def is_similar_color(self, x_pixel, y_pixel):
        for i, pixel in enumerate(x_pixel):
            if abs(y_pixel[i] - pixel) > 50:
                return False
        return True

    # 计算距离
    def get_offset_distance(self, cut_img, full_img):
        x, y = 1, 1
        find_one = False
        top = 0
        left = 0
        right = 0
        while x < cut_img.width:
            y = 1
            while y < cut_img.height:
                cpx = cut_img.getpixel((x, y))
                fpx = full_img.getpixel((x, y))
                if abs(cpx - fpx) > 50:
                    if not find_one:
                        find_one = True
                        x += 60
                        y -= 10
                        continue
                    else:
                        if left == 0:
                            left = x
                            top = y
                        right = x
                        break
                y += 1
            x += 1
        # return left, right - left
        return right - left

    # 截图处理
    def screenshot_processing(self):
        element = self.driver.find_element_by_xpath(
            '//canvas[@class="geetest_canvas_fullbg geetest_fade geetest_absolute"]')

        # 保存登录页面截图
        self.driver.get_screenshot_as_file("login.png")
        image = Image.open("login.png")

        # 打开截图，获取element的坐标和大小
        left = element.location.get("x")
        top = element.location.get("y")
        right = left + element.size.get("width")
        bottom = top + element.size.get("height")

        # 对此区域进行截图，然后灰度处理
        cropImg = image.crop((left, top, right, bottom))
        full_Img = cropImg.convert("L")
        full_Img.save("fullimage.png")
        # 缺口位置
        element = self.driver.find_element_by_xpath(
            '//canvas[@class="geetest_canvas_slice geetest_absolute"]')

        self.driver.get_screenshot_as_file("login.png")
        image = Image.open("login.png")
        left = element.location.get("x")
        top = element.location.get("y")
        right = left + element.size.get("width")
        bottom = top + element.size.get("height")
        cropImg = image.crop((left, top, right, bottom))
        cut_Img = cropImg.convert("L")
        cut_Img.save("cutimage.png")
        distance = self.get_offset_distance(cut_Img, full_Img)
        return distance

    def start_move(self, distance, element, click_hold=False):
        # 这里就是根据移动进行调试，计算出来的位置不是百分百正确的，加上一点偏移
        distance -= 7
        # 按下鼠标左键
        if click_hold:
            ActionChains(self.driver).click_and_hold(element).perform()
        print '--=====-----'
        while distance > 0:
            if distance > 10:
                # 如果距离大于10，就让他移动快一点
                span = random.randint(5, 8)
            else:
                time.sleep(random.randint(10, 50) / 100)
                # 快到缺口了，就移动慢一点
                span = random.randint(2, 3)
            ActionChains(self.driver).move_by_offset(span, 0).perform()
            distance -= span
        ActionChains(self.driver).move_by_offset(distance, 1).perform()
        ActionChains(self.driver).release(on_element=element).perform()
        print '--======---------------'


CNBlogSelenium('Yannis-chen', 'Chen@384915').visit_login()
