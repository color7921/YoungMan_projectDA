from flask import Flask, jsonify, request
from PIL import Image
import easyocr
import re
import io


app = Flask(__name__)

def extract_text_from_image(image_path, languages=['en', 'ko']):
    global text_lists, update_text, json_text
    
    # OCR 리더 초기화
    reader = easyocr.Reader(languages)

    blocked_characters = 'O<>/|]\[-_+=`!@~#$%^&*)(,.:?;'
    # 이미지 파일에서 텍스트 추출
    # 황금비율  width_ths = 15, ycenter_ths = 0.5
    result = reader.readtext(image_path, width_ths=15, ycenter_ths=0.5, blocklist=blocked_characters)

    flag = False
    text_lists = []
    update_text = []
    json_text = []

    for (bbox, text, prob) in result:
        if flag and ("판매소계" in text or "판매" in text or "판매량" in text):
            break
        if flag:
            text_lists.append(text)
        if "금액" in text:
            flag = True

    dt = {}
    for i in range(0, len(text_lists)):
        if i % 2 == 1:
            result_text = text_lists[i].split()
            result_text = [int(item) for item in result_text if item]
            update_text.append(result_text)
            dt['unitPrice'] = result_text[0]
            dt['quantity'] = result_text[1]
            if len(result_text) == 3:
                dt['price'] = result_text[2]
            json_text.append(dt)
            dt = {}
        else:
            update_text.append(text_lists[i])
            dt['item'] = text_lists[i]

    return json_text


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
    extracted_data = extract_text_from_image(image)
    
    date = find_by_date(image) 
    # "date_part"를 각 항목에 추가
    for entry in extracted_data:
        entry["tradeDate"] = date
    # image_path.save(os.path.join('/', "test1.jpg"))
    return jsonify(extracted_data)

if __name__ == "__main__":
    app.run(host="10.125.121.211", port=5000, debug=True)
