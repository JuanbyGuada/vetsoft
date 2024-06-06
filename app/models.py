from django.db import models
from datetime import datetime

def validate_client(data):  

    """
    valida los datos del cliente proporcionados en el formulario.

    data: Los datos del cliente. nombre, teléfono, correo electrónico.

    devuelve un diccionario que contiene mensajes de error si la validación falla.
    """

    errors = {}

    name = data.get("name", "")
    phone = data.get("phone", "")
    email = data.get("email", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    return errors


class Client(models.Model):
    '''esta clase representa un cliente en la base de datos que tiene un nombre, teléfono, correo electrónico y dirección'''
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def save_client(cls, client_data):      #esta funcion es para guardar un cliente en la base de datos
        errors = validate_client(client_data)

        if len(errors.keys()) > 0:          #si hay errores en los datos del cliente, se devuelven los errores
            return False, errors

        Client.objects.create(              #si no hay errores, se crea un nuevo cliente en la base de datos
            name=client_data.get("name"),
            phone=client_data.get("phone"),
            email=client_data.get("email"),
            address=client_data.get("address"),
        )

        return True, None

    def update_client(self, client_data):  #función que nos permitirá actualizar un cliente en la base de datos
        self.name = client_data.get("name", "") or self.name
        self.email = client_data.get("email", "") or self.email
        self.phone = client_data.get("phone", "") or self.phone
        self.address = client_data.get("address", "") or self.address
        self.save()

        

    
#  Provider Class

def validate_provider(data):    #función que nos permitirá validar los datos de un proveedor
    
    """
    valida los datos del proveedor proporcionados en el formulario.

    data: Los datos del proveedor. nombre, correo electrónico.

    devuelve un diccionario que contiene mensajes de error si la validación falla.
    """

    errors = {}

    name = data.get("name", "")
    email = data.get("email", "")


    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    return errors


class Provider(models.Model):
    ''''esta clase representa un proveedor en la base de datos que tiene un nombre y un correo electrónico.'''
    name = models.CharField(max_length=100)
    email = models.EmailField()


    @classmethod
    def save_provider(cls, provider_data): #esta función es para guardar un proveedor en la base de datos
        errors = validate_provider(provider_data)

        if len(errors.keys()) > 0:
            return False, errors

        Provider.objects.create(
            name=provider_data.get("name"),
            email=provider_data.get("email"),
        )

        return True, None

    def update_provider(self, provider_data):       #esta función es para actualizar un proveedor en la base de datos
        self.name = provider_data.get("name", "") or self.name
        self.email = provider_data.get("email", "") or self.email

        self.save() 
        
#  Product Class

def validate_product(data):         #función que nos permitirá validar los datos de un producto
    
    """
    valida los datos del producto proporcionados en el formulario.

    data: Los datos del producto. nombre, tipo, precio, proveedor.

    devuelve un diccionario que contiene mensajes de error si la validación falla.
    """
    errors = {}

    name = data.get("name", "")
    type = data.get("type", "")
    price = data.get("price", "")


    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if type == "":
        errors["type"] = "Por favor ingrese un tipo"

    if not price:
        errors["price"] = "Por favor ingrese un precio"
    else:
        price = float(price)
        if price == 0:
            errors["price"] = "Por favor ingrese un precio mayor a 0"
        
        if price < 0:
            errors["price"] = "Por favor ingrese un numero positivo"
        else:
            try:
                price = float(price)
            except ValueError:
                errors["price"] = "El precio debe ser un número"

    return errors


class Product(models.Model):
    '''esta clase representa un producto en la base de datos que tiene un nombre, tipo, precio y un proveedor.'''
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='products')

    @classmethod
    def save_product(cls, product_data):        #esta función es para guardar un producto en la base de datos
        errors = validate_product(product_data)

        if len(errors.keys()) > 0:      #si hay errores en los datos del producto, se devuelven los errores
            return False, errors
        
        provider_id = product_data.get("provider")
        provider = Provider.objects.get(pk=provider_id)

        Product.objects.create(             #si no hay errores, se crea un nuevo producto en la base de datos
            name=product_data.get("name"),
            type=product_data.get("type"),
            price=product_data.get("price"),
            provider=provider,
        )

        return True, None

    def update_product(self, product_data):         #función que nos permitirá actualizar un producto en la base de datos
        error= validate_product(product_data)
        if len(error.keys()) > 0:
            return False, error
        
        self.name = product_data.get("name", "") or self.name
        self.type = product_data.get("type", "") or self.type
        self.price = product_data.get("price", ) or self.price

        if 'provider' in product_data:
            provider_id = product_data.get("provider")
            self.provider = Provider.objects.get(pk=provider_id)
        self.save()
        return True, None 

