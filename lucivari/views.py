from django.shortcuts import render,redirect

from lucivari.models import Experiment, Conditions, Snv, Genes, Document, TemplateFile, content_file_generic
from lucivari.forms import DocumentForm, UserForm, UserProfileForm
#==============================================================================
# from lucivari.forms import CategoryForm, PageForm
# from lucivari.forms import UserForm, UserProfileForm
#==============================================================================
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from lucivari.webhose_search import run_query
from django.template import RequestContext
from registration.backends.simple.views import RegistrationView
from django.contrib.auth.models import User
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from lib.lucifanalysis import lucifanalysis_report
from lib.plate_consol import lucif_plate_merge, lucif_conso_plate
from zipfile import ZipFile
import glob
import mimetypes

#from django.http import HttpResponse



  # A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

# Updated the function definition

def search(request):
    condition_list = Conditions.objects.all()
    condition_filter = ConditionsFilter(request.GET, queryset=condition_list)
    
    return render(request, 'search/condition_list.html', {'filter': condition_filter})
    
    
def index(request):
    
    # Query the database for a list of ALL categories currently stored.
    
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary
    # that will be passed to the template engine.
   
    experiment_list = {}
    experiments = Experiment.objects.all()[:5]
    for exp in experiments:
        experiment_list[exp] = exp.date
        
    dateset = []
    TFset = []
    condition_id_set = []
   
    
    for i in experiment_list:
        dateset.append(i.date)
        TFset.append(i.gene_symbol)
        condition_id_set.append(i.condition_id)
        
       # cell_line_set.append(i.gene_symbol)
    print mimetypes.guess_type('map.svg')
    
    context_dict = {'dates': list(set(dateset)), 'tf_set': list(set(TFset)), 'condition_id_set': list(set(condition_id_set)) }
    print context_dict
    

    response = render(request, 'lucivari/index.html', context=context_dict)
    
    return response



    
    
    
def get_experiment_list():
    date_list = []
    for i in Experiments.objects.all():
        if i.date in date_list:
            pass
        else:
            date_list.append(i.date)
        
    
    return date_list


def about(request):
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()
    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    print(request.user)
    context_dict = {}
    
    
    
    return render(request, 'lucivari/about.html', context=context_dict)
@login_required
def data_transform(request):
    
    print(request.method)
    
    print(request.user)
    context_dict={}
    
    return render(request, 'lucivari/data_transform.html', context=context_dict)

#==============================================================================
# def simple_upload(request):
#     if request.method == 'POST' and request.FILES['myfile']:
#         myfile = request.FILES['myfile']
#         fs = FileSystemStorage()
#         filename = fs.save(myfile.name, myfile)
#         uploaded_file_url = fs.url(filename)
#         return render(request, 'core/simple_upload.html', {
#                 'uploaded_file_url': uploaded_file_url
#                 })
#     return render(request, 'core/simple_upload.html')
# 
#==============================================================================

@login_required
def model_form_upload(request):
    template = TemplateFile.objects.get(description ="Template_Lucif_Assay")
    #request.session['upload_file'] = "lucif_raw_file.txt" 
    request.session['template_file'] = template.description
    
    documents = Document.objects.all()
    try:
        for document in documents:
            print document.pk
            document.delete()
    except TypeError:
        pass
    
    mediafiles = glob.glob(os.path.join(settings.MEDIA_ROOT,'documents/*'))
    for i in mediafiles:
        os.remove(i)
    
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            for filename, file in request.FILES.iteritems():
                name = request.FILES[filename].name
                request.session['upload_file'] = os.path.join('documents',name)
            return redirect(report_gen)
    else:
        form = DocumentForm()
        context_dict = {'form':form }
        return render(request, 'lucivari/model_form_upload.html', context=context_dict)
    
    
    #request.session['upload_file'] = "lucif_raw_file.txt" 

@login_required
def report_gen(request):
    genericfilename = content_file_generic.objects.get(description = "Lucif_Assay_Report")
    rename = os.path.join(settings.MEDIA_ROOT,'documents',str(genericfilename.generic))
    
    documents = Document.objects.filter(document=request.session['upload_file'])


    for document in documents:
        
        filename = os.path.join(settings.MEDIA_ROOT,str(document.document))
        os.rename(filename, rename)
        document.original_file_name = request.session['upload_file']
        document.document = rename
        document.save()
    
    print(request.user)
    context_dict = {}
    
    return render(request, 'lucivari/report_gen.html', context=context_dict)   

