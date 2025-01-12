# rm2025_buff
RoboMaster buff detect and predict
利用过往赛季的能量机关数据集，先预训练处模型，然后再对数据集重新标注，进行迁移学习，用于2025赛季的buff识别和预测。

## 模型预训练配置

### 1. 数据集

对于以往数据集上的预训练，使用西交利物浦GMaster战队开源数据集：[YOLO-of-RoboMaster-Keypoints-Detection-2023](https://github.com/zRzRzRzRzRzRzR/YOLO-of-RoboMaster-Keypoints-Detection-2023)

转化为 `yolov8 keypoint` 格式

```bash
python ./scripts/split_data.py --data ./datasets/buff_data --ratio 0.8 --output ./datasets/buff_format
```
datasets为yolo数据集存放路径，在配置文件中可以更改，具体位置自行搜索。buff_data为原始数据集，buff_format为转化后的数据集。

### 2. 训练

```bash
yolo pose train data=buff.yaml model=yolov8n-pose.pt epochs=200 batch=32 imgsz=640 iou=0.7 max_det=10 kobj=10 rect=True name=buff
```
## 2.制作新的数据集
### 1.数据标注
对于新的能量机关，没有开源数据集，只能手动标注。推荐使用label studio标注工具，，支持多人协作，与自定义标注格式。
经测试，可以使用之前的能量机关图片，只要忽略外面的发光轮廓，重新规定5个关键点标注即可。训练出来的模型可以识别新的能量机关。


### 2.数据集转化
标注完成后，导出minjson格式的标注文件,修改create_dataset.py中的json与原始图片路径，以及输出路径，运行create_dataset.py生成yolo格式的数据集。
再次运行以下命令，将数据集输入改为上一步的输出路径。
```bash
python ./scripts/split_data.py --data ./datasets/new_buff_data --ratio 0.8 --output ./datasets/new_buff_format
```

## 3.迁移学习
### 1.训练
修改buff.yaml中的数据集路径， 运行训练代码，将模型改为之前训练好的模型。
```bash
yolo pose train data=buff.yaml model=/runs/buff/weights/best.pt epochs=200 batch=32 imgsz=640 iou=0.7 max_det=10 kobj=10 rect=True name=buff
```

## 模型验证
srcipts文件夹下的predict_yolo.py和predict_video_yolo.py可以用于模型验证，修改模型路径和图片/视频路径，运行即可。
## 模型导出
### 1. pt -> onnx

```bash
yolo export model=models/best.pt format=onnx dynamic=False half=True simplify=True opset=13
```

### 2. onnx -> ov

```bash
mo --input_model ./models/best.onnx --output_dir ./models
```

### 3. 模型量化

```bash
python ./scripts/ov_quantize.py
```
