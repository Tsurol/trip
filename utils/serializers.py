# 序列化:将django ORM对象转成python字典


class BaseSerializers(object):
    def __init__(self, obj):
        self.obj = obj

    def to_dict(self):
        return {}


class MetaSerializers(object):
    """ 分页元数据 """

    def __init__(self, current_page, page_count, total_count, **kwargs):
        """
        :param current_page:当前第几页
        :param page_count:总页数
        :param total_count:总记录数
        """
        self.current_page = current_page
        self.page_count = page_count
        self.total_count = total_count

    def to_dict(self):
        return {
            'total_count': self.total_count,
            'page_count': self.page_count,
            'current_page': self.current_page,
        }


class BaseListPageSerializers(object):
    """ 分页类的封装 """

    def __init__(self, page_obj, paginator=None, object_list=[]):
        """
        :param page_obj:分页当前页的对象
        :param paginator:分页器对象
        :param object_list:当前页的数据列表
        """
        self.page_obj = page_obj
        self.paginator = paginator if paginator else page_obj.paginator
        self.object_list = object_list if object_list else page_obj.object_list

    def get_object(self, obj):
        return {}

    def to_dict(self):
        meta = MetaSerializers(current_page=self.page_obj.number,
                               page_count=self.paginator.num_pages,
                               total_count=self.paginator.count)
        meta = meta.to_dict()
        objects = []
        for obj in self.object_list:
            objects.append(self.get_object(obj))
        return {
            'meta': meta,
            'objects': objects
        }
