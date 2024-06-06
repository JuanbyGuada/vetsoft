import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect, Browser

from django.urls import reverse
from app.models import Client, Provider, Medicine
from app.context_processors import links

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
playwright = sync_playwright().start()
headless = os.environ.get("HEADLESS", 1) == 1
slow_mo = os.environ.get("SLOW_MO", 0)


class PlaywrightTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser: Browser = playwright.firefox.launch(
            headless=headless, slow_mo=int(slow_mo)
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()

    def setUp(self):
        super().setUp()
        self.page = self.browser.new_page()

    def tearDown(self):
        super().tearDown()
        self.page.close()


class HomeTestCase(PlaywrightTestCase):
     def test_should_have_navbar_with_links(self):
        self.page.goto(self.live_server_url)

        for link_info in links:
            link_label = link_info['label']

            # se construye el selector basado en el enlace label
            link_selector = f'[data-testid="navbar-{link_label}"]'
            
            # se espera que el selector esté en la página
            nav_link = self.page.wait_for_selector(link_selector)

            assert nav_link.is_visible()
            assert nav_link.inner_text().strip() == link_label


        
     def  test_should_have_home_cards_with_links(self): 
            self.page.goto(self.live_server_url)

            home_clients_link = self.page.get_by_test_id("home-Clientes")
            home_pets_link = self.page.get_by_test_id("home-Mascotas")


            expect(home_clients_link).to_be_visible()
            expect(home_clients_link).to_have_attribute("href", reverse("clients_repo"))

            expect(home_pets_link).to_be_visible()
            expect(home_pets_link).to_have_attribute("href", reverse("pets_repo"))

            home_products_link = self.page.get_by_test_id("home-Productos")
            expect(home_products_link).to_be_visible()
            expect(home_products_link).to_have_attribute("href", reverse("products_repo"))

            home_vets_link = self.page.get_by_test_id("home-Veterinarios")
            expect(home_vets_link).to_be_visible()
            expect(home_vets_link).to_have_attribute("href", reverse("vets_repo"))

            home_medicines_link = self.page.get_by_test_id("home-Medicamentos")
            expect(home_medicines_link).to_be_visible()
            expect(home_medicines_link).to_have_attribute("href", reverse("medicines_repo"))

            home_providers_link = self.page.get_by_test_id("home-Proveedores")
            expect(home_providers_link).to_be_visible()
            expect(home_providers_link).to_have_attribute("href", reverse("providers_repo"))
        

class ClientsRepoTestCase(PlaywrightTestCase):
    def test_should_show_message_if_table_is_empty(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).to_be_visible()

    def test_should_show_clients_data(self):
        Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        Client.objects.create(
            name="Guido Carrillo",
            address="1 y 57",
            phone="221232555",
            email="goleador@gmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).not_to_be_visible()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("13 y 44")).to_be_visible()
        expect(self.page.get_by_text("221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("1 y 57")).to_be_visible()
        expect(self.page.get_by_text("221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@gmail.com")).to_be_visible()

    def test_should_show_add_client_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        add_client_action = self.page.get_by_role(
            "link", name="Nuevo cliente", exact=False
        )
        expect(add_client_action).to_have_attribute("href", reverse("clients_form"))

    def test_should_show_client_edit_action(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id})
        )

    def test_should_show_client_delete_action(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de cliente"
        )
        client_id_input = edit_form.locator("input[name=client_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("clients_delete"))
        expect(client_id_input).not_to_be_visible()
        expect(client_id_input).to_have_value(str(client.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_client(self):
        Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("clients_delete"))

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()



class ClientCreateEditTestCase(PlaywrightTestCase):
    def test_should_be_able_to_create_a_new_client(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.get_by_label("Email").fill("brujita75@hotmail.com")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()
        expect(self.page.get_by_text("13 y 44")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.get_by_label("Email").fill("brujita75")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(
            self.page.get_by_text("Por favor ingrese un teléfono")
        ).not_to_be_visible()

        expect(
            self.page.get_by_text("Por favor ingrese un email valido")
        ).to_be_visible()

    def test_should_be_able_to_edit_a_client(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        path = reverse("clients_edit", kwargs={"id": client.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Guido Carrillo")
        self.page.get_by_label("Teléfono").fill("221232555")
        self.page.get_by_label("Email").fill("goleador@gmail.com")
        self.page.get_by_label("Dirección").fill("1 y 57")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()
        expect(self.page.get_by_text("13 y 44")).not_to_be_visible()
        expect(self.page.get_by_text("221555232")).not_to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).not_to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("1 y 57")).to_be_visible()
        expect(self.page.get_by_text("221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@gmail.com")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id})
        )

class ProductCreateEditTestCase(PlaywrightTestCase):
    def setUp(self):
        super().setUp()
        # Crear un proveedor para los tests
        self.provider = Provider.objects.create(name="ProveedorEjemplo", email="correo@utn.com")
        
    def test_should_be_able_to_create_product_with_valid_price(self):
        with playwright.chromium.launch() as browser:

            page = browser.new_page()
            page.goto(f"{self.live_server_url}{reverse('products_form')}")

            page.wait_for_load_state("networkidle")

            expect(page.get_by_role("form")).to_be_visible()

            page.get_by_label("Nombre").fill("Collar de Perro") 
            page.get_by_label("Tipo").fill("Ropa")
            page.get_by_label("Precio").fill("100")
            page.select_option("#provider", str(self.provider.id))



            page.get_by_role("button", name="Guardar").click()

            expect(page.get_by_text("Collar de Perro")).to_be_visible()
            expect(page.get_by_text("Ropa")).to_be_visible()
            expect(page.get_by_text("100")).to_be_visible()
            expect(page.get_by_text("ProveedorEjemplo")).to_be_visible()

    def test_create_product_with_invalid_data(self):
        with playwright.chromium.launch() as browser:
            page = browser.new_page()
            page.goto(f"{self.live_server_url}{reverse('products_form')}")

            page.wait_for_load_state("networkidle")

            expect(page.get_by_role("form")).to_be_visible()

            page.get_by_label("Nombre").fill("Collar de Perro") 
            page.get_by_label("Tipo").fill("Ropa")
            page.get_by_label("Precio").fill("-3")
            page.select_option("#provider", str(self.provider.id))

            page.get_by_role("button", name="Guardar").click()

            assert page.url == f"{self.live_server_url}{reverse('products_form')}"

            assert "Por favor ingrese un numero positivo" in page.inner_text("#price + .invalid-feedback")

class MedicineCreateEditTestCase(PlaywrightTestCase):
    def test_should_be_able_to_create_medicine_with_valid_dose(self):
        with playwright.chromium.launch() as browser:

            page = browser.new_page()
            page.goto(f"{self.live_server_url}{reverse('medicines_form')}")

            page.wait_for_load_state("networkidle")

            expect(page.get_by_role("form")).to_be_visible()

            page.get_by_label("Nombre").fill("MedicineA") 
            page.get_by_label("Descripción").fill("DescriptionA")
            page.get_by_label("Dosis").fill("5")



            page.get_by_role("button", name="Guardar").click()

            expect(page.get_by_text("MedicineA")).to_be_visible()
            expect(page.get_by_text("DescriptionA")).to_be_visible()
            expect(page.get_by_text("5")).to_be_visible()

    def test_create_medicine_with_invalid_data(self):
        with playwright.chromium.launch() as browser:
            page = browser.new_page()
            page.goto(f"{self.live_server_url}{reverse('medicines_form')}")

            page.wait_for_load_state("networkidle")

            expect(page.get_by_role("form")).to_be_visible()

            page.get_by_label("Nombre").fill("") 
            page.get_by_label("Descripción").fill("DescriptionA")
            page.get_by_label("Dosis").fill("abc") 

            page.get_by_role("button", name="Guardar").click()

            assert page.url == f"{self.live_server_url}{reverse('medicines_form')}"

            assert "Por favor ingrese un nombre" in page.inner_text("#name + .invalid-feedback")
            assert "La dosis debe ser un número" in page.inner_text("#dose + .invalid-feedback")

    def  test_should_be_able_to_edit_a_medicine(self):
            
            medicine = Medicine.objects.create(
            name="MedicineA",
            description="DescriptionA",
            dose="5",)

            path = reverse("medicines_edit", kwargs={"id": medicine.id})

            self.page.goto(f"{self.live_server_url}{path}")

            self.page.get_by_label("Nombre").fill("MedicineB")
            self.page.get_by_label("Descripción").fill("DescriptionB")
            self.page.get_by_label("Dosis").fill("8")

            self.page.get_by_role("button", name="Guardar").click()

            expect(self.page.get_by_text("MedicineA")).not_to_be_visible()
            expect(self.page.get_by_text("DescriptionA")).not_to_be_visible()
            expect(self.page.get_by_text("5")).not_to_be_visible()

            expect(self.page.get_by_text("MedicineB")).to_be_visible()
            expect(self.page.get_by_text("DescriptionB")).to_be_visible()
            expect(self.page.get_by_text("8")).to_be_visible()


            edit_action = self.page.get_by_role("link", name="Editar")
            expect(edit_action).to_have_attribute(
                "href", reverse("medicines_edit", kwargs={"id": medicine.id})
            )

