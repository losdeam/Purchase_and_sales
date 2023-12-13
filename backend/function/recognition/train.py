from ultralytics import YOLO
from setting import setting
from  multiprocessing import freeze_support

# 加载预训练的YOLOv8n模型


# 将模型导出为ONNX格式
# success = model.export(format='onnx')
if __name__ == '__main__':
    freeze_support()
    model = YOLO(setting['model_path'])
    # 使用“coco128.yaml”数据集训练模型3个周期
    results = model.train(data='./data/goods.yaml', epochs=3,amp = False)

    # 评估模型在验证集上的性能
    results = model.val()

    # 使用模型对图片进行目标检测
    # results = model('data/images/fall_0.jpg')