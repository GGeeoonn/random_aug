from PIL import Image
import random
import os

def synthesize_image(background_path, object_path, output_folder, num_outputs):
    # 먼저 배경 이미지와 객체 이미지를 엽니다.
    background = Image.open(background_path)
    obj = Image.open(object_path)

    # 합성할 이미지 수만큼 반복합니다.
    for i in range(num_outputs):
        # 이미지의 사이즈를 무작위로 조절합니다. 여기서는 배경 이미지의 절반 크기까지 조절하도록 하였습니다.
        resize_factor = random.uniform(0.1, 0.5)
        new_size = (int(obj.size[0] * resize_factor), int(obj.size[1] * resize_factor))
        rescaled_obj = obj.resize(new_size)

        # 이미지의 방향을 무작위로 조절합니다. 여기서는 0도에서 360도 사이의 각도를 무작위로 선택하였습니다.
        rotate_angle = random.uniform(0, 360)
        rotated_obj = rescaled_obj.rotate(rotate_angle, expand=True)

        # 합성할 위치를 랜덤으로 선택합니다. 
        # 이 때, 객체가 배경 이미지 바깥으로 나가지 않도록 위치를 선택합니다.
        max_x = background.size[0] - rotated_obj.size[0]
        max_y = background.size[1] - rotated_obj.size[1]
        position = (random.randint(0, max_x), random.randint(0, max_y))

        # 배경 이미지를 복사한 후, 해당 위치에 객체 이미지를 붙여넣습니다.
        synth = background.copy()
        synth.paste(rotated_obj, position, rotated_obj)

        # 합성한 이미지를 저장합니다.
        synth.save(os.path.join(output_folder, f'synthesis_{i}.png'))

# 코드 실행
synthesize_image('background.jpg', './creack_extract/crack_test.png', './synthesis_result', 10)