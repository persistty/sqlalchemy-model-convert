SqlalchemyModelConvert
===
- 使用简单方便的模型转字典模块(Python3)
- 模型对象转换成字典，列表模型对象转换成列表
- 支持关联模型转换，不需要显示的字段，字段值的修改


### Manually【手动导入】
下载sqlalchemy_model_convert.py文件


# Examples【示例】
### 定义的模型类，继承ModelConvert

```python
class Role(db.Model, ModelConvert):
    """角色"""
    __tablename__ = 'tbl_roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)

    users = db.relationship('User', backref='role')


class User(db.Model, ModelConvert):
    """用户"""
    __tablename__ = 'tbl_users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('tbl_roles.id'))
```
### 模型对象转换字典
```python
user = User.query.first()
print(user.key_values())

/***********************************************/

{
  "id": 1, 
  "name": "xiaowang", 
  "password": "123456", 
  "role_id": 1
}
```

关联模型的转换，不需要显示的字段

```python
user = User.query.first()
print(user.key_values(related_models=['role'], ignore_fields=['role_id']))

/***********************************************/

{
  "id": 1, 
  "name": "xiaowang", 
  "password": "123456", 
  "role": {
    "id": 1, 
    "name": "Python"
  }
}
```
关联模型的转换(关联的列表模型对象)

```python
role = Role.query.first()
print(role.key_values(related_models=['users']))

/***********************************************/

{
  "id": 2, 
  "name": "Java", 
  "users": [
    {
      "id": 3, 
      "name": "xiaoliu", 
      "password": "123456", 
      "role_id": 2
    }
  ]
}
```
字段值的修改，在模型类中重写set_field _value方法

```python
class User(db.Model, ModelConvert):
    """用户"""
    __tablename__ = 'tbl_users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('tbl_roles.id'))

    def set_field_value(self, field, value):
        if field == 'password':
            return '6666666'
        return value
        
user = User.query.first()
print(user.key_values())

/***********************************************/

{
  "id": 1, 
  "name": "xiaowang", 
  "password": "6666666", 
  "role_id": 1
}
```

### 列表模型对象转换列表
```python
users = User.query.all()
print(User.key_values_list(users))

/***********************************************/

[
  {
    "id": 1, 
    "name": "xiaowang", 
    "password": "123456", 
    "role_id": 1
  }, 
  {
    "id": 2, 
    "name": "xiaoli", 
    "password": "123456", 
    "role_id": 1
  }, 
  {
    "id": 3, 
    "name": "xiaoliu", 
    "password": "123456", 
    "role_id": 2
  }
]
```
列表里面模型对象关联的模型对象，列表里面模型对象不需要显示的字段

```python
users = User.query.all()
print(User.key_values_list(users, related_models=['role'], ignore_fields=['role_id']))

/***********************************************/

[
  {
    "id": 1, 
    "name": "xiaowang", 
    "password": "123456", 
    "role": {
      "id": 1, 
      "name": "Python"
    }
  }, 
  {
    "id": 2, 
    "name": "xiaoli", 
    "password": "123456", 
    "role": {
      "id": 1, 
      "name": "Python"
    }
  }, 
  {
    "id": 3, 
    "name": "xiaoliu", 
    "password": "123456", 
    "role": {
      "id": 2, 
      "name": "Java"
    }
  }
]
```
