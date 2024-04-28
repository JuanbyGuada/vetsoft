from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.home, name="home"),
    #CLIENTS
    path("clientes/", view=views.clients_repository, name="clients_repo"),
    path("clientes/nuevo/", view=views.clients_form, name="clients_form"),
    path("clientes/editar/<int:id>/", view=views.clients_form, name="clients_edit"),
    path("clientes/eliminar/", view=views.clients_delete, name="clients_delete"),
    
    #CLIENTS-PRODUCTS
    path('clientes/<int:client_id>/compras/', views.client_purchases, name='client_purchases'),
    path('clientes/<int:client_id>/añadir-compra/', views.add_purchase, name='add_purchase'),

    #PRODUCTS
    path("productos/", view=views.products_repository, name="products_repo"),
    path("productos/nuevo/", view=views.products_form, name="products_form"),
    path("productos/editar/<int:id>/", view=views.products_form, name="products_edit"),
    path("productos/eliminar/", view=views.products_delete, name="products_delete"),
    #PETS
    path("mascotas/", view=views.pets_repository, name="pets_repo"),
    path("mascotas/nuevo/", view=views.pets_form, name="pets_form"),
    path("mascotas/editar/<int:id>/", view=views.pets_form, name="pets_edit"),
    path("mascotas/eliminar/", view=views.pets_delete, name="pets_delete"),
    #PET-MED
    path('pets/<int:pet_id>/medications/', views.pet_medicine_history, name='pet_medicine_history'),
    path('pets/<int:pet_id>/add_medicine/', views.add_medicine_to_pet, name='add_medicine_to_pet'),
    path('pets/<int:pet_id>/medications/edit/<int:med_id>/', views.edit_medicine_for_pet, name='edit_medicine_for_pet'),
    path('pets/<int:pet_id>/medications/delete/<int:medicine_id>/', views.delete_medicine_for_pet, name='delete_medicine_for_pet'),

    #VETS
    path("veterinarios/", view=views.vets_repository, name="vets_repo"),
    path("veterinarios/nuevo/", view=views.vets_form, name="vets_form"),
    path("veterinarios/editar/<int:id>/", view=views.vets_form, name="vets_edit"),
    path("veterinarios/eliminar/", view=views.vets_delete, name="vets_delete"),
    #MEDICINES
    path("medicamentos/", view=views.medicines_repository, name="medicines_repo"),
    path("medicamentos/nuevo/", view=views.medicines_form, name="medicines_form"),
    path("medicamentos/editar/<int:id>/", view=views.medicines_form, name="medicines_edit"),
    path("medicamentos/eliminar/", view=views.medicines_delete, name="medicines_delete"),
    #PROVIDERS
    path("proveedores/", view=views.providers_repository, name="providers_repo"),
    path("proveedores/nuevo/", view=views.providers_form, name="providers_form"),
    path("proveedores/editar/<int:id>/", view=views.providers_form, name="providers_edit"),
    path("proveedores/eliminar/", view=views.providers_delete, name="providers_delete"),
    path('proveedores/<int:provider_id>/productos/', views.provider_products, name='provider_products'),

    #PET_VET
    path('mascota/<int:mascota_id>/', views.mascota_detalle, name='mascota_detalle'),
    path('asociar_veterinario/<int:mascota_id>/', views.asociar_veterinario, name='asociar_veterinario'),
    path('desasociar_veterinario/<int:mascota_id>/<int:veterinario_id>/', views.desasociar_veterinario, name='desasociar_veterinario'),


]


