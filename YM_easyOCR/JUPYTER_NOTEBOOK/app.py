from flask import Flask, jsonify, request
from PIL import Image
import easyocr
import re
import io
import torch

app = Flask(__name__)


def extract_text_from_image(image_path, languages=['en', 'ko']):
    global update_text, json_text
    update_text = []
    json_text = []

    blocked_characters = 'COUBJuIi<{}>|]\-:[_+=`!@~#$%^&*)(?;\"\''

    try:
        # 황금비율  width_ths = 15, ycenter_ths = 0.5
        text_lists = []
        # OCR 리더 초기화
        reader = easyocr.Reader(languages)
        # 이미지 파일에서 텍스트 추출
        result = reader.readtext(image_path, width_ths=15, ycenter_ths=0.5, blocklist=blocked_characters)

        for detection in result:
            print(detection[1])
        flag = False
        text_lists = []
        

        list = []

        for (bbox, text, prob) in result:
            if flag and ("판매소계" in text or "판매" in text or "판매량" in text or "만" in text or "판" in text or "민" in text or "소계" in text):
                break
            if flag:
                text_lists.append(text)
            if "금액" in text or "수량" in text or "단가" in text:
                flag = True
                

        # 텍스트를 추출할 때,  width_ths = 15, ycenter_ths = 0.5 의 비율로 박스를 조정하면 [품명, 단가 수량 금액] 별로 나온다.
        # 품명은 문제 없지만, 단가 수량 금액을 따로 딕셔너리로 바꾸려면 공백을 기준으로 split을 해야함.
        # 그래서 다음 코드는 짝수번째에 해당하는 배열은 그대로 두고 홀수번째에 해당하는 배열을 조정하는 것이다.
                
        dt = {}
        flag2 = False
    
        if("," in text_lists[0] or "." in text_lists[0]) :
            flag2 = True

        for i in range(0, len(text_lists)):
            if(flag2) :

                result_text = text_lists[i].split()
                if(len(result_text) == 4) :

                    dt['item'] = result_text[0]
                    dt['unitPrice'] = result_text[1].replace("I", "1")
                    dt['quantity'] = result_text[2]
                    dt['price'] = result_text[3] 
                    json_text.append(dt)
                    dt = {}
                    
                else :

                    k = 0
                    n = 0
                    q = 0
                    for (j,c) in enumerate(text_lists[i]) :
                        if(c == " " and text_lists[i][j+1] == " ") :
                            
                            dt['item'] = text_lists[i][0:j]
                            k = j
                            break
                    text2 = text_lists[i][k+1:].strip()
                    for (m,c) in enumerate(text2) :
                        if(c == " ") :
                            dt['unitPrice'] = text2[0:m]
                            n = m
                            break
                    text3 = text2[n+1:].strip()
                    for (z,c) in enumerate(text3) :
                        if(c == " ") :
                            dt["quantity"] = text3[0:z]
                            q = z
                            break
                            
                    text4 = text3[q+1:].strip()
                    for (y,c) in enumerate(text4) :
                        if(c == " ") :
                            text4 = text4[0:y] + "." + text4[y+1:]

                    dt["price"] = text4
                    
                    json_text.append(dt)
                    dt={}
            else:
                if i % 2 == 1:
                    result_text = text_lists[i].split()

                    result_text = [item for item in result_text if item]
                    update_text.append(result_text)
                    dt['unitPrice'] = result_text[0]
                    dt['quantity'] = result_text[1]
                    if len(result_text) == 3 :
                        dt['price'] = result_text[2]
                    json_text.append(dt)

                    dt = {}
                else:
                    update_text.append(text_lists[i])
                    dt['item'] = text_lists[i] 
    except:
        text_lists = []
        json_text = []
        reader = easyocr.Reader(['en', 'ko'])
        # result = reader.readtext(image_path, width_ths = 15, ycenter_ths = 0.5, blocklist=blocked_characters)
        result = reader.readtext('/Users/402-07/YoungMan_projectDE/receipt_list/h12.jpg')

        flag = False
        list = []
    
        # 추출된 텍스트 출력
        for detection in result:
            print(detection[1])
    
        for (bbox, text, prob) in result:
                list.append(text)
        
        for text in list:
            if flag and ("국민은행" in text or "판매소계" in text or "판매" in text or "판매량" in text or "만" in text or "판" in text or "민" in text or "소계" in text):
                break
            if flag:
                text_lists.append(text)
            if "AMOUNT" in text or "금액" in text or "수량" in text or "단가" in text:
                flag = True
            
        # 텍스트를 추출할 때,  width_ths = 15, ycenter_ths = 0.5 의 비율로 박스를 조정하면 [품명, 단가 수량 금액] 별로 나온다.
        # 품명은 문제 없지만, 단가 수량 금액을 따로 딕셔너리로 바꾸려면 공백을 기준으로 split을 해야함.
        # 그래서 다음 코드는 짝수번째에 해당하는 배열은 그대로 두고 홀수번째에 해당하는 배열을 조정하는 것이다.
        dt = {}
    
        dt['item'] = text_lists[0]
        dt['quantity'] = text_lists[1].replace("I", "1")
        dt['unitPrice'] = text_lists[2].replace("-", "000")
        dt['price'] = text_lists[3].replace("I", "1").replace("C", "4") + "000"
        json_text.append(dt)
        dt = {}
    return json_text

    # for i in range(0, len(text_lists)):
    #     if i % 2 == 1:
    #         result_text = text_lists[i].split()
    #         result_text = [int(item) for item in result_text if item]
    #         update_text.append(result_text)
    #         dt['unitPrice'] = result_text[0]
    #         dt['quantity'] = result_text[1]
    #         if len(result_text) == 3:
    #             dt['price'] = result_text[2]
    #         json_text.append(dt)
    #         dt = {}
    #     else:
    #         update_text.append(text_lists[i])
    #         dt['item'] = text_lists[i]

