from sqlite3 import Cursor
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404, redirect
from .models import Calculation, RadiusData, Neighborhood, Tree, Street, Result, TreeType
from .forms import CreateNewTree, DeleteForm
from django.views import generic
from django.db import connection
import decimal 
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django import template
import json


# Create your views here.
#view function for the home webpage
def home(request):
    return render(request, 'tree/home.html', {})


#view function for the create webpage
def create(request):

    if not request.user.is_authenticated:
        return redirect('/tree/login')
    
    #once the create tree button is clicked, then validate the info and create the tree
    if request.method == "POST":
        form = CreateNewTree(request.POST)

        if form.is_valid():
            n = form.cleaned_data["scientific_name"]
            street = form.cleaned_data['street']
            neigh = form.cleaned_data["neighborhood"]
            alive = form.cleaned_data["alive"]
            radius = form.cleaned_data['radius']
            rad_year = form.cleaned_data['rad_year']
            rad_month = form.cleaned_data['rad_month']
            biomass = form.cleaned_data['biomass']
            desc = form.cleaned_data['desc']


            valid_n = check_neigborhood(neigh)
            valid_s = check_street(street)
            if valid_n != -1 and valid_s != -1:
                st_from_db = Street.objects.get(address=street)
                tr_type=TreeType.objects.get(tree_type=n)
                t = Tree(type=tr_type, street=st_from_db, alive=alive)
                t.save()
                r = RadiusData(tree=t,radius=radius,year=rad_year, month=rad_month, biomass=biomass)
                r.save()
                st = stock(biomass)
                ab = absorb(st)
                prod = produce(st)
                calc = Calculation(tree=t, description=desc, year=rad_year, biomass=biomass, carbon_absorbed=ab, carbon_stocked=st, carbon_produced=prod)
                calc.save()
                result = Result(tree=t, tree_name=n, description=desc, year=rad_year, carbon_absorbed=ab, carbon_stocked=st, carbon_produced=prod)
                result.save()
                return render(request, 'tree/view.html', {'tree': t, 'avg': r, 'results': result})
            
            else:
                return HttpResponseRedirect('/tree/create')
           

           
    else:
        form = CreateNewTree()
        return render(request, 'tree/create.html', {'form': form})


#returns the carbon stocked amount
def stock(biomass):
    return round(decimal.Decimal(biomass) * decimal.Decimal(.47), 5)

#returns the carbon absorbed amount
def absorb(stock):
    return round(decimal.Decimal(stock) * decimal.Decimal(3.67), 5)

#returns the carbon produced amount
def produce(stock):
    return round(decimal.Decimal(stock) * decimal.Decimal(2.67), 5)


#checks that a street is a valid street within the neighborhood
def check_street(street):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * from street;")
        data = cursor.fetchall()
        arr = []
        for row in data:
            arr.append(row[2])
        if street not in arr:
            return -1
        else:
            cursor.execute("SELECT sid from street where address = %s;", [street])
            return cursor.fetchone()


#checks that a neighborhood is valid within the database
def check_neigborhood(n):
     with connection.cursor() as cursor:
        cursor.execute("SELECT * from neighborhood;")
        data = cursor.fetchall()
        arr = []
        for row in data:
            arr.append(row[1])
        if n not in arr:
            return -1
        else:
            cursor.execute("SELECT nid from neighborhood where neighborhood = %s;", [n])
            return cursor.fetchone()



#view function for registration page
def register(request):
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/tree/')
    else:
        form = UserCreationForm()
    return render(request, 'tree/register.html', {'form': form})


#view function for main view page of an individual tree
def view(request, tid):
    t = get_object_or_404(Tree, pk=tid)
    avg = RadiusData.objects.get(tree=t.tid)
    results = Result.objects.get(tree=t.tid)
    return render(request, 'tree/view.html', {'tree': t, 'avg': avg, 'results': results})


#view function for webpage of all tree scientific names
def collection(request):
    if not request.user.is_authenticated:
        return redirect('/tree/login')
    else:
        types = TreeType.objects.all()


        
        return render(request, 'tree/collection.html', {'types': types})
        

#view function for all trees of a given type in boston
def neighbor_view(request, ttid):
    trees = Tree.objects.filter(type=ttid)
    n_list=[]
    st_list=[]
    
    for tr in trees:
        st = Street.objects.get(sid=tr.street.sid)
        if st not in st_list:
            st_list.append(st)
        
    for st in st_list:
        ne = Neighborhood.objects.get(nid=st.neighborhood.nid)
        if ne not in n_list:
            n_list.append(ne)
        
    
    
    return render(request, 'tree/area.html',  {'n_list' : n_list, 'st_list' : st_list, 'trees': trees})


#view function for delete webpage
def delete_view(request, tid):
    tree = Tree.objects.get(tid=tid)
    if request.method == "POST":
        form = DeleteForm(request.POST)
        if form.is_valid():
            confirmation = form.cleaned_data["confirmation"]
            if confirmation == 'Confirm':
                with connection.cursor() as cursor:
                    cursor.execute("call updateResult(%s);", [tree.tid])
                tree.delete()
                
                return HttpResponseRedirect('/tree/collection')

    else: 

        form = DeleteForm()
        return render(request, 'tree/delete.html', {'tree': tree, 'form': form})