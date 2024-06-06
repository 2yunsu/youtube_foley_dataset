import cv2
import matplotlib.pyplot as plt
import math
import pdb

# 사용할 변수들 미리 정의
FONT = cv2.FONT_HERSHEY_DUPLEX
BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
RED = (0, 0, 255)
FILTER_RATIO = 0.85


def extract_first_frame(video_path):
    # 동영상 파일 열기
    cap = cv2.VideoCapture(video_path)
    
    # 동영상이 성공적으로 열렸는지 확인
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    # 첫 번째 프레임 읽기
    ret, frame = cap.read()
    
    # 프레임이 성공적으로 읽혔는지 확인
    if ret:
        # 이미지를 파일로 저장
        # cv2.imwrite(output_image_path, frame)
        return frame
        print(f"First frame saved as {output_image_path}")
    else:
        print("Error: Could not read frame.")
    
    # 동영상 캡처 객체 해제
    cap.release()

# 경계선을 가져오는 함수
def get_contours(img, min_area, is_simple=False):
    # 근사화 방식 Simple : 경계선의 꼭짓점 좌표만 반환
    if is_simple:
        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 근사화 방식 None : 모든 경계선을 반환
    else:
        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    result = []

    # 경계선 개수만큼 반복
    for cnt in contours:
        # 경계선의 너비가 최소 영역 이상일 때만 result 배열에 추가
        if cv2.contourArea(cnt) > min_area:
            result.append(cnt)

    return result

# 꼭짓점을 그리는 함수
def draw_points(img, cnt, epsilon, color):
    cnt_length = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon * cnt_length, True)

    for point in approx:
        cv2.circle(img, (point[0][0], point[0][1]), 3, color, -1)

video_path = './videos/Recreating_Vintage_Cartoon_Sounds_(HARD).mp4'
img = extract_first_frame(video_path)

"""
def crop_top_right_rectangle(image):
    # 이미지를 회색조로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 에지 감지
    edges = cv2.Canny(gray, 50, 150)
    cv2.imshow('Cropped Image', edges)
    
    # 컨투어 찾기
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 가장 오른쪽 상단에 위치한 사각형 찾기
    max_area = 0
    top_right_rect = None
    
    for contour in contours:
        # 컨투어를 근사화하여 사각형 찾기
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        if len(approx) == 4:  # 사각형일 때
            x, y, w, h = cv2.boundingRect(approx)
            area = w * h
            # 오른쪽 상단에 위치한 사각형을 선택
            if area > max_area and x + w // 2 > image.shape[1] // 2 and y + h // 2 < image.shape[0] // 2:
                max_area = area
                top_right_rect = (x, y, w, h)
    
    if top_right_rect is not None:
        x, y, w, h = top_right_rect
        cropped_image = image[y:y+h, x:x+w]
        return cropped_image
    else:
        print("Error: No rectangle found in the top right corner.")
        return None

if img is not None:
    # 오른쪽 상단에 있는 사각형을 자동으로 크롭
    cropped_image = crop_top_right_rectangle(img)
    
    if cropped_image is not None:
        # 크롭된 이미지 표시
        cv2.imshow('Cropped Image', cropped_image)
        cv2.waitKey(0)  # 키 입력을 기다립니다
        cv2.destroyAllWindows()

"""

# 이미지 불러와서 필터링
filter_img = cv2.inRange(img, (0, 0, 0), (255, 150, 255))

# 경계선 가져오기
contours_simple = get_contours(filter_img, 50, True)
contours_none = get_contours(filter_img, 50, False)

# 텍스트 출력하고 경계선 그리기(simple)
simple_text = "contours count : " + str(len(contours_simple))
simple_img = cv2.putText(img.copy(), simple_text, (0, 25), FONT, 1, RED)
for cnt in contours_simple:
    cv2.drawContours(simple_img, cnt, -1, BLUE, 5)
    draw_points(simple_img, cnt, 0.1, GREEN)

# 텍스트 출력하고 경계선 그리기(none)
none_text = "contours count : " + str(len(contours_none))
none_img = cv2.putText(img.copy(), none_text, (0, 25), FONT, 1, RED)
for cnt in contours_none:
    cv2.drawContours(none_img, cnt, -1, BLUE, 5)
    draw_points(none_img, cnt, 0.1, GREEN)


# 이미지 화면에 출력
cv2.imshow("origin image", img)
cv2.imshow("filter image", filter_img)
cv2.imshow("simple image", simple_img)
cv2.imshow("none image", none_img)
cv2.waitKey(0)