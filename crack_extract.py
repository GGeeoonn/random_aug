import os
import cv2
import numpy as np

# 이미지가 저장된 디렉토리 경로
src_dir = './test_results/resnet_101'
# 이미지를 저장할 디렉토리 경로
dest_dir = './creack_extract'
# 이미지 크기
img_size = (448, 448)
# 어둡다고 판단할 픽셀값의 임계값 (0-255)
threshold = 50

# 만약 저장할 디렉토리가 존재하지 않다면 디렉토리 생성
if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

# 소스 디렉토리의 모든 파일을 검사
for filename in os.listdir(src_dir):
    # 파일이 .jpg, .png 등의 이미지 파일인지 확인
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # 이미지 파일 경로
        image_path = os.path.join(src_dir, filename)
        # 이미지를 로드, 3채널 (RGB)로 로드
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        # 이미지의 크기를 변경
        resized_img = cv2.resize(img, img_size)
        # 투명도(alpha) 채널을 추가 (4채널로 변환)
        if len(resized_img.shape) < 3 or resized_img.shape[2] < 4:
            alpha_channel = np.ones(resized_img.shape[:2], dtype=resized_img.dtype) * 255
            resized_img = cv2.merge([resized_img, alpha_channel])
        # 투명도 채널에 대해, 각 픽셀의 값이 임계값 이상이면 0 (투명)으로 설정
        resized_img[(cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)) >= threshold, 3] = 0
        # 이미지의 색상을 반전
        inv_img = cv2.bitwise_not(resized_img)
        # 파일명에서 확장자를 제거하고 .png를 추가
        filename = os.path.splitext(filename)[0] + '.png'
        # 이미지를 목적지 디렉토리에 저장
        cv2.imwrite(os.path.join(dest_dir, filename), inv_img)