from django.shortcuts import render,get_object_or_404
from django.db.models import Q
from django.views import View
from django.core import serializers
from django.http import JsonResponse
from django import forms
from .models import Product
from django.views.decorators.csrf import csrf_exempt
from dialogflow_fulfillment import WebhookClient
import json
from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

@csrf_exempt
def dialogflow_webhook(request):
    if request.method == 'POST':
        # Parse the incoming JSON request from Dialogflow
        req = json.loads(request.body)
        params = req.get('queryResult').get('parameters')
        print(params)
        return JsonResponse({'fulfillmentText': 'Your pizza order has been received.'})



class SearchForm(forms.Form):
    query = forms.CharField()

def store(request):
     context = {}
     return render(request, 'store/index.html', context)
def about(request):
     context = {}
     return render(request, 'store/about.html', context)
def contact(request):
     context = {}
     return render(request, 'store/contact.html', context)
def product_search(request):
    form = SearchForm(request.POST)
    #print(form)
    if form.is_valid():
        query = form.cleaned_data['query']
        print(query)
        if query:
        #products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        #return render(request, 'search_results.html', {'query': query, 'products': products})
            data_dict = get_dict_from_data()
            context = {'data': data_dict}
            return render(request, 'store/product_recommendations.html', context)
        else:
            data_dict = get_dict_from_data()
            context = {'data': data_dict}
            return render(request, 'store/product_recommendations.html', context)    
    else:
        data_dict = get_dict_from_data()
        context = {'data': data_dict}
        return render(request, 'store/product_recommendations.html', context)   
        #return render(request, 'store/product_recommendations.html', {'form': form})
def search(request):
    query = request.GET.get('q')
    print(query)
    #if query:
    #    products = Product.objects.filter(
    #        Q(name__icontains=query) |
    #        Q(description__icontains=query)
    #    )
    #else:
    #    products = Product.objects.all()
    data_dict = get_dict_from_data()
    context = {'data': data_dict}
    return render(request, 'store/product_recommendations.html', context)

def get_dict_from_data():
    import csv
    # Define the filename of the CSV file
    filename = BASE_DIR / "data.csv"

    # Define the header row as a list
    header = []

    # Create an empty dictionary to store the data
    data_dict = {}

    # Open the CSV file in read mode
    with open(filename, mode='r') as file:

        csv_reader = csv.reader(file)

        header = next(csv_reader)
        
        for row in csv_reader:

            # Get the key (value of a particular column)
            key = row[header.index("asin")]
            columns = [header.index("description"),header.index("title"),header.index("category"), header.index("image"), header.index("brand"),
                                                                                        header.index("price")]
            data_dict[key] = {}
            # Create a dictionary of the other column-value pairs
            for i in range(len(row)):
                if i in columns:
                    if i != header.index("image") :
                        data_dict[key][header[i]] = row[i]
                    else :
                        #print(data_dict[key][header[i]])
                        import ast
                        img_list = ast.literal_eval(row[i])
                        data_dict[key][header[i]] = img_list
    return data_dict

class ProductRecommendationsView(View):
    def get(self, request):
        data_dict = get_dict_from_data()
        context = {'data': data_dict}
        return render(request, 'store/product_recommendations.html', context)
        #recommended_products = Product.objects.order_by('?')[:6]
        #data = serializers.serialize('json', recommended_products)
        #return JsonResponse({'products': data})


def product_detail(request, id):
    data_dict = get_dict_from_data()
    return render(request, 'store/single-product.html', {'product': data_dict[id]})