SqlalchemyModelConvert
===
- Use simple and convenient model transform dictionary module(Python3)
- Model objects are converted to dictionaries, and list model objects are converted to list dictionaries
- Support for association model conversion, no need to display fields, field value modification


### Installation【安装】
pip install sqlalchemy-model-convert


# Examples【示例】
### Defined model class，Inherited ModelConvert

```python
class Role(db.Model, ModelConvert):
    """Role"""
    __tablename__ = 'tbl_roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)

    users = db.relationship('User', backref='role')


class User(db.Model, ModelConvert):
    """User"""
    __tablename__ = 'tbl_users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('tbl_roles.id'))
```
### Model object transform dictionary
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

Associated model transformation with fields that do not need to be displayed

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
Association model conversion(Associated list model objects)

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
Field value modification，Override the set_field _value method in the model class

```python
class User(db.Model, ModelConvert):
    """User"""
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

### List model object transform list
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
Model objects associated with model objects in the list，Fields in the list that model objects do not need to display

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
