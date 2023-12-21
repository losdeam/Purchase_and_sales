from ultralytics import YOLO
import sys
sys.path.append('.')
from instance.yolo_config import path_config,train_config
source_model_path = path_config['source_model_path']
yaml_path = path_config['yaml_path']

def train_new_label():
    model = YOLO(source_model_path)
    # 使用“coco128.yaml”数据集训练模型3个周期
    results = model.train(data=yaml_path,imgsz = train_config['imgsz']  ,\
                        epochs=train_config['epochs'],\
                        amp = False,\
                        augment	= train_config['augment'],\
                        mosaic= train_config['mosaic'],\
                        mixup= train_config['mixup'],\
                        degrees =train_config['degrees'],\
                        translate  =train_config['translate'],\
                        scale= train_config['scale'] ,\
                        
                        flipud=train_config['flipud'],\
                        fliplr=train_config['fliplr'])

    # 评估模型在验证集上的性能
    results = model.val()

    # 使用模型对图片进行目标检测
    # results = model('data/images/fall_0.jpg')


if __name__ == "__main__":
    print("训练开始")
    train_new_label()
    print("训练结束")