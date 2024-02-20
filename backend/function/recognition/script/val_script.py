from ultralytics import YOLO
import sys
source_model_path = sys.argv[1]

yaml_path = sys.argv[2]    


if __name__ == "__main__":
    model = YOLO(source_model_path)
    result = model.val()
