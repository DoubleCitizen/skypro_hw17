class Serialize:
    def __init__(self, Schema):
        """
        Инициализация класса Serialize, аргументом является схема класса marshmallow
        """
        self.schema = Schema()
        self.schemas = Schema(many=True)

    def serialize(self, Object):
        """
        Сериализация объекта
        """
        result = Object
        return self.schemas.dump(result)

    def serialize_all(self, Object):
        """
        Сериализация списка, объектов
        """
        result = Object.query.all()
        return self.schemas.dump(result)

    def serialize_get(self, Object, pk):
        """
        Сериализация объекта по pk
        """
        result = Object.query.get(pk)
        return self.schema.dump(result)
