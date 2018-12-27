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
"""
作者：星星在线
来源：CSDN
原文：https://blog.csdn.net/wuqing942274053/article/details/80425709
版权声明：本文为博主原创文章，转载请附上博文链接！

goolge drive的地址 http://chromedriver.storage.googleapis.com/index.html
"""


class SeleniumVerify(object):
    def __init__(self):
        opt = webdriver.ChromeOptions()
        # 设置无头模式，调试的时候可以注释这句
        # opt.set_headless()
        self.driver = webdriver.Chrome(executable_path=r"/usr1/webdrivers/chromedriver", chrome_options=opt)
        self.driver.set_window_size(1440, 900)

    def visit_login(self):
        try:
            self.driver.get("https://passport.cnblogs.com/user/signin")
            WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="input1"]')))
            username = self.driver.find_element_by_xpath('//*[@id="input1"]')
            username.clear()
            username.send_keys("账号")
            WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="input2"]')))
            password = self.driver.find_element_by_xpath('//*[@id="input2"]')
            password.clear()
            password.send_keys("密码")
            WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="signin"]')))
            signin = self.driver.find_element_by_xpath('//*[@id="signin"]')
            signin.click()
            WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="geetest_radar_tip_content"]')))
            geetest = self.driver.find_element_by_xpath('//*[@class="geetest_radar_tip_content"]')
            geetest.click()
            # 点击滑动验证码后加载图片需要时间
            time.sleep(3)
            self.analog_move()
        except:
            pass

        self.driver.quit()

    # 截图处理
    def screenshot_processing(self):
        WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable(
            (By.XPATH, '//canvas[@class="geetest_canvas_fullbg geetest_fade geetest_absolute"]')))
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
        WebDriverWait(self.driver, 10, 0.5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@class="geetest_slider_button"]')))
        move_btn = self.driver.find_element_by_xpath('//*[@class="geetest_slider_button"]')
        ActionChains(self.driver).move_to_element(move_btn).click_and_hold(move_btn).perform()
        WebDriverWait(self.driver, 10, 0.5).until(
            EC.element_to_be_clickable((By.XPATH, '//canvas[@class="geetest_canvas_slice geetest_absolute"]')))
        element = self.driver.find_element_by_xpath('//canvas[@class="geetest_canvas_slice geetest_absolute"]')
        self.driver.get_screenshot_as_file("login.png")
        image = Image.open("login.png")
        left = element.location.get("x")
        top = element.location.get("y")
        right = left + element.size.get("width")
        bottom = top + element.size.get("height")
        cropImg = image.crop((left, top, right, bottom))
        cut_Img = cropImg.convert("L")
        cut_Img.save("cutimage.png")

    def calc_cut_offset(self, cut_img, full_img):
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
        return left, right - left

    def start_move(self, distance, element, click_hold=False):
        # 这里就是根据移动进行调试，计算出来的位置不是百分百正确的，加上一点偏移
        distance -= 7
        print(distance)
        # 按下鼠标左键
        if click_hold:
            ActionChains(self.driver).click_and_hold(element).perform()

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