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
# #   'skipServerInstallation':True,
#   'automationName' : 'UiAutomator2'
  # 'app': r'd:\apk\bili.apk',
}

# 连接Appium Server，初始化自动化环境
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
# find_element_by_class_name("android.widget.RelativeLayout").click()