@login_required
def consol_upload(request):
    template = TemplateFile.objects.get(description ="Template_Multi-Read_Raw")
    request.session['template_file'] = template.description
    

    documents = Document.objects.all()
    
    try:
        for document in documents:
            print document.original_file_name
            document.delete()
    except TypeError:
        pass
    
    mediafiles = glob.glob(os.path.join(settings.MEDIA_ROOT,'documents/*'))
    for i in mediafiles:
        os.remove(i)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            for filename, file in request.FILES.iteritems():
                name = request.FILES[filename].name
                request.session['upload_file'] = os.path.join('documents',name)

            return redirect(consol_upload_part2)
    else:
        form = DocumentForm()
        context_dict = {'form':form }
        return render(request, 'lucivari/consol_upload.html', context=context_dict)
    
@login_required  
def consol_upload_part2(request):
    genericfilename = content_file_generic.objects.get(description = "Consol_FF")
    rename = os.path.join(settings.MEDIA_ROOT,'documents',str(genericfilename.generic))
    
    documents = Document.objects.filter(document=request.session['upload_file'])
    for document in documents:
        print document.document
        filename = os.path.join(settings.MEDIA_ROOT,str(document.document))
        os.rename(filename, rename)
        document.original_file_name = request.session['upload_file']
        document.document = rename
        document.save()
        
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            for filename, file in request.FILES.iteritems():
                name = request.FILES[filename].name
                request.session['upload_file'] = os.path.join('documents',name)
            return redirect(consol_gen)
    else:
        form = DocumentForm()
        context_dict = {'form':form }
        return render(request, 'lucivari/consol_upload_part2.html', context=context_dict)
  

@login_required
def consol_gen(request):
    genericfilename = content_file_generic.objects.get(description = "Consol_RN")
    rename = os.path.join(settings.MEDIA_ROOT,'documents',str(genericfilename.generic))
    
    documents = Document.objects.filter(document=request.session['upload_file'])
    for document in documents:
        filename = os.path.join(settings.MEDIA_ROOT,str(document.document))
        os.rename(filename, rename)
        document.original_file_name = request.session['upload_file']
        document.document = rename
        document.save()
    
    print(request.user)
    context_dict = {}
    
    return render(request, 'lucivari/consol_gen.html', context=context_dict) 
     
@login_required
def consol_download(request):
    ff_filter = content_file_generic.objects.get(description = "Consol_FF")
    generic_ff = os.path.join(settings.MEDIA_ROOT,'documents',str(ff_filter.generic))
    rn_filter = content_file_generic.objects.get(description = "Consol_RN")
    generic_rn = os.path.join(settings.MEDIA_ROOT,'documents',str(rn_filter.generic))
    

    documents  = Document.objects.filter(document=generic_ff )
    #print documents
    for document in documents:
        doc = document.document
        original = document.original_file_name
        
    
        tempfile = os.path.join(settings.MEDIA_ROOT, original)
        tempfilename = tempfile.replace(".txt","_consol.txt")
        rawtemp = doc.readlines()
        ffplate = lucif_conso_plate(rawtemp)
    
    #print tempfilename
    
    documents  = Document.objects.filter(document=generic_rn )
    for document in documents:
        doc = document.document
        rawtemp = doc.readlines()
        rnplate = lucif_conso_plate(rawtemp)
    
    lucif_plate_merge(ffplate,rnplate, tempfilename)
   
    filename = tempfilename.split("/")[-1]
    fsock = open(tempfilename, 'r')
    
    response = HttpResponse(fsock, content_type='text/plain')
    response["Content-Disposition"] = 'attachment; filename= %s' % filename
    fsock.close()
    
    return response

@login_required
def static_file_download(request):
    print request
    basepath = os.path.join(settings.STATIC_DIR,'docs')
    template = TemplateFile.objects.get(description = request.session['template_file'])
    filepath = os.path.join(basepath,template.filename)
    
    
    fsock = open(filepath, 'r')
    response = HttpResponse(fsock, content_type='text/plain')
    response["Content-Disposition"] = 'attachment; filename= %s' % template.filename
    fsock.close()
    
    
    return response

