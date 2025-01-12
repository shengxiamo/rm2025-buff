import cv2
import os

# 获取图片和标签文件夹的路径
image_folder = "new_buff_data/images/"
label_folder = "new_buff_data/labels/"

# 获取所有图片文件
image_files = sorted(os.listdir(image_folder))  # 排序以确保按顺序读取
image_index = 0  # 当前图片的索引


def show_image(image_index):
    # 获取当前图片文件和标签文件
    image_file = image_files[image_index]
    label_file = image_file.replace('.jpg', '.txt')  # 假设图片是.jpg后缀，标签是.txt后缀

    # 读取图片
    img = cv2.imread(os.path.join(image_folder, image_file))

    # 读取标签文件内容
    with open(os.path.join(label_folder, label_file), "r") as file:
        text = file.read().strip()

    # 将内容分割并转换为浮点数
    label = text.split(" ")

    # 获取图片宽度和高度
    width = img.shape[1]
    height = img.shape[0]

    # 提取边界框信息
    xywh = list(map(float, label[1:5]))  # 转换为浮点数并存储为列表
    x_center, y_center, box_width, box_height = xywh  # 解包坐标信息

    # 提取关键点坐标 (x1, y1, x2, y2, ...)
    kpts = list(map(float, label[5:]))
    kpts = [(int(kpts[i] * width), int(kpts[i + 1] * height)) for i in range(0, len(kpts), 2)]  # 转换为像素点坐标

    # 转换边界框为矩形的左上角和右下角
    x1 = int((x_center - box_width / 2) * width)
    y1 = int((y_center - box_height / 2) * height)
    x2 = int((x_center + box_width / 2) * width)
    y2 = int((y_center + box_height / 2) * height)

    # 在图片上绘制矩形
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # 在图片上绘制关键点
    i = 1
    for kpt in kpts:
        cv2.circle(img, kpt, 3, (0, 0, 255), -1)  # 红色点
        cv2.putText(img, str(i), kpt, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 1)  # 文字
        i += 1

    # 显示结果
    cv2.imshow("img", img)


# 显示当前图片
show_image(image_index)

while True:
    key = cv2.waitKey(0) & 0xFF  # 等待按键输入

    if key == ord('e'):  # 按下'e'键显示下一张图片
        image_index = (image_index + 1) % len(image_files)
        show_image(image_index)

    elif key == ord('q'):  # 按下'q'键显示上一张图片
        image_index = (image_index - 1) % len(image_files)
        show_image(image_index)

    elif key == ord('x'):  # 按下'x'键退出
        break

cv2.destroyAllWindows()
