from django.test import TestCase
from app.models import Client
from app.models import Product
from app.models import Provider


class ClientModelTest(TestCase):
    def test_can_create_and_get_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@hotmail.com")

    def test_can_update_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "221555232")

        client.update_client({"phone": "221555233"})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "221555233")

    def test_update_client_with_error(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "221555232")

        client.update_client({"phone": ""})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "221555232")

class ProductModelTest(TestCase):
    def setUp(self):
        # Crear un proveedor para los productos de prueba
        self.provider = Provider.objects.create(name="ProveedorEjemplo", email="correo@utn.com")
        proveedores = Provider.objects.all()
        self.assertEqual(len(proveedores), 1)

    def test_can_create_and_get_product(self):
        success, errors = Product.save_product(
            {
                "name": "Collar de Perro",
                "type": "Ropa",
                "price": 100,
                "provider": self.provider.id,
            }
        )
        self.assertTrue(success)
        products = Product.objects.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].name, "Collar de Perro")
        self.assertEqual(products[0].price, 100)
        self.assertEqual(products[0].type, "Ropa")
        self.assertEqual(products[0].provider, self.provider)

    def test_precio_positivo(self):
        success, errors = Product.save_product(
            {
                "name": "Collar de Perro",
                "type": "Ropa",
                "price": 100,
                "provider": self.provider.id,
            }
        )
        self.assertIsNone(errors)
        self.assertTrue(success)
        products = Product.objects.all()
        self.assertEqual(len(products), 1)

    def test_precio_negativo(self):
        success, errors = Product.save_product(
            {
                "name": "Collar de Perro",
                "type": "Ropa",
                "price": -100,
                "provider": self.provider.id,
            }
        )
        self.assertFalse(success)
        self.assertIn("price", errors)
        self.assertEqual(errors["price"], "Por favor ingrese un numero positivo")
        products = Product.objects.all()
        self.assertEqual(len(products), 0)

    def test_precio_nulo(self):
        success, errors = Product.save_product(
            {
                "name": "Collar de Perro",
                "type": "Ropa",
                "price": 0,
                "provider": self.provider.id,
            }
        )
        self.assertFalse(success)
        self.assertIn("price", errors)
        self.assertEqual(errors["price"], "Por favor ingrese un precio")
        products = Product.objects.all()
        self.assertEqual(len(products), 0)