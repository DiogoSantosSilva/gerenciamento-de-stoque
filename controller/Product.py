from datetime import datetime

from model.Product import Product


class ProductController:

    def __init__(self):
        self.product_model = Product()

    def get_products(self, limit):
        result = []
        try:
            response = self.product_model.get_all(limit=limit)
            for product in response:
                result.append(
                    {
                        "id": product.id,
                        "name": product.name,
                        "description": product.description,
                        "qtd": str(product.qtd),
                        "price": str(product.price),
                        "image": product.image,
                        "date_created": product.date_created
                    }
                )
            status = 200
        except Exception as error:
            result = []
            print(error)
            status = 400
        finally:
            return {
                "result": result,
                "status": status
            }

    def get_product_by_id(self, product_id):
        result = {}
        try:
            self.product_model.id = product_id
            product = self.product_model.get_product_by_id()
            result = {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "qtd": str(product.qtd),
                "price": str(product.price),
                "image": product.image,
                "date_created": product.date_created
            }
        except Exception as error:
            print(error)
            result = []
            status = 400
        finally:
            return {
                "result": result,
                "status": status
            }

    def save_product(self, obj):
        self.product_model.name = obj["name"]
        self.product_model.description = obj["description"]
        self.product_model.qtd = obj["qtd"]
        self.product_model.price = obj["price"]
        self.product_model.date_created = datetime.now()
        self.product_model.status = 1
        self.product_model.category = obj["category"]
        self.product_model.user_created = obj["user_created"]
        return self.product_model.save()

    def update_product(self, obj):
        self.product_model.id = obj["id"]
        return self.product_model.update(obj)

    def delete_product(self, obj):
        self.product_model.id = obj["id"]
        return self.product_model.delete()
