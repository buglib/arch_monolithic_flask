# -*- coding: utf-8 -*-

import six
from jsonschema import RefResolver
# TODO: datetime support

class RefNode(object):

    def __init__(self, data, ref):
        self.ref = ref
        self._data = data

    def __getitem__(self, key):
        return self._data.__getitem__(key)

    def __setitem__(self, key, value):
        return self._data.__setitem__(key, value)

    def __getattr__(self, key):
        return self._data.__getattribute__(key)

    def __iter__(self):
        return self._data.__iter__()

    def __repr__(self):
        return repr({'$ref': self.ref})

    def __eq__(self, other):
        if isinstance(other, RefNode):
            return self._data == other._data and self.ref == other.ref
        elif six.PY2:
            return object.__eq__(other)
        elif six.PY3:
            return object.__eq__(self, other)
        else:
            return False

    def __deepcopy__(self, memo):
        return RefNode(copy.deepcopy(self._data), self.ref)

    def copy(self):
        return RefNode(self._data, self.ref)

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###

base_path = '/v1'

definitions = {'definitions': {'advertisementsModel': {'type': 'array', 'items': {'type': 'object', 'properties': {'id': {'type': 'integer'}, 'image': {'type': 'string', 'description': '广告轮播图中某书本的图片URL', 'example': '/static/carousel/fenix2.png'}, 'productId': {'type': 'integer'}}}}, 'productModel': {'type': 'object', 'properties': {'id': {'type': 'integer', 'description': '书本编号'}, 'title': {'type': 'string', 'description': '书名'}, 'price': {'type': 'number', 'description': '书本价格'}, 'rate': {'type': 'number', 'description': '优惠折扣'}, 'description': {'type': 'string', 'description': '书本描述'}, 'cover': {'type': 'string', 'description': '书本封面页图片链接'}, 'detail': {'type': 'string', 'description': '书本详情图片链接'}, 'specifications': {'type': 'array', 'items': {'type': 'object', 'properties': {'id': {'type': 'integer', 'description': '书本规格属性编号'}, 'item': {'type': 'string', 'description': '书本规格属性名称'}, 'value': {'type': 'string', 'description': '书本规格属性值'}}}}}}, 'tokenModel': {'type': 'object', 'example': {'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJpY3lmZW5peCIsInNjb3BlIjpbIkFMTCJdLCJleHAiOjE1ODQyNTA3MDQsImF1dGhvcml0aWVzIjpbIlJPTEVfVVNFUiIsIlJPTEVfQURNSU4iXSwianRpIjoiMTNmNGNlMWQtNmY2OC00NzQxLWI5YzYtMzkyNzU1OGQ5NzRlIiwiY2xpZW50X2lkIjoiYm9va3N0b3JlX2Zyb250ZW5kIiwidXNlcm5hbWUiOiJpY3lmZW5peCJ9.82awQU4IcLVXr7w6pxcUCWrcEHKq-LRT7ggPT_ZPhE0', 'token_type': 'bearer', 'refresh_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJpY3lmZW5peCIsInNjb3BlIjpbIkFMTCJdLCJhdGkiOiIxM2Y0Y2UxZC02ZjY4LTQ3NDEtYjljNi0zOTI3NTU4ZDk3NGUiLCJleHAiOjE1ODU1MzU5MDQsImF1dGhvcml0aWVzIjpbIlJPTEVfVVNFUiIsIlJPTEVfQURNSU4iXSwianRpIjoiY2IwN2ZjZjEtMjViZS00MDRjLTkwNzctY2U5ZTlhZjFjOWEwIiwiY2xpZW50X2lkIjoiYm9va3N0b3JlX2Zyb250ZW5kIiwidXNlcm5hbWUiOiJpY3lmZW5peCJ9.-gNKkhspN1XfVybmS3Rnz2AYFdteZN4kvdEmC4g-aYk', 'expires_in': 10799, 'scope': 'ALL', 'authorities': ['ROLE_USER', 'ROLE_ADMIN'], 'username': 'icyfenix', 'jti': '13f4ce1d-6f68-4741-b9c6-3927558d974e'}, 'properties': {'access_token': {'type': 'string', 'description': '访问令牌'}, 'token_type': {'type': 'string', 'description': '令牌类型'}, 'refresh_token': {'type': 'string', 'description': '刷新令牌'}, 'expires_in': {'type': 'integer', 'description': '令牌过期时间'}, 'scope': {'type': 'string', 'description': '许可时间'}, 'authorities': {'type': 'array', 'items': {'type': 'string', 'description': '授予的权限'}}, 'username': {'type': 'string', 'description': '申请认证者'}, 'jti': {'type': 'string', 'description': 'JWT标识符'}}}, 'stockpileModel': {'type': 'object', 'properties': {'id': {'type': 'integer', 'description': '库存编号'}, 'product_id': {'type': 'integer', 'description': '商品编号'}, 'amount': {'type': 'integer', 'description': '商品总数'}, 'frozen': {'type': 'integer', 'description': '商品不可售的数量'}}}}, 'parameters': {}}

