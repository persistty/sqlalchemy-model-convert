class ModelConvert(object):
    """模型转换类，把对象转换成对应的字典"""
    @classmethod
    def key_values_list(cls, models, related_models=[], ignore_fields=[]):
        """
        把对象列表转换成字典列表
        :param models: 要转换的对象列表
        :param related_models: 列表里面模型对象要显示关联查询的对象
        :param ignore_fields: 列表里面模型对象不需要显示的字段
        :return: 返回列表
        """
        return cls.__convert_list(models, related_models, ignore_fields)

    def key_values(self, related_models=[], ignore_fields=[]):
        """
        把对象转换成字典
        :param related_models: 要显示关联查询的对象
        :param ignore_fields: 不需要显示的字段
        :return: 返回字典
        """
        if not hasattr(self, '__table__'):
            return self.__dict__

        columns = self.__table__.columns
        attrs_dict = self.__convert_field(columns, ignore_fields)

        for model in related_models:
            value = getattr(self, model)
            if isinstance(value, ModelConvert):
                attrs_dict[model] = value.key_values()
            elif isinstance(value, list):
                attrs_dict[model] = self.key_values_list(value)

        return attrs_dict

    def __convert_field(self, fields, ignore_fields=[]):
        """转换数据库对应的字段"""
        field_dict = dict()
        for column in fields:
            field = column.name
            if field in ignore_fields:
                continue
            value = getattr(self, field, None)
            field_dict[field] = self.set_field_value(field, value)

        return field_dict

    @classmethod
    def __convert_list(cls, models, related_models=[], ignore_fields=[]):
        """转换一个列表"""
        list_dicts = list()
        for model in models:
            if isinstance(model, ModelConvert):
                list_dicts.append(model.key_values(related_models, ignore_fields))
            else:
                list_dicts.append(model)

        return list_dicts

    def set_field_value(self, field, value):
        """
        设置对应字段的值，重写该方法，对特殊字段值的修改，例如日期字段值的修改
        :param field: 字段名
        :param value: 值
        :return: 返回修改的值
        """
        return value
