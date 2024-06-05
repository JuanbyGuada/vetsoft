from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Client, Product, Pet, Vet, Medicine, Provider, Sale, PetMedicine, Appointment


def home(request):

    """
    Renderiza la página de inicio.

    Returns:
        HttpResponse: La respuesta que contiene la página de inicio renderizada.
    """

    return render(request, "home.html")


def clients_repository(request):

    """
    Renderiza la página del repositorio de clientes con todos los clientes.

    """
     
    clients = Client.objects.all()
    return render(request, "clients/repository.html", {"clients": clients})


def clients_form(request, id=None):

    """
    Maneja el formulario de cliente para crear o actualizar un cliente.

    Args:
        request (HttpRequest):
            - Si la solicitud es POST y el cliente se guarda o se actualiza con éxito, redirige al repositorio de clientes.
            - Si la solicitud es POST y hay errores, renderiza el formulario de cliente con los errores.
            - Si la solicitud es GET, renderiza el formulario de cliente con los datos existentes si se proporciona un ID, 
              o un formulario vacío si no se proporciona ningún ID
        id (int, opcional): El ID del cliente para actualizar un cliente existente. Por defecto es None.

    Returns:
        Si se guarda bien o se edita con éxito, redirige al repositorio 
        Si hay errores, los devuelve al form.html
    """

    if request.method == "POST":
        client_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if client_id == "":
            saved, errors = Client.save_client(request.POST)
        else:
            client = get_object_or_404(Client, pk=client_id)
            client.update_client(request.POST)

        if saved:
            return redirect(reverse("clients_repo"))

        return render(
            request, "clients/form.html", {"errors": errors, "client": request.POST}
        )

    client = None
    if id is not None:
        client = get_object_or_404(Client, pk=id)

    return render(request, "clients/form.html", {"client": client})


def clients_delete(request):

    """
    Elimina un cliente.

    Si se elimina con éxito, redirige a la página del repositorio de clientes.
    """

    client_id = request.POST.get("client_id")
    client = get_object_or_404(Client, pk=int(client_id))
    client.delete()

    return redirect(reverse("clients_repo"))


#provider


def providers_repository(request):
    """
    Renderiza la página del repositorio de proveedores con todos los proveedores.

    """
    providers = Provider.objects.all()
    return render(request, "providers/repository.html", {"providers": providers})


def providers_form(request, id=None):

    """
    Maneja el formulario de proveedor para crear o actualizar un proveedor.

    Args:
        request (HttpRequest): POST o GET
        id (int, opcional): El ID del proveedor para actualizar un proveedor existente. Por defecto es None.

    """

    
    if request.method == "POST":
        provider_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if provider_id == "":
            saved, errors = Provider.save_provider(request.POST)
        else:
            provider = get_object_or_404(Provider, pk=provider_id)
            provider.update_provider(request.POST)

        if saved:
            return redirect(reverse("providers_repo"))

        return render(
            request, "providers/form.html", {"errors": errors, "provider": request.POST}
        )

    provider = None
    if id is not None:
        provider = get_object_or_404(Provider, pk=id)

    return render(request, "providers/form.html", {"provider": provider})

def provider_products(request, provider_id):

    """
    Renderiza la página con una lista de productos de un proveedor determinado, encontrado por provider_id.

    """
    provider = get_object_or_404(Provider, pk=provider_id)
    products = Product.objects.filter(provider=provider)
    return render(request, 'providers/products.html', {'provider': provider, 'products': products})


def providers_delete(request):

    """
    Elimina un proveedor de la base de datos.
    """

    provider_id = request.POST.get("provider_id")
    provider = get_object_or_404(Provider, pk=int(provider_id))
    provider.delete()

    return redirect(reverse("providers_repo"))



#product


def products_repository(request):

    """
    Renderiza la página del repositorio de productos que se encuentran en la base de datos.
    """

    products = Product.objects.all()
    return render(request, "products/repository.html", {"products": products})