@login_required
def report_download(request):
    file_filter = content_file_generic.objects.get(description = "Lucif_Assay_Report")
    generic_filter = os.path.join(settings.MEDIA_ROOT,'documents',str(file_filter.generic))
    
    documents  = Document.objects.get(document=generic_filter )
    doc = documents.document
    original = documents.original_file_name
    tempfile = os.path.join(settings.MEDIA_ROOT,original)
    tempfilename = tempfile.replace(".txt","_report.txt")
    
    rawtemp = doc.readlines()
    lucifanalysis_report(rawtemp,False, tempfilename)
    
    filename = tempfilename.split("/")[-1]
    fsock = open(tempfilename, 'r')
    
    response = HttpResponse(fsock, content_type='text/plain')
    response["Content-Disposition"] = 'attachment; filename= %s' % filename
    fsock.close()
    
    return response

@login_required
def zip_download(request):
    file_filter = content_file_generic.objects.get(description = "Lucif_Assay_Report")
    generic_filter = os.path.join(settings.MEDIA_ROOT,'documents',str(file_filter.generic))
    
    documents  = Document.objects.get(document=generic_filter)
    
    doc = documents.document
    original = documents.original_file_name
    tempfile = os.path.join(settings.MEDIA_ROOT,original)
    tempfilename = tempfile.replace(".txt","_report.txt")
    pdffilename = tempfilename.replace(".txt",".pdf")
    zip_path = tempfilename.replace(".txt",".zip")
    
    zip_filename = zip_path.split("/")[-1]
    
    rawtemp = doc.readlines()
    lucifanalysis_report(rawtemp,True, tempfilename)
    
    
    with ZipFile(zip_path,'w') as zip:
        zip.write(tempfilename,os.path.basename(tempfilename))
        zip.write(pdffilename,os.path.basename(pdffilename))
    
    downfilename = zip_filename.split("/")[-1]
    
    fsock = open(zip_path, 'r')
    
    response = HttpResponse(fsock, content_type='application/zip')
    response["Content-Disposition"] = 'attachment; filename= %s' % downfilename
    fsock.close()
    
    return response


def register(request):
    # A boolean value for telling the template 
    # whether the registration was successful.
    # Set to False initially. Code changes value to 
    # True when registration succeeds.
    registered = False
    
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.	
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        
        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()
            
            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()
            
            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, 
            # we set commit=False. This delays saving the model
# until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
            
            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and 
            #put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            # Now we save the UserProfile model instance.
            profile.save()
            
            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    # Render the template depending on the context.
    return render(request,
                  'lucivari/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form, 
                   'registered': registered})


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Lucivari account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
        
    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'lucivari/login.html', {})    
    
    
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('index'))



    
#==============================================================================
# def show_category(request,category_name_slug):
#     # Create a context dictionary which we can pass 
#     # to the template rendering engine.
#     context_dict = {}
#     application/pdf
#     try:
#         # Can we find a category name slug with the given name?
#         # If we can't, the .get() method raises a DoesNotExist exception.
#         # So the .get() method returns one model instance or raises an exception.
#         category = Category.objects.get(slug=category_name_slug)
#         
#         # Retrieve all of the associated pages.
#         # Note that filter() will return a list of page objects or an empty list
#         pages = Page.objects.filter(category=category).order_by('-views')
#         
#         # Adds our results list to the template context under name pages.
#         context_dict['pages'] = pages
#         # We also add the category object from 
#         # the database to the context dictionary.
#         # We'll use this in the template to verify that the category exists.
#         context_dict['category'] = category
#     except Category.DoesNotExist:
#         # We get here if we didn't find the specified category.
#         # Don't do anything - 
#         # the template will display the "no category" message for us.
#         context_dict['category'] = None
#         context_dict['pages'] = None
#     
#     
#     context_dict['query'] = category.name
#         
#     result_list = []
#     
#     if request.method == 'POST':
#         query = request.POST['query'].strip()
#         if query:
#             result_list= run_query(query)
#             context_dict['result_list'] = result_list
#             context_dict['query'] = request.POST['query']
#             
#    
#     
#     
#     # Go render the response and return it to the client.
#     return render(request, 'lucivari/category.html', context_dict)
# 
# @login_required
# def add_category(request):
#     form = CategoryForm()
#     
#     # A HTTP POST?
#     if request.method == 'POST':
#         form = CategoryForm(request.POST)
#         
#         # Have we been provided with a valid form?
#         if form.is_valid():
#             # Save the new category to the database.
#             form.save(commit=True)
#             # Now that the category is saved
#             # We could give a confirmation message
#             # But since the most recent category added is on the index page
#             # Then we can direct the user back to the index page.
#             return index(request)
#         
#         else:
#             # The supplied form contained errors -
#             # just print them to the terminal.
#             print(form.errors)
#     
#     # Will handle the bad form, new form, or no form supplied cases.
#     # Render the form with error messages (if any).
#     return render(request, 'lucivari/add_category.html', {'form': form})
# 
# @login_required
# def add_page(request, category_name_slug):
#     try:
#         category = Category.objects.get(slug=category_name_slug)
#     except Category.DoesNotExist:
#         category = None
#     
#     form = PageForm()
#     if request.method == 'POST':
#         form = PageForm(request.POST)
#         if form.is_valid():
#             if category:
#                 page = form.save(commit=False)
#                 page.category = category
#                 page.views = 0
#                 
#                 page.save()
#             return show_category(request, category_name_slug)
#         else:
#             print(form.errors)
#     
#     context_dict = {'form':form, 'category': category}
#     return render(request, 'lucivari/add_page.html', context_dict)
# 
# 
# 
# @login_required
# def restricted(request):
#     return render(request, 'lucivari/restricted.html')
# 
# 
# 
# 
# def track_url(request):
#     context = RequestContext(request)
#     page_id = None
#     url = '/lucivari/'
#     
#     if request.method == 'GET':
#         if 'page_id' in request.GET:
#             page_id = request.GET['page_id']
#             try:
#                 page = Page.objects.get(id=page_id)
#                 page.views = page.views +1
#                 page.save()
#                 url = page.url
#             except:
#                 pass
#             
#     
#         else:
#             url = reverse('index')
# 
#         
#     return redirect(url)
# 
@login_required
def register_profile(request):
    form = UserProfileForm()
 
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
 
            return redirect('index')
        else:
            print(form.errors)
 
    context_dict = {'form':form}
 
    return render(request, 'lucivari/profile_registration.html', context_dict)
 