validators = {
    ('products', 'POST'): {'json': {'$ref': '#/definitions/productModel'}},
    ('product', 'PUT'): {'json': {'$ref': '#/definitions/productModel'}},
    ('accounts', 'POST'): {'json': {'example': {'username': 'buglib', 'email': 'buglib@foxmail.com', 'password': '5hV62VD9mMbvRKthI563w8tTJs4VHFy', 'telephone': '12345665431'}, 'type': 'object', 'required': ['username', 'email', 'password', 'telephone'], 'properties': {'username': {'type': 'string'}, 'email': {'type': 'string'}, 'password': {'type': 'string'}, 'telephone': {'type': 'string'}}}},
    ('accounts', 'PUT'): {'json': {'type': 'object', 'required': ['id', 'username'], 'example': {'id': 1, 'username': 'icyfenix', 'name': '周志明', 'avatar': 'https://www.gravatar.com/avatar/1563e833e42fb64b41eed34c9b66d723?d=mp', 'telephone': '18888888888', 'email': 'icyfenix@gmail.com', 'location': '唐家湾港湾大道科技一路3号远光软件股份有限公司'}, 'properties': {'id': {'type': 'integer'}, 'username': {'type': 'string'}, 'email': {'type': 'string'}, 'password': {'type': 'string'}, 'telephone': {'type': 'string'}, 'avatar': {'type': 'string'}, 'name': {'type': 'string'}, 'location': {'type': 'string'}}}},
    ('oauth_token', 'GET'): {'args': {'required': ['grant_type', 'client_id', 'client_secret'], 'properties': {'username': {'type': 'string', 'required': False}, 'password': {'type': 'string', 'required': False}, 'refresh_token': {'type': 'string', 'required': False, 'description': '如果该字段为空，则用户名和密码不能同时为空'}, 'grant_type': {'type': 'string'}, 'client_id': {'type': 'string'}, 'client_secret': {'type': 'string'}}}},
    ('settlement', 'POST'): {'json': {'type': 'object', 'example': {'items': [{'amount': 1, 'id': 1}, {'amount': 1, 'id': 6}], 'purchase': {'name': '周志明', 'telephone': '18888888888', 'delivery': True, 'address': {'province': '广东省', 'city': '广州市', 'area': '海珠区'}, 'location': '广东省  广州市 海珠区 唐家湾港湾大道科技一路3号远光软件股份有限公司', 'pay': 'wechat', 'id': 1, 'username': 'icyfenix', 'avatar': 'https://www.gravatar.com/avatar/1563e833e42fb64b41eed34c9b66d723?d=mp', 'email': 'icyfenix@gmail.com'}}, 'properties': {'items': {'type': 'array', 'items': {'type': 'object', 'properties': {'id': {'type': 'integer', 'description': '商品编号'}, 'amount': {'type': 'integer', 'description': '商品库存数量'}}}}, 'purchase': {'type': 'object', 'properties': {'id': {'type': 'integer', 'description': '用户编号'}, 'name': {'type': 'string'}, 'username': {'type': 'string'}, 'telephone': {'type': 'string'}, 'email': {'type': 'string'}, 'avatar': {'type': 'string'}, 'location': {'type': 'string'}, 'address': {'type': 'object', 'properties': {'province': {'type': 'string'}, 'city': {'type': 'string'}, 'area': {'type': 'string'}}}, 'dilivery': {'type': 'boolean', 'description': '是否需要物流配送'}, 'pay': {'type': 'string', 'description': '支付方式'}}}}}},
}

