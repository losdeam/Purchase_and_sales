from flask_restx import Namespace, Resource , fields   # RESTful API
from function.recognition import image_to_mongo,image_from_mongo,image_delete_mongo,tranform,img_clear


api = Namespace('recognition', description='识别接口')
label_model = api.model('labelmodel', {
    'label_name': fields.String(max_length=100, required=True, description='标签名称'),
})

@api.route('/add')
class add(Resource):
    @api.doc(description='显示数量过低的商品')
    @api.expect(label_model, validate=True)
    def post(self):
        """
        显示所有数量小于标准持有量的商品
        """
        name = api.payload['label_name']
        return image_to_mongo(name)

@api.route('/get')
class get(Resource):
    @api.doc(description='获取')
    def post(self):
        """
        获取数据
        """
        return image_from_mongo()
    
@api.route('/delete')
class delete(Resource):
    @api.doc(description='获取')
    @api.expect(label_model, validate=True)
    def post(self):
        """
        获取数据
        """
        name = api.payload['label_name']
        return image_delete_mongo(name)
    
@api.route('/trans')
class trans(Resource):
    @api.doc(description='')
    def post(self):
        """
        """
        return tranform()
    
@api.route('/clear')
class clear(Resource):
    @api.doc(description='')
    def post(self):
        """
        """
        return img_clear()