import re
import cv2
import serial
import xlsxwriter

import numpy as np
import pandas as pd
import pytesseract as pp

from PIL import Image
from subprocess import call


arduino = serial.Serial('COM6', 9600)  # 포트 연결 시도
pp.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'   # Tesseract-OCR의 실행 파일 지정



def medicine_caution(diseases):
    """
    ocr을 통해 진단된 병명에 따른 약 조제 및 주의사항 인쇄
    """
    
    acrobat = "C:/Program Files (x86)/Adobe/Acrobat Reader DC\Reader/AcroRd32.exe" # 인쇄해줄 Acrobat 프로세스 실행
    printer = "Samsung M2020 Series (USB001)"                                      # 인쇄를 실행할 프린터 선택

    if diseases == 'cold':
        #file_name = "C:/Users/anjae/Desktop/영상인식중/cold.pdf"       
        print('감기에 대한 주의사항입니다')

        # 시리얼 통신
        arduino.write('1'.encode('utf-8'))         # 약 조제를 위해 아두이노 통신 1
        
        
    elif diseases == 'headache':
        #file_name = "C:/Users/anjae/Desktop/영상인식중/Headache.pdf"
        print('두통에 대한 주의사항입니다')

        # 시리얼 통신
        arduino.write('2'.encode('utf-8'))         # 약 조제를 위해 아두이노 통신 2

    call([acrobat, "/T", file_name, printer])      # 약을 조제하는 동안 인쇄 진행
    

def do_ocr(image):
    """
    이미지(처방전)가 들어오면 처방전으로부터 글씨를 ocr진행후, 지정되있는 데이터 저장
    """
    test = pp.image_to_string(image, lang='eng')  # ocr진행

    data = name_re.findall(test)
    data = [ i[3:] for i in data]

    return data



if __name__ == '__main__':
    url = 'http://192.168.43.204:8080/video' # IP camera와 ip를 통한 통신 연결 주소 지정
    cap = cv2.VideoCapture(url)              # 카메라와 연결 통신

    frame_l = []
    name_re = re.compile(r' = \w+')          # 처방전으로 부터 추출할 데이터 형식 지정

    while(True):
        ret, frame = cap.read()
        frame_l.append(frame)
        
        cv2.imshow('frame', cv2.resize(frame, (1400, 840)))  # 이미지 확인

        s = cv2.waitKey(1)       # s키를 ocr실행 키로 지정
        
        if s == ord("s"):
            
            print("OCR NOW")
            data = do_ocr(frame_l[-1])      # ocr을 통해 데이터 추출
            print("OCR DONE")

            
            if len(data) < 4:      # 만약 데이터가 추출이 실패할 경우 재시도
                continue

            name = data[0]         # 이름을 ID로 사용하여 db에 저장
            df = pd.read_csv('Data/Personal Health Information.csv')


            if not (name in df.Name.values): # db에 저장된 이름이 없다면 == 첫 고객이면
                new_client = pd.Series({'Name': name, 'Sex': data[1], 'Age': data[2],  # 고객 정보 추가
                                     'Disease': data[3], 'Visit':1})
                df = df.append(new_client, ignore_index=True)   
                
            else:  # 기존 고객일 경우
                conditional_index = df[df.Name == name].index
                df.loc[conditional_index, ['Visit']] += 1       # 방문 횟수와 병 추

            df.to_csv('Data/Personal Health Information.csv', index=False)   # db 업그레이

            # caution for medicine printing
            medicine_caution(data[3])

            
           
    cv2.destroyAllWindows()