def products_form(request, id=None):

    """
    Renderiza el formulario de productos para crear o actualizar un producto.
    """

    errors = {}
    providers = Provider.objects.all()
    product = None # Inicializamos la variable product como None

    if request.method == "POST":
        product_id = request.POST.get("id")
        product_data = {
            "name": request.POST.get("name"),
            "type": request.POST.get("type"),
            "price": request.POST.get("price"),
            "provider": request.POST.get("provider")
        }

        if product_id:
            product = get_object_or_404(Product, pk=product_id)
            saved, errors = product.update_product(product_data)
        else:
            saved, errors = Product.save_product(product_data)

        if saved:
            return redirect(reverse("products_repo"))

    else:
        if id is not None:
            product = get_object_or_404(Product, pk=id)
        else:
            product = None

    return render(request, "products/form.html", {"product": product, "providers": providers, "errors": errors})



def products_delete(request):

    """
    Se elimina un producto de la base de datos
    """
    product_id = request.POST.get("product_id")
    product = get_object_or_404(Product, pk=int(product_id))
    product.delete()

    return redirect(reverse("products_repo"))




#sale

def client_purchases(request, client_id):

    """
    Se muestra todas los productos que el cliente ha comprado
    """
    client = get_object_or_404(Client, id=client_id)
    purchases = Sale.objects.filter(client=client)
    return render(request, 'clients/products/client_purchases.html', {'client': client, 'purchases': purchases})


def add_purchase(request, client_id):

    """
    Se agrega un producto a la lista de compras del cliente
    """
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        
        existing_sale = Sale.objects.filter(client=client, product=product).exists()
        
        if not existing_sale:
            Sale.objects.create(client=client, product=product)
        

        return redirect('client_purchases', client_id=client.id)
    else:
        products = Product.objects.all()
        return render(request, 'clients/products/addproduct.html', {'products': products, 'client': client})
    
#pet

def pets_repository(request):

    """
    Renderiza la página del repositorio de mascotas con todas las mascotas en la base de datos.
    """
    pets = Pet.objects.all()
    return render(request, "pets/repository.html", {"pets": pets})

def pets_form(request, id=None):

    """
    Función que se encarga de manejar el formulario de mascotas para crear o actualizar una mascota.
    """
    clients = Client.objects.all()
    return_url = request.GET.get('return_url') or request.META.get('HTTP_REFERER')

    if request.method == "POST":
        return_url = request.POST.get('return_url', request.GET.get('return_url', request.META.get('HTTP_REFERER')))
        pet_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if pet_id == "":
            client_id = request.POST.get("client_id", "")
            if client_id:
                request.POST["client_id"] = int(client_id)
            saved, errors = Pet.save_pet(request.POST)
        else:
            pet = get_object_or_404(Pet, pk=pet_id)
            pet.update_pet(request.POST)

        if saved:
            return HttpResponseRedirect(return_url) 
   
        return render(
            request, "pets/form.html", {"errors": errors, "pet": request.POST, "clients": clients , "return_url": return_url}
        )


    pet = None
    if id is not None:
        pet = get_object_or_404(Pet, pk=id)

    return render(request, "pets/form.html", {"pet": pet, "clients": clients, "return_url": return_url})



def pets_delete(request):

    """
    Elimina una mascota de la base de datos.
    """
    pet_id = request.POST.get("pet_id")
    pet = get_object_or_404(Pet, pk=int(pet_id))
    pet.delete()

    return redirect(reverse("pets_repo"))

# vet

def vets_repository(request):

    """
    Se renderiza la página del repositorio de veterinarios con todos los veterinarios en la base de datos.
    """
    vets = Vet.objects.all()
    return render(request, "vets/repository.html", {"vets": vets})

