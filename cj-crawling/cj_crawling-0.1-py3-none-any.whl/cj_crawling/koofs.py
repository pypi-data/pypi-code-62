# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 22:09:01 2020

@author: cjcho
"""

import pandas as pd
from selenium import webdriver
import os, time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import datetime as dte
import re
import glob
#os.chdir(r'D:\임시보관')

class Driver_open():
    def __init__(self,download_dir,exe_path):
        self.exe_path=exe_path
        
        cnt=0
        while True:
            if os.path.isdir(f'{download_dir}\\koofs{str(cnt)}')==False:
                os.mkdir(f'{download_dir}\\koofs{str(cnt)}')
                break
            else: 
                cnt=cnt+1
                if cnt>100:
                    break
        download_dir=f'{download_dir}\\koofs{str(cnt)}\\'
        self.download_dir=download_dir
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {
          "download.default_directory":download_dir,
          "download.prompt_for_download": False,
          "download.directory_upgrade": True,
          "safebrowsing.enabled": True
        })
        self.driver=webdriver.Chrome(options=options,executable_path=self.exe_path)
        self.wait= WebDriverWait(self.driver, 10)
        
    def css_send_keys(self,css,keys):
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,css))).send_keys(keys)

    def get_text(self,css,n=None):
        temp=self.driver.find_elements_by_css_selector(css)
        if len(temp)>1:
            return temp[n].text
        else: 
            return self.driver.find_element_by_css_selector(css).text

    def click(self,css,n=None):
        temp=self.driver.find_elements_by_css_selector(css)
        if len(temp)>1:
            return temp[n].click()
        else: 
            return self.find_element_by_css_selector(css).click()

    def get_html_df(self):
        source=self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.past_rig2_box1_1")))[0]
        temp_df=(pd.read_html(source.get_attribute('innerHTML'),header=0))[0]
        self.temp_df=temp_df


    def main(self):        
        main=self.driver.window_handles[0]
        self.driver.switch_to.window(main)

    def dayType(self,DayTypes,download_type=1):
        self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input#ststistic_period")))[download_type].send_keys(Keys.SPACE)
        if download_type==1:
            DayType=self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select#dataDate.select")))
            DayType.send_keys(DayTypes)
        
    def dayRange(self):
        stDate=self.driver.find_element_by_css_selector('input#sDate.common_dateBox.hasDatepicker').get_attribute('value')
        edDate=self.driver.find_element_by_css_selector('input#eDate.common_dateBox.hasDatepicker').get_attribute('value')
        _stDate = dte.datetime.strptime(stDate, '%Y-%m-%d')
        _edDate = dte.datetime.strptime(edDate, '%Y-%m-%d')
        self.dateList=[i.strftime('%Y-%m-%d') for i in pd.date_range(start=_stDate, end=_edDate).to_list()]

    def file_down(self,station_list,station_type):
        self.log=list()
        self.check_list=list()

        def non_file_close(self):
            if len(self.driver.window_handles)>1:
                time.sleep(1)
                if len(self.driver.window_handles)>1:
                    try:
                        self.main()
                        for pop in range(1,len(self.driver.window_handles)):
                            self.driver.switch_to.window(self.driver.window_handles[pop])
                            self.driver.close()
                            time.sleep(4)
                            self.main()
                            time.sleep(2)
                        self.get_html_df()
                        temp_df=self.temp_df
                        self.log.append(', '.join(temp_df.iloc[i,1:4].values))
                    except:
                        1
        
        def cr_download_wait(p2,n=5):
            cnt1=0
            while True:
                if len([j for j in os.listdir(self.download_dir) if p2.findall(j)])>=1:
                    break
                else:
                    time.sleep(1)
                    cnt1=cnt1+1
                    if cnt1>n:
                        break
            
        def download_start(self,i,n=10):
            count1=0
            while count1<n:
                print('while start')
                try:
                    print('research click error')
                    research=self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table#dataListXscroll a")))[i]
                    while not research.is_enabled():
                        time.sleep(1)
                    print('click after error')
                    self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table#dataListXscroll a")))[i].click()
                    Select(self.driver.find_element_by_css_selector('select#FormJob')).select_by_value('수산업')
                    time.sleep(1)
                    Select(self.driver.find_element_by_css_selector('select#FormPurpose')).select_by_value('수산어업용')
                    time.sleep(1)
                    self.driver.execute_script('$javascript:checkPopupForm();')
                    break
                except:
                    try:
                        print('cencel error')
                        self.driver.execute_script('$javascript:cancelPopupForm();')
                        time.sleep(1)
                    except:
                        time.sleep(1)
                    count1+=1
                    print('count1_'+str(count1))
            
        def download_wait(self,p2):
            count3=0
            while True:
                try:
                    self.get_html_df()
                    temp_df=self.temp_df
                    Alert(self.driver).text
                    alert = self.driver.switch_to.alert
                    alert.accept()
                    self.log.append(', '.join(temp_df.iloc[i,1:4].values))
                except:
                    if len([j for j in os.listdir(self.download_dir) if p2.findall(j)])>=1:
                        time.sleep(1)
                        count3+=1
                        if count3>30:
                            self.log.append(', '.join(temp_df.iloc[i,1:4].values))
                            break
                    else:
                        time.sleep(1)
                        break
        for station in station_list:
                print(station)                    
                while True:
                    if self.driver.find_element_by_css_selector("select#observer2.select").is_enabled():
                        self.css_send_keys(css="select#observer2.select",keys=station)
                        self.driver.execute_script('$javascript:checkForm2();')
                        break
                    else:
                        time.sleep(1)
                time.sleep(2)
                self.driver.find_elements_by_css_selector('td')
                if len(self.driver.find_elements_by_css_selector('td.lt_text2'))==1:
                    time.sleep(2)
                    if self.get_text('td.lt_text2')=='알 수 없는 오류가 발생했습니다.':
                        self.log.append(station_type+', '+station)
                        time.sleep(1)
                        print(self.log[-1])
                    else:
                        1
                else:
                    print('어')
                    while True:
                        try:
                            self.get_html_df()
                            temp_df=self.temp_df
                            self.check_list.append(', '.join(temp_df.iloc[0,1:3])+', '+str(temp_df.shape[0]))
                            break
                        except:
                            time.sleep(1)
                    if temp_df.shape[0]!=0:
                        while station!=temp_df.iloc[0,2]:
                            try:
                                self.get_html_df()
                                temp_df=self.temp_df()
                            except:
                                time.sleep(1)
                        #자료 다운로드
                        for i in range(temp_df.shape[0]):
                            print('디')
                            #제대로 된 파일명
                            p=re.compile(temp_df.iloc[i,2].split(' ')[0]+'[가-힣|A-z|0-9|\\_| |\\+]*'+''.join(re.compile('[0-9]+').findall(temp_df.iloc[i,3]))+'.*.txt$')
                            #임시파일명
                            p2=re.compile(temp_df.iloc[i,2]+'[가-힣|A-z|0-9|\\_| |\\+]*'+''.join(re.compile('[0-9]+').findall(temp_df.iloc[i,3]))+'.*.txt.crdownload$')
                            before=len([j for j in os.listdir(self.download_dir) if re.compile('[가-힣]+.*.txt$').findall(j)])
                #            count2=0
                            print('가')
                            count4=0
                            while True:
                                download_start(self,i=i,n=10)
                                print('에')
                                non_file_close(self)
                                cr_download_wait(p2,n=5)
                                print('있')
                                download_wait(self,p2)
                                #파일 다운로드가 실행됨
                                if len([j for j in os.listdir(self.download_dir) if p.findall(j)])>=1:
                                    #파일 다운로드가 됬고 임시파일이 사라졌으면 다운로드 끝
                                    after=len([j for j in os.listdir(self.download_dir) if re.compile('[가-힣]+.*.txt$').findall(j)])
                                    if before==after:
                                        count4+=1
                                        if count4>4:
                                            self.log.append(', '.join(temp_df.iloc[i,1:4].values))
                                            print(self.log[-1])
                                    else: 
                                        break
                                time.sleep(1)
                    else:
                        self.log.append(station_type+', '+station)
                        print(self.log[-1])


##
    def file_down2(self,dateList,station,station_type,data_type='.csv'):
        naDate=[]    
        for date in dateList:
            print(date)
            if date in dateList:
                try:
                    self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "select#pDate.obs_select_date")))
                    self.driver.find_element_by_css_selector('select#pDate.obs_select_date').send_keys(date)
                except:
                    pass
                _stop=0;count=0
                while _stop!=date:
                    count+=1
                    try:
                        source=self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.past_rig2_box1_1")))[0]
                        temp_df=(pd.read_html(source.get_attribute('innerHTML'),header=0))[0]
                    except:
                        1
                    time.sleep(1)
                    _stop=temp_df.iloc[1,0][0:10]
                    if _stop==date:
                        break
                    if count%10==0:
                        self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "select#pDate.obs_select_date")))
                        self.driver.find_element_by_css_selector('select#pDate.obs_select_date').send_keys(date)
                        time.sleep(1)
                if temp_df.shape[0]==1440:
                    temp_df['관측시간']=pd.to_datetime(temp_df['관측시간'],format='%Y-%m-%d %H:%M')
                    temp_df.sort_values(by='관측시간')
                    temp_df.to_csv(self.download_dir+station+'_'+station_type+re.sub('-','',date)+data_type,encoding='cp949')
                else:
                    temp_df['관측시간']=pd.to_datetime(temp_df['관측시간'],format='%Y-%m-%d %H:%M')
                    temp_df2=pd.DataFrame({'관측시간':pd.date_range(start=date, end=dte.datetime.strptime(date, '%Y-%m-%d')+dte.timedelta(1),freq='min')[0:-1][::-1]})
                    temp_df3=pd.merge(temp_df,temp_df2,how='right').sort_values(by='관측시간')
                    temp_df3.to_csv(self.download_dir+station+'_'+station_type+re.sub('-','',date)+data_type,encoding='cp949')
                    print('결측치 존재')
                    naDate.append(date)
            else:
                temp_df2=pd.DataFrame({'관측시간':pd.date_range(start=date, end=dte.datetime.strptime(date, '%Y-%m-%d')+dte.timedelta(1),freq='min')[0:-1][::-1]})
                temp_df2.to_csv(self.download_dir+station+'_'+station_type+re.sub('-','',date)+data_type,encoding='cp949')
        
        allFile=glob.glob(os.path.join(self.download_dir,'*[0-9]'+data_type))
        allData=[]
        for file in allFile:
            print(file)
            df=pd.read_csv(file,engine='python',encoding='cp949')
            df=df.sort_values(by='관측시간',ascending=False)
            allData.append(df.iloc[:,1:])
        dataCombine=pd.concat(allData,axis=0,ignore_index=False)
        dataCombine=dataCombine.sort_values(by='관측시간',ascending=True)
        dataCombine.to_csv(self.download_dir+'total_file'+data_type,index=False,encoding='cp949')
        self.dataCombine=dataCombine
#def to_date(char,form='%Y%m%d'):
#    return dte.datetime.strptime(char,form)
#
#def to_char_date(char,out_form,form='%Y%m%d'):
#    try:
#        temp=dte.datetime.strptime(char,form).strftime(out_form)
#    except:
#        temp=char.strftime(out_form)
#    return temp