#client-product (sale)

class Sale(models.Model):
    '''esta clase representa una venta en la base de datos que tiene un cliente y un producto.'''
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:             #esta clase meta nos permite definir restricciones en la base de datos para que un cliente no pueda comprar el mismo producto dos veces.
        unique_together = ['client', 'product'] 


#  Vet Class

def validate_vet(data):

    """
    valida los datos del veterinario proporcionados en el formulario.

    data: Los datos del veterinario. nombre, teléfono, correo electrónico.

    devuelve un diccionario que contiene mensajes de error si la validación falla.
    """
        
    errors = {}

    name = data.get("name", "")
    phone = data.get("phone", "")
    email = data.get("email", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    return errors

class Vet(models.Model):
    '''esta clase representa un veterinario en la base de datos que tiene un nombre, teléfono y correo electrónico.'''
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

    @classmethod
    def save_vet(cls, vet_data):        #esta función es para guardar un veterinario en la base de datos
        errors = validate_client(vet_data)

        if len(errors.keys()) > 0:
            return False, errors

        Vet.objects.create(
            name=vet_data.get("name"),
            email=vet_data.get("email"),
            phone=vet_data.get("phone"),
        )
        return True, None

    def update_vet(self, vet_data):         #función que nos permitirá actualizar un veterinario en la base de datos
        self.name = vet_data.get("name", "") or self.name
        self.email = vet_data.get("email", "") or self.email
        self.phone = vet_data.get("phone", "") or self.phone
    
        self.save()


#  Medicine Class

def validate_medicine(data):

    """
    valida los datos del medicamento proporcionados en el formulario.

    data: Los datos del medicamento. nombre, descripción, dosis.

    devuelve un diccionario que contiene mensajes de error si la validación falla.
    """
    errors = {}

    name = data.get("name", "")
    description = data.get("description", "")
    dose = data.get("dose", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if description == "":
        errors["description"] = "Por favor ingrese una descripción"

    if dose == "":
        errors["dose"] = "Por favor ingrese una dosis"
    else :
        try:
            dose= int(dose)
            if dose < 1 or dose > 10:
                errors["dose"] = "La dosis debe ser un número entre 1 y 10"
        except ValueError:
            errors["dose"] = "La dosis debe ser un número"

    return errors

class Medicine(models.Model):
    '''esta clase representa un medicamento en la base de datos que tiene un nombre, descripción y dosis.'''
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    dose = models.IntegerField()

    def __str__(self):
        return self.name
    
    @classmethod
    def save_medicine(cls, medicine_data):      #esta función es para guardar un medicamento en la base de datos
        errors = validate_medicine(medicine_data)

        if len(errors.keys()) > 0:
            return False, errors

        Medicine.objects.create(
            name=medicine_data.get("name"),
            description=medicine_data.get("description"),
            dose=medicine_data.get("dose"),
        )
        return True, None
    
    def update_medicine(self, medicine_data):       #función que nos permitirá actualizar un medicamento en la base de datos
        errors = validate_medicine(medicine_data)

        if errors:
            return False, errors

        self.name = medicine_data.get("name", "") or self.name
        self.description = medicine_data.get("description", "") or self.description
        self.dose = medicine_data.get("dose", "") or self.dose

        self.save() 

        return True, None

        
#  Pet Class

def validate_pet(data):

    """
    valida los datos de la mascota proporcionados en el formulario.

    data: Los datos de la mascota. nombre, raza, fecha de nacimiento, dueño.

    devuelve un diccionario que contiene mensajes de error si la validación falla.
    """
        
    errors = {}

    name = data.get("name", "")
    breed = data.get("breed", "")
    birthday = data.get("birthday", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if breed == "":
        errors["breed"] = "Por favor ingrese una raza"

    if birthday == "":
        errors["birthday"] = "Por favor ingrese una fecha de nacimiento válida"
    
    return errors

class Pet(models.Model):
    '''esta clase representa una mascota en la base de datos que tiene un nombre, raza, fecha de nacimiento y un dueño.'''
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    birthday= models.DateField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='pets')

    def __str__(self):
        return self.name
    
    @classmethod
    def save_pet(cls, pet_data):
        errors = validate_pet(pet_data)

        if len(errors.keys()) > 0:
            return False, errors

        Pet.objects.create(
            name=pet_data.get("name"),
            breed=pet_data.get("breed"),
            birthday=pet_data.get("birthday"),
            client=Client.objects.get(pk=pet_data.get("client")),
        )
        return True, None
    
    def update_pet(self, pet_data):     #esta función nos permitirá actualizar una mascota en la base de datos
        self.name = pet_data.get("name", "") or self.name
        self.breed = pet_data.get("breed", "") or self.breed
        self.birthday = pet_data.get("birthday", "") or self.birthday

        self.save()

        
#Vet-Pet
class Appointment(models.Model):
    '''esta clase representa una cita en la base de datos que tiene una mascota, un veterinario y una fecha.'''
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='appointments')
    vet = models.ForeignKey(Vet, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()

    def __str__(self):
        return f"Cita para {self.pet.name} con {self.vet.name} el {self.date}"
    
    @staticmethod
    def validate_petvet(data):      #función que nos permitirá validar los datos de una cita
        errors = {}
        date = data.get("date", "")
        if not date:
            errors["date"] = "Por favor ingrese fecha de cita"
        else:
            try:
                parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
                if parsed_date > datetime.now().date():
                    errors["date"] = "La fecha de cita no puede ser mayor a la fecha de hoy"
            except ValueError:
                errors["date"] = "Formato de fecha inválido"
        return errors

    @classmethod
    def save_appointment(cls, pet_vet_data):        #esta función es para guardar una cita en la base de datos
        errors = cls.validate_petvet(pet_vet_data)
        if len(errors.keys()) > 0:
            return False, errors
        
        if Appointment.objects.filter(pet_id=pet_vet_data['pet'], vet_id=pet_vet_data['vet'], date=pet_vet_data['date']).exists():  #validar que no haya una cita duplicada
            errors['duplicate'] = "Ya existe una cita con estos datos."
            return False, errors

        pet = Pet.objects.get(id=pet_vet_data['pet'])
        vet = Vet.objects.get(id=pet_vet_data['vet'])
        Appointment.objects.create(     #si no hay errores, se crea una nueva cita en la base de datos
            pet=pet,
            vet=vet,
            date=pet_vet_data['date']
        )
        return True, None




#Pet-Med


class PetMedicine(models.Model):
    '''Esta clase representa un medicamento administrado a una mascota en la base de datos que tiene una mascota, un medicamento y una fecha de administración.'''
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='medications')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='used_on_pets')
    administration_date = models.DateField()

    def __str__(self):
        return f"{self.medicine.name} administrado a {self.pet.name} el {self.administration_date}"
    
    
    
    @staticmethod
    def validate_petmed(data):      #función que nos permitirá validar los datos de un medicamento administrado a una mascota
        errors = {}
        administration_date = data.get("administration_date", "")

        if not administration_date:
            errors["administration_date"] = "Por favor ingrese fecha de administración"
        else:
            try:
                parsed_date = datetime.strptime(administration_date, "%Y-%m-%d").date()
                if parsed_date > datetime.now().date():
                    errors["administration_date"] = "La fecha de administración no puede ser mayor a la fecha de hoy"
            except ValueError:
                errors["administration_date"] = "Formato de fecha inválido"
        return errors

    @classmethod
    def save_petmed(cls, pet_med_data):         #esta función es para guardar un medicamento administrado a una mascota en la base de datos
        errors = cls.validate_petmed(pet_med_data)

        if len(errors.keys()) > 0:
            return False, errors
        
        pet = Pet.objects.get(id=pet_med_data['pet_id'])
        medicine = Medicine.objects.get(id=pet_med_data['medicine_id'])

        PetMedicine.objects.create(
            pet=pet,
            medicine=medicine,
            administration_date=pet_med_data.get("administration_date"),
        )
        return True, None
    
    def update_petmed(self, pet_med_data):      #esta función nos permitirá actualizar un medicamento administrado a una mascota en la base de datos
        self.administration_date = pet_med_data.get("administration_date", "")
        if 'medicine' in pet_med_data:
            medicine_id = pet_med_data.get("medicine")
            self.medicine = Medicine.objects.get(pk=medicine_id)
        self.save()