def find_by_date(image_path, languages=['en', 'ko']):
    global text_list

    # OCR 리더 초기화
    reader = easyocr.Reader(languages)

    blocked_characters = ';이터,'
    
    # 이미지 파일에서 텍스트 추출
    result = reader.readtext(image_path, width_ths = 0.5, ycenter_ths = 0.5, blocklist=blocked_characters)

    text_list = []
    # 추출된 텍스트 확인 
    # for detection in result:
    #     print(detection[1])

    for (bbox, text, prob) in result:
        text_list.append(text)

    # 정규식 패턴
    pattern = r'(\d{4}-\d{2}-\d{2})'

    tradeDate = ""
    for text in text_list:
        match = re.search(pattern, text)


        if match:
            cv = match.group(1) # 날짜 부분
            tradeDate = cv + "T00:00:00"
          
            break
    return tradeDate

# 사용 가능 01, 02, 04, 07, 11(시간이 아쉬움), 15(시간 아쉬움), 17(시간 아쉬움)


# Route definition
@app.route("/", methods=["POST"])
def process_image():
    # 이미지 파일 경로 설정
    image_path = request.files['image']
    image_bytes = io.BytesIO(image_path.stream.read())
    # image_path = '/Users/402-07/YoungMan_projectDE/receipt_list/03.jpg'  # 본인이 사용하는 이미지 파일로 경로를 변경하세요.
    
    image = Image.open(image_bytes)
    # extract_text_from_image의 결과를 가져오기
    print("시작")
    extracted_data = extract_text_from_image(image)
    print("끝")

    date = find_by_date(image) 
    # "date_part"를 각 항목에 추가
    for entry in extracted_data:
        entry["tradeDate"] = date
    # image_path.save(os.path.join('/', "test1.jpg"))
    print(extracted_data)
    return jsonify(extracted_data)


if __name__ == "__main__":
    app.run(host="10.125.121.211", port=5000, debug=True)
