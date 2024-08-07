from django.shortcuts import render
from django.apps import apps
from django.core.exceptions import AppRegistryNotReady

EXCLUDED_APPS = ['auth']

def is_sellable_model(model):
    sellable_criteria = [
        'name', 'title', 'product_name', 'item_name', 'label',
        'price', 'cost', 'amount', 'value', 'pricing', 'rate', 'charge',
        'description', 'details', 'info', 'summary', 'overview', 'spec', 'specification',
        'quantity', 'amount', 'count', 'number', 'volume', 'total', 'stock',
        'size', 'dimension', 'length', 'width', 'height', 'measurements',
        'weight', 'mass', 'heaviness', 'load', 'burden','service','services',
    ]
    if model._meta.app_label in EXCLUDED_APPS:
        return False

    fields = model._meta.get_fields()
    for field in fields:
        if field.name in sellable_criteria:
            return True
    
    return False

def get_tables_with_sellable_objects():
    try:
        models = apps.get_models()
        sellable_models = []
        for model in models:
            if is_sellable_model(model):
                sellable_models.append(model)
        return sellable_models
    except AppRegistryNotReady:
        return []

def get_sellable_objects():
    sellable_models = get_tables_with_sellable_objects()
    sellable_objects = []

    sellable_criteria = [
        'name', 'title', 'product_name', 'item_name', 'label',
        'price', 'cost', 'amount', 'value', 'pricing', 'rate', 'charge',
        'description', 'details', 'info', 'summary', 'overview', 'spec', 'specification',
        'quantity', 'amount', 'count', 'number', 'volume', 'total', 'stock',
        'size', 'dimension', 'length', 'width', 'height', 'measurements',
        'weight', 'mass', 'heaviness', 'load', 'burden''service','services',
    ]

    for model in sellable_models:
        if model._meta.model_name == 'Permission':
            continue
        objects = model.objects.all()
        for obj in objects:
            obj_data = {'model_name': model.__name__}
            for field in model._meta.get_fields():
                if field.name in sellable_criteria:
                    obj_data[field.name] = getattr(obj, field.name, '')
            sellable_objects.append(obj_data)

    return sellable_objects

def home(request):
    sellable_objects = get_sellable_objects()
    print("Sellable Objects:")
    for obj in sellable_objects:
        print(obj)

    context = {
        'sellable_objects': sellable_objects,
    }
    return render(request, 'home.html', context)
