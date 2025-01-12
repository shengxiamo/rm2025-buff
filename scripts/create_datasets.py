import json
import os
import cv2
from sympy.codegen.ast import continue_

classify = {
    "RR": '0',
    "RW": '1',
    "BR": '2',
    "BW": '3'
}

# 读取json文件
with open('label.json', 'r') as f:
    data = json.load(f)


# 创建输出文件夹
os.makedirs('datasets/buff_data/images', exist_ok=True)
os.makedirs('datasets/buff_data/labels', exist_ok=True)

# 遍历json数据
for item in data:
    # 检查是否存在 'bbox' 键
    if 'bbox' not in item:
        print(f"警告: 图片 {item['image']} 缺少 'bbox' 键")
        continue  # 跳过没有 'bbox' 的条目

    # 获取图片文件名
    image_filename = item['image'].split('/')[-1]
    image_filename = '-'.join(image_filename.split('-')[1:])
    print(image_filename)

    image_path='origin_images/'+image_filename

    # 读取图片
    img = cv2.imread(os.path.join(image_path, image_filename))
    if img is not None:
        cv2.imwrite(os.path.join('new_buff_data/images', image_filename), img)
    else:
        print(f"错误: 无法读取图片 {image_filename}")
        continue

    # 创建txt文件路径
    txt_filename = image_filename.replace('.jpg', '.txt')
    txt_path = os.path.join('new_buff_data/labels', txt_filename)

    # 写入txt文件
    with open(txt_path, 'w') as txt_file:
        # 获取图片宽度和高度
        original_width = item['keypoints'][0]['original_width']
        original_height = item['keypoints'][0]['original_height']

        class_num = classify.get(item["bbox"][0]["rectanglelabels"][0], -1)  # 使用 .get() 防止 KeyError
        if class_num == -1:
            print(f"警告: 图片 {image_filename} 类别标签无效")
            continue  # 跳过无效类别的条目

        x = item["bbox"][0]["x"] / 100
        y = item["bbox"][0]["y"] / 100
        width = item["bbox"][0]["width"] / 100
        height = item["bbox"][0]["height"] / 100
        x_center = x + width / 2
        y_center = y + height / 2

        # 获取关键点的归一化坐标
        kpt_num = 0
        for keypoint in item["keypoints"][0]:
            kpt_num += 1
        if kpt_num != 5:
            print(f"警告: 图片 {image_filename} 不足5个关键点")
            continue # 跳过没有5个关键点的条目

        x1 = item["keypoints"][0]["x"] / 100
        y1 = item["keypoints"][0]["y"] / 100
        x2 = item["keypoints"][1]["x"] / 100
        y2 = item["keypoints"][1]["y"] / 100
        x3 = item["keypoints"][2]["x"] / 100
        y3 = item["keypoints"][2]["y"] / 100
        x4 = item["keypoints"][3]["x"] / 100
        y4 = item["keypoints"][3]["y"] / 100
        x5 = item["keypoints"][4]["x"] / 100
        y5 = item["keypoints"][4]["y"] / 100

        # 写入数据到txt文件
        txt_file.write(f"{class_num} {x_center} {y_center} {width} {height} {x1} {y1} {x2} {y2} {x3} {y3} {x4} {y4} {x5} {y5}\n")