def vets_form(request, id=None):

    """
    Función que se encarga de manejar el formulario de veterinarios para crear o actualizar un veterinario.
    """
    if request.method == "POST":
        vet_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if vet_id == "":
            saved, errors = Vet.save_vet(request.POST)
        else:
            vet = get_object_or_404(Vet, pk=vet_id)
            vet.update_vet(request.POST)

        if saved:
            return redirect(reverse("vets_repo"))

        return render(
            request, "vets/form.html", {"errors": errors, "vet": request.POST}
        )

    vet = None
    if id is not None:
        vet = get_object_or_404(Vet, pk=id)

    return render(request, "vets/form.html", {"vet": vet})

def vets_delete(request):

    """
    Elimina un veterinario de la base de datos.
    """
    vet_id = request.POST.get("vet_id")
    vet = get_object_or_404(Vet, pk=int(vet_id))
    vet.delete()

    return redirect(reverse("vets_repo"))



#pet-vet(cita)


def pet_appointments_history(request, pet_id):

    """
    Función que se encarga de mostrar todas las citas de una mascota.
    """
    pet = get_object_or_404(Pet, id=pet_id)
    appointments = pet.appointments.all()
    return render(request, 'pet-vet/citas.html', {'pet': pet, 'appointments': appointments})

def add_appointment_to_pet(request, pet_id):

    """
    Función que se encarga de agregar una cita a una mascota.
    """
    pet = get_object_or_404(Pet, id=pet_id)
    vets = Vet.objects.all()
    if request.method == 'POST':
        form_data = {
            'pet': pet.id,
            'vet': request.POST['vet_id'],
            'date': request.POST['date']
        }
        success, errors = Appointment.save_appointment(form_data)
        if success:
            return redirect('pet_appointments_history', pet_id=pet.id)
        else:
            return render(request, 'pet-vet/asociar_veterinario.html', {
                'pet': pet, 
                'vets': vets, 
                'errors': errors
            })

    return render(request, 'pet-vet/asociar_veterinario.html', {'pet': pet, 'vets': vets})




def delete_appointment(request, appointment_id):

    """
    Función que se encarga de eliminar una cita de la base de datos.
    """
    if request.method == 'POST':
        appointment = get_object_or_404(Appointment, id=appointment_id)
        appointment.delete()
        return redirect('pet_appointments_history', pet_id=appointment.pet.id)


def mascota_detalle(request, mascota_id):

    """
    Se muestra a los veterinarios asociados a una mascota.
    """
    mascota = get_object_or_404(Pet, pk=mascota_id)
    veterinarios = Vet.objects.filter(appointments__pet=mascota).distinct()
    return render(request, 'pet-vet/mascota_detalle.html', {'mascota': mascota, 'veterinarios': veterinarios})

#client-pet

def client_pets(request, client_id):

    """
    Se muestra todas las mascotas de un cliente.

    """
    client = get_object_or_404(Client, id=client_id)
    pets = client.pets.all()
    return render(request, 'clients/pets/repository.html', {'client': client, 'pets': pets})


#medicine
def medicines_repository(request):


    """
    Renderiza la página del repositorio de medicamentos con todos los medicamentos en la base de datos.
    """
    medicines = Medicine.objects.all()
    return render(request, "medicines/repository.html", {"medicines": medicines})

def medicines_form(request, id=None):

    """
    Función que se encarga de manejar el formulario de medicamentos para crear o actualizar un medicamento.
    """
    errors = {}
    medicine_data = {
        "name": "",
        "description": "",
        "dose": ""
    }
    if request.method == "POST":
        medicine_data = {
            "name": request.POST.get("name", ""),
            "description": request.POST.get("description", ""),
            "dose": request.POST.get("dose", "")
        }
        medicine_id = request.POST.get("id", "")
        saved = True

        if medicine_id == "":
            saved, errors = Medicine.save_medicine(medicine_data)
        else:
            medicine = get_object_or_404(Medicine, pk=medicine_id)
            saved, errors = medicine.update_medicine(medicine_data)

        if saved:
            return redirect(reverse("medicines_repo"))

        return render(
            request, "medicines/form.html", {"errors": errors, "medicine": request.POST}
        )

    medicine = None
    if id is not None:
        medicine = get_object_or_404(Medicine, pk=id)

    return render(request, "medicines/form.html", {"errors": errors, "medicine": medicine})

