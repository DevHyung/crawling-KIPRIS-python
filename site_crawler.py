import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
## Parameter variable
query = '자동차'

if __name__ == "__main__":
    # 드라이버 설정
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory": os.getcwd() }
    chromeOptions.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path="./chromedriver", chrome_options=chromeOptions)
    driver.maximize_window()
    """_____________1번까지의 내용________________시작"""
    # 특허실용 부분 검색사이트로 이동
    driver.get('http://kportal.kipris.or.kr/kportal/search/total_search.do')
    driver.implicitly_wait(5)
    # Element 찾은후 send keyu
    driver.find_element_by_xpath('//*[@id="searchKeyword"]').send_keys(query+Keys.ENTER)
    time.sleep(1)
    #특허실용부분만 클릭
    driver.find_element_by_xpath('//*[@id="searchPatentBtn"]/button/span[1]').click()
    time.sleep(1)
    # 검색 결과후 a태그 클릭 부분
    driver.find_element_by_xpath('//*[@id="patentResultList"]/article[1]/div/div[1]/h1/a').click()
    # 팝업창으로 focusing이동
    main_window_handle = None
    while not main_window_handle:
        main_window_handle = driver.current_window_handle
    popup_window_handle = None
    while not popup_window_handle:
        for handle in driver.window_handles:
            if handle != main_window_handle:
                popup_window_handle = handle
                break
    driver.switch_to.window(popup_window_handle)
    #통합행정정보 탭클릭
    driver.find_element_by_xpath('//*[@id="liView09"]/a').click()
    time.sleep(1)
    # 프레임 iframe 으로 이동
    iframe = driver.find_element_by_tag_name('iframe')
    driver.switch_to_frame(iframe)
    driver.find_element_by_xpath('//*[@id="container"]/table/tbody/tr[1]/td[2]/a/img').click()
    """_____________1번까지의 내용________________끝"""
    """_____________2번까지의 내용________________시작"""
    #   ref
    #   관련자료    http://kthan.tistory.com/176 - 캡챠우회 관련 pytesser lib
    #   관련자료    http://blog.alyac.co.kr/997 - 구글 API 이용, 구글 re캡챠 우회
    #   실제사용해봄   https://github.com/lorien/captcha_solver - antigate 외부 API이용 뚫는거 1회 1원 소요
    #   실제사용해봄   https://github.com/JasonLiTW/simple-railway-captcha-solver - CNN 러닝이용한 우회
    #  ___________________________________________________________

    # 새로운 popup(캡챠뜬) 으로 switching
    captcha_window_handle = None
    while not captcha_window_handle:
        for handle in driver.window_handles:
            if handle != main_window_handle and handle != popup_window_handle:
                captcha_window_handle = handle
                break
    driver.switch_to.window(captcha_window_handle)
    # 프레임 iframe 으로 이동
    iframe = driver.find_element_by_tag_name('iframe')
    driver.switch_to_frame(iframe)
    bs4 = BeautifulSoup(driver.page_source,'lxml')
    img = bs4.find('img')
    # 1번방법
    # 이미지링크 가져오고나서 파일 다운로드후 CNN , openCV 이용해서 뚫으면
    # 충분히 우회가능합니다. 캡챠가 노이즈도 적은편이고, 요청한 시간에 적당한
    # 알고리즘 대입해서 유한된 캡챠가 발생된거같음
    print("링크:",'http://kpat.kipris.or.kr'+img['src'])
    driver.switch_to_default_content()
    # 2번방법
    # 캡차를 손으로 입력
    """
    captcha = input("캡챠 문자를 입력하세요 : ")
    driver.find_element_by_xpath('//*[@id="answer"]').send_keys(captcha+Keys.ENTER)
    time.sleep(3)
    """
    # 3번방법
    # 아래의 스크립트 코드를 실행시키면 됨
    # 이건 웹보안상의 취약점임
    time.sleep(5)
    bs4 = BeautifulSoup(driver.page_source, 'lxml')
    txt = str(bs4.find_all('script')[2].get_text())
    # 필요없는 문자제거및 문서고유번호 추출
    src = txt.split('document.getElementById("pdfViewFrame").src = "')[1].split('";')[0]
    src =src.replace('amp;','')
    # 캡챠 우회하는 스크립트 jquery 이용
    script ='$("#pdfViewFrame").show();\
    $("#bgBox").css("display","none");\
    $("#simpleCaptcha").css("display","none");\
    showPopLoadingBar();\
    document.getElementById("pdfViewFrame").src = "'+src+'";\
    resizeH();'
    driver.execute_script(script)
    time.sleep(5)
    # 다운로드 받기
    options = webdriver.ChromeOptions()
    profile = {"plugins.plugins_list": [{"enabled": False,
                                         "name": "Chrome PDF Viewer"}],
               "download.default_directory": os.getcwd(),
               "download.extensions_to_open": ""}
    options.add_experimental_option("prefs", profile)
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(
        'http://kpat.kipris.or.kr'+src)

    """_____________2번까지의 내용________________끝"""

    time.sleep(10)
    driver.quit()