filters = {
    ('index', 'GET'): {200: {'headers': {'Content-Type': {'type': 'string'}}, 'schema': {'type': 'file'}}, 404: {'headers': None, 'schema': None}},
    ('advertisements', 'GET'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/advertisementsModel'}}},
    ('products', 'GET'): {200: {'headers': None, 'schema': {'type': 'array', 'items': {'$ref': '#/definitions/productModel'}}}},
    ('products', 'POST'): {200: {'headers': None, 'schema': {'type': 'object', 'example': {'status': 'done', 'message': 'Succeed to add new product'}, 'properties': {'status': {'type': 'string'}, 'message': {'type': 'string'}}}}},
    ('product', 'GET'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/productModel'}}, 404: {'headers': None, 'schema': None}},
    ('product', 'PUT'): {200: {'headers': None, 'schema': {'type': 'object', 'example': {'status': 'done', 'message': 'Succeed to update product'}, 'properties': {'status': {'type': 'string'}, 'message': {'type': 'string'}}}}},
    ('product', 'DELETE'): {200: {'headers': None, 'schema': {'type': 'object', 'example': {'status': 'done', 'message': 'Succeed to remove product'}, 'properties': {'status': {'type': 'string'}, 'message': {'type': 'string'}}}}, 404: {'headers': None, 'schema': {'type': 'object', 'example': {'status': 'fail', 'message': 'Fail to remove product, because product not found'}, 'properties': {'status': {'type': 'string'}, 'message': {'type': 'string'}}}}},
    ('products_stockpile_product', 'GET'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/stockpileModel'}}, 404: {'headers': None, 'schema': {'type': 'object', 'example': {'status': 'fail', 'message': "fail to get stockpile for product '1', product '1' may be not found"}, 'properties': {'status': {'type': 'string'}, 'message': {'type': 'string'}}}}},
    ('products_stockpile_product', 'PATCH'): {200: {'headers': None, 'schema': {'example': {'status': 'done', 'message': "succeed to update stockpile for product '1'"}, 'properties': {'status': {'type': 'string'}, 'message': {'type': 'string'}}}}, 400: {'headers': None, 'schema': {'example': {'status': 'done', 'message': "fail to update stockpile for product '1', product '1' may be not found"}, 'properties': {'status': {'type': 'string'}, 'message': {'type': 'string'}}}}},
    ('accounts', 'POST'): {200: {'headers': None, 'schema': {'type': 'object', 'example': {'code': 0, 'message': '操作已成功'}, 'properties': {'code': {'type': 'integer'}, 'message': {'type': 'string'}}}}, 400: {'headers': None, 'schema': {'type': 'object', 'example': {'code': 0, 'message': '操作失败，用户已存在'}, 'properties': {'code': {'type': 'integer'}, 'message': {'type': 'string'}}}}},
    ('accounts', 'PUT'): {200: {'headers': None, 'schema': {'type': 'object', 'example': {'status': 'done', 'message': "Succeed to update user 'Messi'"}, 'properties': {'status': {'type': 'string'}, 'message': {'type': 'string'}}}}},
    ('accounts_username', 'GET'): {200: {'headers': None, 'schema': {'example': {'id': 1, 'username': 'icyfenix', 'name': '周志明', 'avatar': '', 'telephone': '18888888888', 'email': 'icyfenix@gmail.com', 'location': '唐家湾港湾大道科技一路3号远光软件股份有限公司'}, 'properties': {'id': {'type': 'integer'}, 'username': {'type': 'string'}, 'name': {'type': 'string'}, 'avatar': {'type': 'string'}, 'telephone': {'type': 'string'}, 'email': {'type': 'string'}, 'location': {'type': 'string'}}}}, 404: {'headers': None, 'schema': {'example': {'code': -1, 'message': '按用户名查找用户失败，即用户不存在'}, 'type': 'object', 'properties': {'code': {'type': 'integer'}, 'message': {'type': 'string'}}}}},
    ('oauth_token', 'GET'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/tokenModel'}}, 400: {'headers': None, 'schema': {'type': 'object', 'properties': {'error': {'type': 'string', 'description': '错误信息', 'example': ['invalid_request', 'invalid_client', 'invalid_grant']}}}}},
    ('settlement', 'POST'): {200: {'headers': None, 'schema': {'example': {'id': 2, 'createTime': '2023-01-01T09:25:30.843+0000', 'payId': 'c862e362-98bb-4ef6-b49c-d3ce896db4fa', 'totalPrice': 220, 'expires': 120000, 'paymentLink': '/pay/modify/c862e362-98bb-4ef6-b49c-d3ce896db4fa?state=PAYED&accountId=1', 'payState': 'WAITING'}, 'type': 'object', 'properties': {'id': {'type': 'integer', 'description': '订单编号'}, 'createTime': {'type': 'string', 'format': 'date-time'}, 'payId': {'type': 'integer', 'description': '支付流水号'}, 'totalPrice': {'type': 'number'}, 'expires': {'type': 'integer'}, 'paymentLink': {'type': 'string'}, 'payState': {'type': 'string'}}}}, 400: {'headers': None, 'schema': {'type': 'object', 'example': {'code': 1, 'message': '商品库存不足'}, 'properties': {'code': {'type': 'integer'}, 'message': {'type': 'string'}}}}},
}

scopes = {
}

resolver = RefResolver.from_schema(definitions)

class Security(object):

    def __init__(self):
        super(Security, self).__init__()
        self._loader = lambda: []

    @property
    def scopes(self):
        return self._loader()

    def scopes_loader(self, func):
        self._loader = func
        return func

security = Security()


def merge_default(schema, value, get_first=True, resolver=None):
    # TODO: more types support
    type_defaults = {
        'integer': 9573,
        'string': 'something',
        'object': {},
        'array': [],
        'boolean': False
    }

    results = normalize(schema, value, type_defaults, resolver=resolver)
    if get_first:
        return results[0]
    return results


def normalize(schema, data, required_defaults=None, resolver=None):
    if required_defaults is None:
        required_defaults = {}
    errors = []

    class DataWrapper(object):

        def __init__(self, data):
            super(DataWrapper, self).__init__()
            self.data = data

        def get(self, key, default=None):
            if isinstance(self.data, dict):
                return self.data.get(key, default)
            return getattr(self.data, key, default)

        def has(self, key):
            if isinstance(self.data, dict):
                return key in self.data
            return hasattr(self.data, key)

        def keys(self):
            if isinstance(self.data, dict):
                return list(self.data.keys())
            return list(getattr(self.data, '__dict__', {}).keys())

        def get_check(self, key, default=None):
            if isinstance(self.data, dict):
                value = self.data.get(key, default)
                has_key = key in self.data
            else:
                try:
                    value = getattr(self.data, key)
                except AttributeError:
                    value = default
                    has_key = False
                else:
                    has_key = True
            return value, has_key

    def _merge_dict(src, dst):
        for k, v in six.iteritems(dst):
            if isinstance(src, dict):
                if isinstance(v, dict):
                    r = _merge_dict(src.get(k, {}), v)
                    src[k] = r
                else:
                    src[k] = v
            else:
                src = {k: v}
        return src

    def _normalize_dict(schema, data):
        result = {}
        if not isinstance(data, DataWrapper):
            data = DataWrapper(data)

        for _schema in schema.get('allOf', []):
            rs_component = _normalize(_schema, data)
            _merge_dict(result, rs_component)

        for key, _schema in six.iteritems(schema.get('properties', {})):
            # set default
            type_ = _schema.get('type', 'object')

            # get value
            value, has_key = data.get_check(key)
            if has_key or '$ref' in _schema:
                result[key] = _normalize(_schema, value)
            elif 'default' in _schema:
                result[key] = _schema['default']
            elif key in schema.get('required', []):
                if type_ in required_defaults:
                    result[key] = required_defaults[type_]
                else:
                    errors.append(dict(name='property_missing',
                                       message='`%s` is required' % key))

        additional_properties_schema = schema.get('additionalProperties', False)
        if additional_properties_schema is not False:
            aproperties_set = set(data.keys()) - set(result.keys())
            for pro in aproperties_set:
                result[pro] = _normalize(additional_properties_schema, data.get(pro))

        return result

    def _normalize_list(schema, data):
        result = []
        if hasattr(data, '__iter__') and not isinstance(data, (dict, RefNode)):
            for item in data:
                result.append(_normalize(schema.get('items'), item))
        elif 'default' in schema:
            result = schema['default']
        return result

    def _normalize_default(schema, data):
        if data is None:
            return schema.get('default')
        else:
            return data

    def _normalize_ref(schema, data):
        if resolver == None:
            raise TypeError("resolver must be provided")
        ref = schema.get(u"$ref")
        scope, resolved = resolver.resolve(ref)
        if resolved.get('nullable', False) and not data:
            return {}
        return _normalize(resolved, data)

    def _normalize(schema, data):
        if schema is True or schema == {}:
            return data
        if not schema:
            return None
        funcs = {
            'object': _normalize_dict,
            'array': _normalize_list,
            'default': _normalize_default,
            'ref': _normalize_ref
        }
        type_ = schema.get('type', 'object')
        if type_ not in funcs:
            type_ = 'default'
        if schema.get(u'$ref', None):
            type_ = 'ref'

        return funcs[type_](schema, data)

    return _normalize(schema, data), errors