#==============================================================================
#  
# @login_required
# def profile(request, username):
#     try:
#         user = User.objects.get(username=username)
#     except User.DoesNotExist:
#         return redirect('index')
#  
#     userprofile = UserProfile.objects.get_or_create(user=user)[0]
#     form = UserProfileForm(
#             {'website': userprofile.website, 'picture': userprofile.picture})
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
#         if form.is_valid():
#             form.save(commit=True)
#             return redirect('profile', user.username)
#         else:
#             print(form.errors)
#  
#     return render(request, 'lucivari/profile.html',
#                   {'userprofile': userprofile, 'selecteduser': user, 'form': form})
#  
# @login_required
# def list_profiles(request):
#     userprofile_list = UserProfile.objects.all()
#  
#     return render(request, 'lucivari/list_profiles.html',
#                   {'userprofile_list' : userprofile_list})
# #     
#==============================================================================
# 
# @login_required
# def like_category(request):
# 
#     cat_id = None
#     if request.method == 'GET':
#         cat_id = request.GET['category_id']
# 
#     likes = 0
#     if cat_id:
#         cat = Category.objects.get(id=int(cat_id))
#         if cat:
#             likes = cat.likes + 1
#             cat.likes =  likes
#             cat.save()
# 
#     return HttpResponse(likes)
# 
# def get_category_list(max_results=0, starts_with=''):
#     cat_list = []
#     if starts_with:
#         cat_list = Category.objects.filter(name__istartswith=starts_with)
#     
#     if max_results > 0:
#         if len(cat_list) > max_results:
#             cat_list = cat_list[:max_results]
#     return cat_list
# 
# def suggest_category(request):
#     cat_list = []
#     starts_with = ''
#     
#     if request.method == 'GET':
#         starts_with = request.GET['suggestion']
#     cat_list = get_category_list(8, starts_with)
#     
#     return render(request, 'lucivari/cats.html', {'cats': cat_list })
# 
# @login_required
# def auto_add_page(request):
#     cat_id = None
#     url = None
#     title = None
#     context_dict = {}
#     if request.method == 'GET':
#         cat_id = request.GET['category_id']
  #         url = request.GET['url']
#         title = request.GET['title']
#         if cat_id:
#             category = Category.objects.get(id=int(cat_id))
#             p = Page.objects.get_or_create(category=category, 
#                 title=title, url=url)
#             pages = Page.objects.filter(category=category).order_by('-views')
#             # Adds our results list to the template context under name pages.
#             context_dict['pages'] = pages
#     return render(request, 'lucivari/page_list.html', context_dict)
# 
# def add_cat(name, views, likes):
#     c = Category.objects.get_or_create(name=name)[0]
#     c.views = views
#     c.likes = likes
#     c.save()
#     return c
#==============================================================================

