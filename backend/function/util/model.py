import datetime
image_model = {
    "image" : bytes,
    "label_txt" : bytes,
    "label" : str,
}

goods_model = {
    "id" : int,
    "name" : str,
    "num" : int,
    "sort" : str ,
    "price_buying" : float,
    "price_retail" : float,
    "baseline" : int,
}

user_model = {
    "id" : int,
    "name" : str,
    "password" : bytes,
    "rank" : int,
    "power" : int,
    "path_config" : dict,
    "data_config" : dict,
    "train_config" : dict,
}


Sales_records_model= {
    "id" : int,
    "time_stamp" : str,
    "records_data" : dict,
}