from ultralytics import YOLO,settings
import sys
import json 


# Update multiple settings
settings.update({'datasets_dir': 'function/recognition/data'})
settings.update({'runs_dir': 'function/recognition/runs'})
# print(settings['runs_dir'])
# Reset settings to default values
# settings.reset()


source_model_path = sys.argv[1]
# print('source_model_path',source_model_path)
origin_model_path = sys.argv[2]
# print('origin_model_path',origin_model_path)
yaml_path = sys.argv[3]    
# print('yaml_path',yaml_path)
args_json = sys.argv[4]  
# print('args',args_json,type(args_json))
args = json.loads(args_json)
def train_new_label():
    try :
        model = YOLO(source_model_path)
    except:
        model = YOLO(origin_model_path)
    # 使用“coco128.yaml”数据集训练模型3个周期
    results = model.train(data=yaml_path,**args )



    # 使用模型对图片进行目标检测
    # results = model('data/images/fall_0.jpg')


if __name__ == "__main__":
    print("训练开始")
    train_new_label()
    print("训练结束")