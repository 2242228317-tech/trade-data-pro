list_name=driver.find_elements_by_android_uiautomator('new UiSelector().className("android.support.v7.app.ActionBar$Tab").childSelector(new UiSelector().className("android.widget.TextView"))')
# 机构 白马 游资 庄股 温州帮
print(list_name)
for i in list_name:
    print(i.text)

baima_button=driver.find_element_by_android_uiautomator('new UiSelector().className("android.support.v7.app.ActionBar$Tab").childSelector(new UiSelector().textContains("机构"))')
baima_button.click()

baima_gp_list=driver.find_elements_by_android_uiautomator('new UiSelector().resourceId("com.quchaogu.dxw:id/adapter_new_ch_layout_item_left_stock_code")')
print("当前页有{}个股票".format(len(baima_gp_list)))
for i in baima_gp_list:
    print(i.text)

from appium import webdriver
from appium.webdriver.extensions.android.nativekey import AndroidKey
desired_caps = {
  'platformName': 'Android', # 被测手机是安卓
  'platformVersion': '5.1.1', # 手机安卓版本
  'deviceName': 'xxx', # 设备名，安卓手机可以随意填写
  'appPackage': 'com.quchaogu.dxw', # 启动APP Package名称
  'appActivity': '.main.MainActivity', # 启动Activity名称
#   'unicodeKeyboard': True, # 使用自带输入法，输入中文时填True
#   'resetKeyboard': True, # 执行完程序恢复原来输入法
  'noReset': True,       # 不要重置App
#   'newCommandTimeout': 6000,
  'skipServerInstallation':True,
#   'automationName' : 'UiAutomator2'
  # 'app': r'd:\apk\bili.apk',
}

# 连接Appium Server，初始化自动化环境
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
# find_element_by_class_name("android.widget.RelativeLayout").click()
import time
time.sleep(15)
driver.implicitly_wait(18)
driver.find_element_by_id("tab_home_zixuan").click()
a_click=driver.find_element_by_id("adapter_new_ch_layout_item_left_img")
a_click.click()
print("成功切换到游资模式")

list_name=driver.find_elements_by_android_uiautomator('new UiSelector().className("android.support.v7.app.ActionBar$Tab").childSelector(new UiSelector().className("android.widget.TextView"))')
# 机构 白马 游资 庄股 温州帮
print(list_name)
baima_button=driver.find_element_by_android_uiautomator('new UiSelector().className("android.support.v7.app.ActionBar$Tab").childSelector(new UiSelector().textContains("机构"))')
baima_button.click()    
baima_gp_list=driver.find_elements_by_android_uiautomator('new UiSelector().resourceId("com.quchaogu.dxw:id/adapter_new_ch_layout_item_left_stock_code")')
print("当前页有{}个股票".format(len(baima_gp_list)))
for i in baima_gp_list:
    print(i.text)

#翻页1-2：
list_1=baima_gp_list[0]
list_2=baima_gp_list[len(baima_gp_list)-1]
driver.drag_and_drop(list_2,list_1)

#翻页第2以后：
    for i in range(3):#第二页循环
        baima_gp_list_2=driver.find_elements_by_android_uiautomator('new UiSelector().resourceId("com.quchaogu.dxw:id/adapter_new_ch_layout_item_left_stock_code")')
        print("-----------------当前页有{}个股票".format(len(baima_gp_list_2)))
        list_2_1=baima_gp_list_2[0]
        list_2_2=baima_gp_list_2[len(baima_gp_list_2)-1]
        driver.drag_and_drop(list_2_2,list_2_1)
        for i in baima_gp_list_2:
            print(i.text)
            list_i_text.append(i.text)
        print("休眠5秒")
        time.sleep(5)
