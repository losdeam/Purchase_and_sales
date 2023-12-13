from ultralytics import settings

setting = {}
setting['datasets_dir'] = ''
setting['weights_dir'] = ''
setting['runs_dir'] = 'run'
settings.update(setting)
# print(settings)

setting['model_path'] = 'D:\\learn\\Flask\\Purchase_and_sales\\backend\\function\\recognition\\model\\best.pt'
# setting['model_path'] =  'D:\\learn\\Flask\\Purchase_and_sales\\backend\\function\\recognition\\model\\test_1.pt'
setting['source_path'] = 'D:\\learn\\Flask\\Purchase_and_sales\\backend\\function\\recognition\\data\\images\\fall_0.jpg'



setting['source_path'] = []
for i in range(2,10):
    setting['source_path'].append(f'D:\\learn\\Flask\\Purchase_and_sales\\backend\\function\\recognition\\data\\images\\fall_{i}.jpg')
# setting['source_path'] = '0'
# data/images/fall_0.jpg