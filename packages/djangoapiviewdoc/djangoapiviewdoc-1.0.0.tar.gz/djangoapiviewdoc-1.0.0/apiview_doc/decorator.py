#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2021/12/14 13:31
    Desc  :
--------------------------------------
"""

from functools import wraps
from django_http_log.common.response import ParamsErrorResponse

from apiview_doc import settings


class ApiDocTags:
    def __init__(self):
        self.name = None
        self.description = None


class ApiDocParams(ApiDocTags):

    def __init__(self):
        super().__init__()
        self.type = None
        self.required = False
        self.example = None
        self.remark = None


params_list = list[ApiDocParams().__dict__]
tag_list = list[ApiDocTags().__dict__]
tag_dict = dict(ApiDocTags().__dict__)


class ApiDocBase:

    def __init__(self):
        # 标题
        # self.title = '接口文档'
        self.title = getattr(settings, 'APIVIEW_DOC_TITLE') if hasattr(settings, 'APIVIEW_DOC_TITLE') else '接口文档'
        # 版本号
        self.version = getattr(settings, 'APIVIEW_DOC_VERSION') if hasattr(settings, 'APIVIEW_DOC_VERSION') else '接口文档'
        # 标签
        # self.tags: tag_list = []
        # 接口
        # self.paths = {}
        # 数据
        self.data = {}
        # 状态码
        self.status_code = None

        self.class_list = []


global_api_doc = ApiDocBase().__dict__


class ApiDoc:

    def __init__(self):
        # 接口请求路径
        self.path = None
        # 接口tag
        self.tag: tag_dict = None
        # 接口请求参数
        self.params = []
        # 接口请求方法
        self.method = None
        # 接口描述
        self.summary = None

        # 类名
        self.class_name = None

    def ApiPath(self, value: str):
        """地址"""

        def decorator(f):
            self.get_class_name(f)

            self.path = value
            return f

        return decorator

    def ApiTag(self, value: str, desc: str = None):
        """地址"""

        def decorator(f):
            self.get_class_name(f)

            apiDocTags = ApiDocTags()
            apiDocTags.name = value
            apiDocTags.description = desc
            self.tag = apiDocTags.__dict__
            return f

        return decorator

    def ApiOperation(self, summary: str, path: str, method: str):
        """表示一个http请求的操作 """

        def decorator(f):
            self.get_class_name(f)

            self.method = method
            self.summary = summary
            self.path = path
            return f

        return decorator

    def get_class_name(self, f):
        qual_name = f.__qualname__
        if qual_name == '':
            raise ValueError(
                f"{f.__name__}不是类方法"
            )
        self.class_name = qual_name[:str(qual_name).find('.')]

        class_list = global_api_doc.get('class_list')
        if self.class_name not in class_list:
            class_list.append(self.class_name)

    def ApiParams(self, value: str, type: str, desc: str = None, require: bool = False, example: str = None,
                  remark: str = None):
        """表示一个请求参数"""

        def decorator(f):
            self.get_class_name(f)
            self.setParams(value = value, type = type, require = require,
                           desc = desc if desc else '',
                           example = example if example else '',
                           remark = remark if remark else '')
            return f

        return decorator

    def setParams(self, value: str, type: str, desc: str = '', require: bool = False, example: str = '',
                  remark: str = ''):
        """设置参数"""
        apiDocParams = ApiDocParams()
        apiDocParams.name = value
        apiDocParams.description = desc
        apiDocParams.type = type
        apiDocParams.required = require
        apiDocParams.example = example
        apiDocParams.remark = remark
        self.params.append(apiDocParams.__dict__)

        data = global_api_doc.get('data')
        if data.get(self.class_name):
            data[self.class_name]['params'].append(
                apiDocParams.__dict__
            )
        else:
            data[self.class_name] = {
                'params': [apiDocParams.__dict__]
            }

    def ApiParamsRequest(self, value: str, type: str, desc: str = '', require: bool = False, example: str = '',
                         remark: str = ''):
        """表示一个请求参数"""

        def decorator(f):
            @wraps(f)
            def wrapper(request, *args, **kwargs):
                self.get_class_name(f)

                # 设置文档参数
                self.setParams(value = value, type = type, require = require,
                               desc = desc if desc else '',
                               example = example if example else '',
                               remark = remark if remark else '')
                # 校验参数
                return f(request, *args, **kwargs)

            return wrapper

        return decorator

    @property
    def checkParams(self):
        """校验参数"""

        def decorator(f):
            self.get_class_name(f)
            data = global_api_doc.get('data')
            params = []

            if data:
                if data.get(self.class_name):
                    if data.get(self.class_name).get('params'):
                        params = data.get(self.class_name).get('params')

            @wraps(f)
            def wrapper(self, request, *args, **kwargs):

                method: list = ['GET', 'POST']

                not_list = []
                if request.method == 'GET':
                    form = request.query_params.copy()
                elif request.method == 'POST':
                    form = request.data.copy()
                else:
                    return ParamsErrorResponse(message = f"只允许{','.join([str(i) for i in method])}请求", code = 40003)

                for i in params:
                    if i.get('name') in list(form.keys()) or not i.get('required'):
                        if form.get(i.get('name')) == '' or form.get(i.get('name')) is None:
                            return ParamsErrorResponse(message = f"{i.get('name')}不能为空")
                    else:
                        not_list.append(i.get('name'))
                if len(not_list) != 0:
                    return ParamsErrorResponse(message = f"{','.join([str(i) for i in not_list])}" + "不能为空")
                return f(self, request, *args, **kwargs)

            return wrapper

        return decorator

    @property
    def start(self):
        """开始"""

        def decorator(f):
            self.get_class_name(f)

            data = global_api_doc.get('data')

            if data.get(self.class_name):
                data[self.class_name].update(
                    {
                        'tag': self.tag,
                        'path': self.path,
                        'method': self.method,
                        'summary': self.summary,
                    }
                )
            else:
                data[self.class_name] = {
                    'tag': self.tag,
                    'path': self.path,
                    'method': self.method,
                    'summary': self.summary,
                    'params': []
                }
            return f

        return decorator


def api_doc():
    api_doc_data = global_api_doc.copy()
    data = api_doc_data.get('data')
    docs = []
    tags = []
    if data:
        for i in data.keys():
            tag = data.get(i).get('tag')
            if tag and tag not in tags:
                tags.append(tag)
                docs.append({
                    'tag': tag
                })
        for i in data.keys():
            for j in docs:
                if data.get(i).get('tag') == j.get('tag'):
                    if j.get('paths'):
                        j['paths'].append({
                            'path': data.get(i).get('path'),
                            'method': data.get(i).get('method'),
                            'summary': data.get(i).get('summary'),
                            'params': data.get(i).get('params'),
                        })
                    else:
                        j['paths'] = [
                            {
                                'path': data.get(i).get('path'),
                                'method': data.get(i).get('method'),
                                'summary': data.get(i).get('summary'),
                                'params': data.get(i).get('params'),
                            }
                        ]

    api_doc_data['data'] = docs
    return api_doc_data