def medicines_delete(request):

    """
    Función que elimina un medicamento de la base de datos.
    """
    medicine_id = request.POST.get("medicine_id")
    medicine = get_object_or_404(Medicine, pk=int(medicine_id))
    medicine.delete()

    return redirect(reverse("medicines_repo"))



#pet-med


def pet_medicine_history(request, pet_id):

    """
    Se muestra el historial de medicamentos de una mascota.
    """
    pet = get_object_or_404(Pet, id=pet_id)
    medications = pet.medications.all()
    return render(request, 'pets/meds/pet_medications.html', {'pet': pet, 'medications': medications})

    
def add_medicine_to_pet(request, pet_id):

    """
    Función que se encarga de agregar un medicamento a una mascota.
    
    """
    pet = get_object_or_404(Pet, id=pet_id)
    medicines = Medicine.objects.all()
    if request.method == 'POST':
        form_data = {
            'pet_id': pet.id,
            'medicine_id': request.POST['medicine_id'],
            'administration_date': request.POST['administration_date']
        }
        success, errors = PetMedicine.save_petmed(form_data)
        if success:
            return redirect('pet_medicine_history', pet_id=pet.id)
        else:
            return render(request, 'pets/meds/add_med.html', {'pet': pet, 'medicines': medicines, 'errors': errors})
 
    return render(request, 'pets/meds/add_med.html', {'pet': pet, 'medicines': medicines})


def edit_medicine_for_pet(request, pet_id, med_id):

    """
    Función que se encarga de editar un medicamento de una mascota.
    """
    pet = get_object_or_404(Pet, id=pet_id)
    pet_medicine = get_object_or_404(PetMedicine, id=med_id)
    medicines = Medicine.objects.all()

    if request.method == 'POST':
        medicine_id = request.POST.get('medicine_id')
        administration_date = request.POST.get('administration_date')
        form_data = {
            'medicine': medicine_id,
            'administration_date': administration_date
        }
        
        errors = PetMedicine.validate_petmed(request.POST)
        if not errors:
            pet_medicine.update_petmed(form_data)
            return redirect('pet_medicine_history', pet_id=pet.id)
        else:
            return render(request, 'pets/meds/edit_med.html', {
                'pet': pet,
                'pet_medicine': pet_medicine,
                'medicines': medicines,
                'errors': errors
            })

    return render(request, 'pets/meds/edit_med.html', {
        'pet': pet,
        'pet_medicine': pet_medicine,
        'medicines': medicines
    })



def delete_medicine_for_pet(request, pet_id, medicine_id):

    """
    Función que se encarga de eliminar un medicamento de una mascota.
    """
    if request.method == 'POST':
        pet_medicine = get_object_or_404(PetMedicine, id=medicine_id)
        pet_medicine.delete()
        return redirect('pet_medicine_history', pet_id=pet_id)
    
    #historial medico

def pet_medical_history(request, pet_id):

    """
    Función que se encarga de mostrar el historial médico de una mascota, vinculando las citas y los medicamentos recetados
    """
    pet = get_object_or_404(Pet, pk=pet_id)
    appointments = pet.appointments.all().order_by('date')
    medications = pet.medications.all().order_by('administration_date')

    events = []

    # Agregamos citas
    for appointment in appointments:
        events.append({
            'date': appointment.date,
            'vet': appointment.vet.name,
            'medication': None  # Inicialmente no hay medicamento asociado
        })

    # Agregamos medicamentos
    for medication in medications:
        matched = False
        for event in events:
            if event['date'] == medication.administration_date and not event['medication']:
                event['medication'] = f" {medication.medicine.name}"
                matched = True
                break
        if not matched:
            events.append({
                'date': medication.administration_date,
                'vet': None, 
                'medication': f" {medication.medicine.name}"
            })

    events.sort(key=lambda x: x['date'])

    return render(request, 'pets/medical_history.html', {'pet': pet, 'events': events})



