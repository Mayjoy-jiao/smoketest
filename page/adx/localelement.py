from selenium import webdriver
import time
def a():
    dr=webdriver.Chrome()
    dr.get("http://192.168.0.245:8585/login#configPubAppAdNew")
    # 登陆
    dr.find_element_by_id("loginName").send_keys("wangyufen")
    dr.find_element_by_id("password").send_keys("Wangyufen0527")
    dr.find_element_by_id("validateCode").send_keys("9527")
    dr.find_element_by_class_name("btn").click()
    dr.maximize_window()
    time.sleep(3)
    # 打开“开发者广告位管理”页面
    dr.find_element_by_xpath('//*[@id="sidebar"]/div[2]/div[2]/ul[4]/li/ul/li[3]/div/a').click()
    time.sleep(3)
    # 查找指定广告位
    dr.find_element_by_xpath('//*[@id="pubAppAdSoltForm"]/div/table/tbody/tr[1]/td[1]/input').send_keys("tikv1jna")
    dr.find_element_by_class_name("buttonContent").click()
    time.sleep(3)

    #获取搜索广告位的记录,并存放到列表中，用于广告配置（新）页面的，开发者等信息的断言
    info = dr.find_element_by_xpath('//*[@id="navTab"]/div[2]/div[2]/div[2]/div[2]/div[2]/div/table/tbody/tr').text
    info_list = info.split("\n")
    print(info_list)

    #点击广告配置（新）的链接，进入【广告配置（新）】页面
    dr.find_element_by_class_name("navTab-link").click()
    time.sleep(20)

    # 切换到框架中
    ifram = dr.find_elements_by_tag_name("iframe")[0]
    dr.switch_to_frame(ifram)

    # 获取顶部展示广告位的信息
    title = dr.find_element_by_xpath("/html/body/div[1]/div/form[1]/div[1]/div/div[1]/span").text
    print(title)

    # 获取同时请求数，和竞价比例的属性，确定是输入框
    attribute_name1 = dr.find_element_by_xpath("/html/body/div[1]/div/form[1]/div[3]/div[1]/div/div/div/input").get_attribute("type")
    attribute_name2 = dr.find_element_by_xpath("/html/body/div[1]/div/form[1]/div[3]/div[2]/div/div/div/input").get_attribute("type")
    attribute_value = dr.find_element_by_xpath("/html/body/div[1]/div/form[1]/div[3]/div[2]/div/div/div/input").get_attribute("value")
    print(attribute_name1)
    print(attribute_name2)
    print(attribute_value)

    #保存请求数和竞价比例
    dr.find_element_by_xpath("/html/body/div[1]/div/form[1]/div[3]/div[1]/div/div/div/input").clear()
    dr.find_element_by_xpath("/html/body/div[1]/div/form[1]/div[3]/div[1]/div/div/div/input").send_keys(4)
    time.sleep(2)
    dr.find_element_by_xpath("/html/body/div[1]/div/form[1]/div[3]/div[2]/div/div/div/input").clear()
    dr.find_element_by_xpath("/html/body/div[1]/div/form[1]/div[3]/div[2]/div/div/div/input").send_keys(80)
    time.sleep(2)
    dr.find_element_by_xpath("/html/body/div[1]/div/form[1]/div[3]/div[4]/div/div/button").click()
    time.sleep(2)
    dr.find_element_by_xpath("/html/body/div[1]/div/form[1]/div[3]/div[5]/div/div/button").click()
    time.sleep(4)

    # 获取测试广告的广告名称
    js ='document.getElementsByClassName("ivu-input-disabled").disabled = false;'
    dr.execute_script(js)
    s = dr.find_element_by_class_name("ivu-input-disabled").get_property("disabled")
    print(s)
    test_ad = dr.find_element_by_xpath("/html/body/div[1]/div/form[1]/div[3]/div[3]/div/div/div/div/div[1]/input").text
    print(test_ad)

    # 搜索dsp功能
    dr.find_element_by_xpath("/html/body/div[1]/div/form[2]/div/div[1]/div/div/div/div[1]/div/input").click()
    dsp_li = dr.find_element_by_xpath("/html/body/div[1]/div/form[2]/div/div[1]/div/div/div/div[2]/ul[2]/li[4]")
    dsp_li.click()
    dsp_s = dsp_li.text
    print(dsp_s)
    time.sleep(2)
    dsp_rowcount = len(dr.find_elements_by_xpath("/html/body/div[1]/div/div[1]/div/div[2]/table/tbody/tr"))
    print(dsp_rowcount)
    dr.find_element_by_xpath("/html/body/div[1]/div/form[1]/div[3]/div[5]/div/div/button").click()
    time.sleep(3)


    # 搜索dsp应用功能
    dr.find_element_by_xpath("/html/body/div[1]/div/form[2]/div/div[2]/div/div/div/div[1]/div/input").click()
    # 选择第二项
    dsp_app_li = dr.find_element_by_xpath("/html/body/div[1]/div/form[2]/div/div[2]/div/div/div/div[2]/ul[2]/li[2]")
    dsp_app_li.click()
    dsp_app_s = dsp_app_li.text
    print(dsp_app_s)
    time.sleep(3)
    dsp_app_rowcount = len(dr.find_elements_by_xpath("/html/body/div[1]/div/div[1]/div/div[2]/table/tbody/tr"))
    print(dsp_app_rowcount)
    dr.find_element_by_xpath("/html/body/div[1]/div/form[1]/div[3]/div[5]/div/div/button").click()
    time.sleep(3)

    # 搜索dsp类型功能
    dr.find_element_by_xpath("/html/body/div[1]/div/form[2]/div/div[3]/div/div/div/div[1]/div/span").click()
    dsp_type_li = dr.find_element_by_xpath("/html/body/div[1]/div/form[2]/div/div[3]/div/div/div/div[2]/ul[2]/li[2]")
    dsp_type_li.click()
    dsp_type_s = dsp_type_li.text
    print(dsp_type_s)
    time.sleep(2)
    dsp_type_rowcount = len(dr.find_elements_by_xpath("/html/body/div[1]/div/div[1]/div/div[2]/table/tbody/tr"))
    print(dsp_type_rowcount)
    dr.find_element_by_xpath("/html/body/div[1]/div/form[1]/div[3]/div[5]/div/div/button").click()
    time.sleep(3)

    # 搜索是否全时段功能
    dr.find_element_by_xpath("/html/body/div[1]/div/form[2]/div/div[4]/div/div/div/div[1]").click()
    dsp_type_li = dr.find_element_by_xpath("/html/body/div[1]/div/form[2]/div/div[4]/div/div/div/div[2]/ul[2]/li[3]")
    dsp_type_li.click()
    dsp_type_s = dsp_type_li.text
    print(dsp_type_s)
    time.sleep(2)
    is_fultime_rowcount = len(dr.find_elements_by_xpath("/html/body/div[1]/div/div[1]/div/div[2]/table/tbody/tr"))
    print(is_fultime_rowcount)
    dr.find_element_by_xpath("/html/body/div[1]/div/form[1]/div[3]/div[5]/div/div/button").click()
    time.sleep(3)

    # 打开dsp的开关，并点击保存
    value = dr.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[2]/table/tbody/tr[1]/td[12]/div/div/span/input").get_attribute("value")
    print(value)
    if value =="false":
        dr.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[2]/table/tbody/tr[1]/td[12]/div/div/span/span/span").click()
        time.sleep(3)
        dr.find_element_by_xpath('//*[@id="saveAButton + {index}"]/span').click()
        time.sleep(3)
        value = dr.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[2]/table/tbody/tr[1]/td[12]/div/div/span/input").get_attribute("value")
    else:
        pass
    print(value)

    ad = dr.find_element_by_xpath('/html/body/div[1]/div/form[1]/div[3]/div[3]/div/div/div/div/div[1]/input').get_attribute("value")
    print(f"挑选的测试广告是：{ad}")

    # # 点击选择测试广告
    # dr.find_element_by_xpath("/html/body/div[1]/div/form[1]/div[3]/div[3]/div/div/div/div/div[1]/div/span/a/i").click()
    # time.sleep(3)
    # dr.find_element_by_xpath("/html/body/div[7]/div[2]/div/div/div[2]/div/div/div[2]/table/tbody/tr[1]/td[1]/div/label/span/input").click()
    # # dr.find_element_by_xpath("/html/body/div[7]/div[2]/div/div/div[2]/div/div/div[2]/table/tbody/tr[1]/td[1]/div/label").click()
    # time.sleep(3)
    # dr.find_element_by_xpath("/html/body/div[7]/div[2]/div/div/a").click()


if __name__ == '__main__':
    a()