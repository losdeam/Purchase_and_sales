from ultralytics import YOLO
import sys
sys.path.append('.')
from instance.yolo_config import path_config,train_config
source_model_path = path_config['source_model_path']
origin_model_path = path_config['origin_model_path']
yaml_path = path_config['yaml_path']

def train_new_label():
    try :
        model = YOLO(source_model_path)
    except:
        model = YOLO(origin_model_path)
    args = train_config
    # 使用“coco128.yaml”数据集训练模型3个周期
    results = model.train(data=yaml_path,**args )



    # 使用模型对图片进行目标检测
    # results = model('data/images/fall_0.jpg')


if __name__ == "__main__":
    print("训练开始")
    train_new_label()
    print("训练结束")