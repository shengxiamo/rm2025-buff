import cv2
from ultralytics import YOLO
import os

# 模型路径和视频路径
model_path = "D:\\PycharmProjects\\rm_buff\\runs\pose\\buff\weights\\best.pt"
video_path = "D:/PycharmProjects/rm_buff/input/vedio.mp4"

# 检查视频文件是否存在
if not os.path.exists(video_path):
    raise FileNotFoundError(f"视频文件不存在: {video_path}")

# 加载模型
model = YOLO(model_path)

# 打开视频
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    raise Exception("无法打开视频")

# 逐帧处理视频
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:  # 视频结束时退出
        print("视频读取完毕")
        break

    # 调整帧大小
    frame_resized = cv2.resize(frame, (640, 480))

    # 模型推理
    results = model(frame_resized)

    # 获取推理结果并绘制
    annotated_frame = results[0].plot()

    # 打印推理速度信息
    print("推理速度:", results[0].speed)

    # 定义字体和字体大小
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 0.6
    font_thickness = 1

    # 循环遍历速度字典并在图像上标注文本
    for i, (key, value) in enumerate(results[0].speed.items()):
        text = f'{key}: {value:.2f} ms'
        y_position = 30 + i * 30  # 调整文本的垂直位置
        cv2.putText(annotated_frame, text, (10, y_position), font,
                    font_size, (0, 255, 0), font_thickness, cv2.LINE_AA)

    # 显示推理结果
    cv2.imshow("YOLOv8 推理", annotated_frame)

    # 按 'q' 键退出
    if cv2.waitKey(10) & 0xFF == ord('q'):
        print("用户终止视频播放")
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()
