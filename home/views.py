from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json
from django.core import serializers
import uuid
import random
import string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .forms import OrganizationForm, AppForm, ListForm, ListFieldFormset
from django.views.decorators.csrf import csrf_exempt
import subprocess
from itertools import chain
from tempfile import NamedTemporaryFile
from subprocess import call
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

N = 16
def randomstr(N: int=16):
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k = N))

def get_domain(request):
    return request.scheme + '://' + request.get_host()

#===============================================================================
# Static Pages / Home Page Setup
#===============================================================================

def home(request):
    # Placeholder for now
    context = {}
    return render(request, 'home/home.html', context=context)

def terms(request):
    # Placeholder for now
    context = {}
    return render(request, 'home/terms.html', context=context)

def privacy(request):
    # Placeholder for now
    context = {}
    return render(request, 'home/privacy.html', context=context)

def about(request):
    # Placeholder for now
    context = {}
    return render(request, 'home/about.html', context=context)

def is_unauthorized(request, organization, app):
    org_obj = OrganizationUser.objects.filter(organization=organization, user=request.user, status__exact='active')
    if not org_obj.exists():
        return True
    elif app not in org_obj[0].permitted_apps.all():
        if org_obj[0].role != 'admin':
            return True
#===============================================================================
# Organizations
#===============================================================================


@login_required
def organizations(request):

    userOrganizations = OrganizationUser.objects.filter(user=request.user, status__exact='active', organization__status__exact="active").order_by('organization__name',)
    organizations = []

    for userOrganization in userOrganizations:
        organizations.append(userOrganization.organization)

    context = {
        'organizations': organizations
    }

    return render(request, 'home/organizations.html', context=context)



@login_required
def add_organization(request):

    # Uses standard django forms

    if request.method == "POST":
        form = OrganizationForm(request.POST)
        if form.is_valid():
            organization = form.save(commit=False)
            organization.created_at = timezone.now()
            organization.id = randomstr()
            organization.save()
            u = User.objects.get(username = request.user.username)
            organization.active_users.add(u)
            org_user = OrganizationUser.objects.get(organization=organization,user = request.user)
            org_user.role = "admin"
            org_user.save()
            organization.save()
            return redirect('apps', organization_pk=organization.pk)

    else:

        form = OrganizationForm()

        return render(request, 'home/organization-form.html', {'form': form})




@login_required
def edit_organization(request, organization_pk):

    # Uses standard django forms

    organization = get_object_or_404(Organization, pk=organization_pk)

    if request.method == "POST":
        form = OrganizationForm(request.POST, instance=organization)
        if form.is_valid():
            organization = form.save(commit=False)
            organization.save()
            return redirect('organizations')
    else:
        form = OrganizationForm(instance=organization)

        context = {
            'organization': organization,
            'form': form
        }

        return render(request, 'home/organization-form.html', {'form': form})



@login_required
def archive_organization(request, organization_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)

    organization.status = "archived"
    organization.save()

    return redirect('organizations')



@csrf_exempt
@login_required
def organization_settings(request, organization_pk):

    # Uses standard django forms

    organization = get_object_or_404(Organization, pk=organization_pk)
    if request.method == "POST":
        if not OrganizationUser.objects.filter(organization=organization, user=request.user,role='admin').exists():
            return HttpResponse('You are not allowed here!', status=401)
    #    print(request.POST)
        if request.POST['type'] == "add_user":
            if User.objects.filter(email=request.POST['email']):
                u = User.objects.get(email=request.POST['email'])
                organization.active_users.add(u)
                org_user = OrganizationUser.objects.get(user=u,organization=organization)
                org_user.status='active'
                org_user.save()
                subject = "You have been added to " + organization.name +" on OneTable"
                html_message = render_to_string('home/mail_template.html', {
                    'type': 'added_registered_user_to_org',
                    'added_person' : request.user,
                    'org_added' : organization,
                    "domain" : get_domain(request)
                    })
                plain_message = strip_tags(html_message)
                from_email = None
                to = [request.POST['email']]
                print('Subject :' + subject )
                print(html_message)
                try:
                    mail.send_mail(subject=subject, message=plain_message, from_email=from_email, recipient_list=to,html_message=html_message,fail_silently=True)
                except:
                    print('Unable to send E-mail')
                organization.save()
            else:
                u = InactiveUsers.objects.get_or_create(user_email=request.POST['email'])
                u[0].save()
                organization.inactive_users.add(u[0])
                organization.save()
                subject = "You have been added to " + organization.name + " on OneTable"
                html_message = render_to_string('home/mail_template.html', {
                    'type': "added_unregistered_user_to_org",
                    'added_person' : request.user,
                    'org_added' : organization,
                    "domain" : get_domain(request)
                    })
                plain_message = strip_tags(html_message)
                from_email = None
                to = [request.POST['email']]
                print('Subject :' + subject )
                print(html_message)
                try:
                    mail.send_mail(subject=subject, message=plain_message, from_email=from_email, recipient_list=to,html_message=html_message,fail_silently=True)
                except:
                    print('Unable to send E-mail')
                organization.save()


            return JsonResponse({
                "added" : "true"
            })

        elif request.POST['type'] == "remove_user":
            if request.POST['user_type'] == "active":
                org_user = OrganizationUser.objects.get(user__email=request.POST['email'],organization_id=organization.pk)
                org_user.status = "deleted"
                org_user.save()
            else:
                u = InactiveUsers.objects.get(user_email=request.POST['email'])
                organization.inactive_users.remove(u)
                organization.save()
            return JsonResponse({
                "removed" : "true"
            })

        elif request.POST['type'] == 'change_role':
            org_user = OrganizationUser.objects.get(organization=organization,user__email=request.POST['email'])
            print(org_user)
            org_user.role = request.POST['to']
            print(request.POST['to'])
            if request.POST['to'] == 'admin':
                subject = "You have been made an Admin for "+ organization.name +" on OneTable"
                html_message = render_to_string('home/mail_template.html', {
                    'type': 'registered_user_made_admin_of_org',
                    'added_person' : request.user,
                    'org' : organization,
                    "domain" : get_domain(request)
                    })
                plain_message = strip_tags(html_message)
                from_email = None
                to = [request.POST['email']]
                print('Subject :' + subject )
                print(html_message)
                try:
                    mail.send_mail(subject=subject, message=plain_message, from_email=from_email, recipient_list=to,html_message=html_message,fail_silently=True)
                except:
                    print('Unable to send E-mail')
            org_user.save()

            return JsonResponse({
                "changed_to" : org_user.role
            })

    else:
        form = OrganizationForm(instance=organization)
        active_users = organization.organizationuser_set.filter(status="active").order_by('-created_at')
        inactive_users = organization.inactive_users.all().order_by('-created_at')
        connection = chain(active_users,inactive_users)
        is_admin = OrganizationUser.objects.filter(organization=organization,user=request.user,role='admin').exists
        print(connection)
        context = {
            'organization': organization,
            'form': form,
            "connection":connection,
            "is_admin" : is_admin
     }

        return render(request, 'home/organization-settings.html', context=context)



#===============================================================================
# Apps (Workspaces)
#===============================================================================

@login_required
def apps(request, organization_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    user_obj = OrganizationUser.objects.filter(user=request.user, status__exact='active', organization = organization).exists()
    if not user_obj:
         return HttpResponse('You are not allowed here!', status=401)

    user_obj = OrganizationUser.objects.get(user=request.user, status__exact='active', organization = organization)
    if not user_obj.role == "admin":
        userApps = user_obj.permitted_apps.filter(status='active')
    else:
        userApps =App.objects.filter(organization=organization,status='active')

    apps = []

    for userApp in userApps:
        apps.append(userApp)

    is_admin_of_parent_org = OrganizationUser.objects.filter(user=request.user,organization=organization,role='admin').exists()
    context = {
        'organization': organization,
        'apps': apps,
        'is_admin_of_parent_org' : is_admin_of_parent_org
    }

    return render(request, 'home/apps.html', context=context)




@login_required
def add_app(request, organization_pk):

    # Uses standard django forms

    organization = get_object_or_404(Organization, pk=organization_pk)
    if not OrganizationUser.objects.filter(organization=organization,role='admin',user=request.user):
        return HttpResponse('You are not allowed here!', status=401)

    if request.method == "POST" and OrganizationUser.objects.filter(organization=organization,role='admin',user=request.user):
        form = AppForm(request.POST)
        if form.is_valid():

            # Save the new project
            app = form.save(commit=False)
            app.organization = organization
            app.created_user = request.user
            app.created_at = timezone.now()
            app.id = randomstr()
            app.save()

            # Save the new user <> project relation
            appUser = AppUser()
            appUser.user = request.user
            appUser.app = app
            appUser.status = "active"
            appUser.role = "admin"
            appUser.save()

            return redirect('app_details', organization_pk=organization_pk, app_pk=app.pk)

    else:

        form = AppForm()
        context = {
            'form': form,
            'organization': organization
        }

        return render(request, 'home/app-form.html', {'form': form})

@login_required
def edit_app(request, organization_pk, app_pk):

    # Uses standard django forms

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    org_obj = OrganizationUser.objects.filter(organization=organization,user=request.user, status__exact='active')
    if not org_obj.exists():
        return HttpResponse('You are not allowed here!', status=401)
    elif app not in org_obj[0].permitted_apps.all():
        if org_obj[0].role != 'admin':
            return HttpResponse('You are not allowed here!', status=401)
    if request.method == "POST":
        form = AppForm(request.POST, instance=app)
        if form.is_valid():
            app = form.save(commit=False)
            app.save()
            return redirect('apps', organization_pk=organization_pk)
    else:
        form = AppForm(instance=app)

        context = {
            'organization': organization,
            'app': app,
            'form': form
        }

        return render(request, 'home/app-form.html', {'form': form})

@login_required
def archive_app(request, organization_pk, app_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    org_obj = OrganizationUser.objects.filter(organization=organization,user=request.user, status__exact='active')
    if not org_obj.exists():
        return HttpResponse('You are not allowed here!', status=401)
    elif app not in org_obj[0].permitted_apps.all():
        if org_obj[0].role != 'admin':
            return HttpResponse('You are not allowed here!', status=401)
    app.status = "archived"
    app.save()

    return redirect('apps', organization_pk=organization_pk)

@login_required
@csrf_exempt
def app_settings(request, organization_pk, app_pk):
    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    org_obj = OrganizationUser.objects.filter(organization=organization,user=request.user, status__exact='active')
    if not org_obj.exists():
        return HttpResponse('You are not allowed here!', status=401)
    elif app not in org_obj[0].permitted_apps.all():
        if org_obj[0].role != 'admin':
            return HttpResponse('You are not allowed here!', status=401)
    # Uses standard django forms
    if request.method == "POST":
        print(request.POST)
        #print(request.POST)
        if request.POST['type'] == "add_user":
            print('if')
            if User.objects.filter(email=request.POST["email"]):
                u = User.objects.get(email=request.POST['email'])
                print(u)
                organization.active_users.add(u)
                organization.save()
                org_user = OrganizationUser.objects.get(organization=organization,user=u)
                org_user.permitted_apps.add(app)
                org_user.status='active'
                org_user.save()
                #print(org_user.permitted_apps.objects.all())
                app.save()
                subject = "You have been added to " + app.name + " on OneTable"
                html_message = render_to_string('home/mail_template.html', {
                    'type': "added_registered_user_to_workspace",
                    'added_person' : request.user,
                    'app' : app,
                    "domain" : get_domain(request)
                    })
                plain_message = strip_tags(html_message)
                from_email = None
                to = [request.POST['email']]
                print('Subject :' + subject )
                print(html_message)
                try:
                    mail.send_mail(subject=subject, message=plain_message, from_email=from_email, recipient_list=to,html_message=html_message,fail_silently=True)
                except:
                    print('Unable to send E-mail')

            else:
                u = InactiveUsers.objects.get_or_create(user_email=request.POST['email'])
                u[0].attached_workspaces.add(app)
                organization.inactive_users.add(u[0])
                u[0].save()
                organization.save()
                subject = "You have been added to " + app.name + " on OneTable"
                html_message = render_to_string('home/mail_template.html', {
                    'type': "added_unregistered_user_to_workspace",
                    'added_person' : request.user,
                    'app' : app,
                    "domain" : get_domain(request)
                    })
                plain_message = strip_tags(html_message)
                from_email = None
                to = [request.POST['email']]
                print('Subject :' + subject )
                print(html_message)
                try:
                    mail.send_mail(subject=subject, message=plain_message, from_email=from_email, recipient_list=to,html_message=html_message,fail_silently=True)
                except:
                    print('Unable to send E-mail')

            return JsonResponse({
                "added" : "true"
            })

        elif request.POST['type'] == "remove_user":
            print('elif')
            if request.POST['user_type'] == "active":
                org_user = OrganizationUser.objects.get(user__email=request.POST['email'],organization_id=organization.pk)
                print(org_user)
                org_user.permitted_apps.remove(app)
                org_user.save()
            else:
                u = InactiveUsers.objects.get(user_email=request.POST['email'])
                u.attached_workspaces.remove(app)
                u.save()

            return JsonResponse({
                "removed" : "true"
            })

        elif request.POST['type'] == 'change_role':
            org_user = OrganizationUser.objects.get(organization=organization,user__email=request.POST['email'])
            print(org_user)
            org_user.role = request.POST['to']
            org_user.save()

            return JsonResponse({
                "changed_to" : org_user.role
            })

    else:
        form = AppForm(instance=app)
        active_users = OrganizationUser.objects.filter(organization_id=organization,permitted_apps=app, status='active').exclude(role='admin')
        admin = OrganizationUser.objects.filter(organization_id=organization.pk,role='admin')
        organization_inactive = [inactive.user_email for inactive in organization.inactive_users.all()]
        inactive_users = InactiveUsers.objects.filter(attached_workspaces=app, user_email__in=organization_inactive)
        connection = chain(admin,active_users,inactive_users)
        is_admin = OrganizationUser.objects.filter(organization=organization,user=request.user,role='admin').exists
        #print(connection)
        context = {
        'organization': organization,
        'app': app,
        'form': form,
        "connection":connection,
        "is_admin" : is_admin
        }

    return render(request, 'home/app-settings.html', context=context)

@login_required
def app_details(request, organization_pk, app_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    org_obj = OrganizationUser.objects.filter(organization=organization,user=request.user, status__exact='active')
    activities = Activity.objects.filter(app=app).order_by('-created_at')
    if not org_obj.exists():
        return HttpResponse('You are not allowed here!', status=401)
    elif app not in org_obj[0].permitted_apps.all():
        if org_obj[0].role != 'admin':
            return HttpResponse('You are not allowed here!', status=401)
    context = {
        'organization': organization,
        'app': app,
        'type': 'activity',
        'activities' : activities
    }
    return render(request, 'home/workspace.html', context=context)


#===============================================================================
# Workspace Pages
#===============================================================================

@login_required
def activity(request, organization_pk, app_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    org_obj = OrganizationUser.objects.filter(organization=organization,user=request.user, status__exact='active')
    activities = Activity.objects.filter(app=app).order_by('-created_at')
    if not org_obj.exists():
        return HttpResponse('You are not allowed here!', status=401)
    elif app not in org_obj[0].permitted_apps.all():
        if org_obj[0].role != 'admin':
            return HttpResponse('You are not allowed here!', status=401)
    if request.is_ajax() and request.method == "GET":

        # Call is ajax, just load main content needed here

        html = render_to_string(
            template_name="home/activity.html",
            context={
                'organization': organization,
                'app': app,
                "activities" : activities
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:

        context = {
            'organization': organization,
            'app': app,
            'type': 'activity',
            "activities" : activities
        }

        return render(request, 'home/workspace.html', context=context)


#===============================================================================
# Lists
#===============================================================================

@login_required
def lists(request, organization_pk, app_pk):
    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    org_obj = OrganizationUser.objects.filter(organization=organization,user=request.user, status__exact='active')
    if not org_obj.exists():
        return HttpResponse('You are not allowed here!', status=401)
    elif app not in org_obj[0].permitted_apps.all():
        if org_obj[0].role != 'admin':
            return HttpResponse('You are not allowed here!', status=401)


    # lists = List.objects.all().filter(status='active', app=app)
    lists = List.objects.filter(status='active', app=app).order_by('name',)

    if request.is_ajax() and request.method == "GET":
        # Call is ajax, just load main content needed here

        html = render_to_string(
            template_name="home/lists.html",
            context={
                'organization': organization,
                'app': app,
                'lists': lists
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:
        # If accessing the url directly, load full page

        context = {
            'organization': organization,
            'app': app,
            'lists': lists,
            'type': 'lists'
        }

        return render(request, 'home/workspace.html', context=context)

@csrf_exempt
@login_required
def list(request, organization_pk, app_pk, list_pk):
    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)
    search = request.GET.get('search', None)

    if search != None:
        fields = RecordField.objects.filter(value__icontains=search, record__list=list)
        list_of_records=fields.values_list('record_id',flat=True)
        records=Record.objects.filter(pk__in=list_of_records)
    else:
        records = Record.objects.filter(status='active', list=list)

    per_page = request.GET.get('per_page', None)
    search = request.GET.get('search', None)

    if per_page != None:
        paginator = Paginator(records,per_page)
    else:
        paginator = Paginator(records, 10)

    page_number = request.GET.get('page', None)
    records_page = paginator.get_page(1)
    if page_number != '':
        records_page = paginator.get_page(page_number)
    else:
        records_page = paginator.get_page(1)

    if request.is_ajax() and request.method == "GET":
        search_value = request.GET.get('search_value')
        if search_value:
            record_fields = RecordField.objects.filter(record__list=list, value__icontains=search_value)
            record_ids = [i['record_id'] for i in record_fields.values('record_id')]
            records = Record.objects.filter(id__in=record_ids, status='active', list=list)
        # Call is ajax, just load main content needed here
        #paginator = Paginator(records, 10)


        html = render_to_string(
            template_name="home/list.html",
            context={
                'organization': organization,
                'app': app,
                'list': list,
                'records': records_page
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:
        # If accessing the url directly, load full page


        context = {
            'organization': organization,
            'app': app,
            'list': list,
            'records': records_page,
            'type': 'list'
        }

        return render(request, 'home/workspace.html', context=context)


@login_required
def create_list(request, organization_pk, app_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    if is_unauthorized(request, organization, app):
        return HttpResponse('You are not allowed here!', status=401)
    # Django formset stuff

    # Use model formset and not inline formset for more control over the data
    # being saved (i.e. setting and checking primary fields, etc.)

    if request.method == 'GET':
        listform = ListForm(request.GET or None)
        formset = ListFieldFormset(queryset=List.objects.none())
        # Reduce the queryset for select_list field to just active lists in current app
        for form in formset:
            form.fields['select_list'].queryset = List.objects.filter(app=app, status='active')

    elif request.method == 'POST':
        listform = ListForm(request.POST)
        formset = ListFieldFormset(request.POST)
        print(request.POST)
        # Verify the form submitted is valid
        if listform.is_valid() and formset.is_valid():
            list = listform.save(commit=False)
            list.app = app
            list.created_user = request.user
            list.created_at = timezone.now()
            list.id =randomstr()
            list.public_link = randomstr(N=30)
            list.save() # Save here then update primary field once field is saved
            # Loop through the list field forms submitted
            list_field_order = 0
            change_from_select_list = False
            for index, form in enumerate(formset):
                # Save the list field
                list_field = form.save(commit=False)
                list_field.field_id = randStr(N=10)
                list_field.list = list
                list_field.created_user = request.user
                list_field.created_at = timezone.now()
                list_field.order = list_field_order

                if index == 0:
                    list_field.primary = True
                    list_field.required = True
                    list_field.visible = True
                else:
                    list_field.primary = False

                list_field.save()
                list_field.field_id = list_field.id
                list_field.save()

                for select_list_id in request.POST.getlist(f'form-{index}-select_list'):
                    if form.cleaned_data.get('select_list') is not None:
                        if select_list_id != form.cleaned_data.get('select_list').id:
                            ListField.objects.create(
                                created_at=timezone.now(),
                                created_user=request.user,
                                list=list,
                                field_label=request.POST[f'form-{index}-field_label'],
                                field_type=request.POST[f'form-{index}-field_type'],
                                select_list_id=int(select_list_id),
                                order=list_field_order
                            )

                            list_field_order += 1
                            change_from_select_list = True

                if change_from_select_list is False:
                    list_field_order += 1

            return redirect('lists', organization_pk=organization_pk, app_pk=app_pk)
        else:
            print(formset.errors)

    context={
        'organization': organization,
        'app': app,
        'listform': listform,
        'formset': formset,
        'type': 'list-create'
    }

    # TODO eventually handle ajax calls vs. direct link call

    return render(request, 'home/workspace.html', context=context)

@login_required
def edit_list(request, organization_pk, app_pk, list_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)
    if is_unauthorized(request, organization, app):
        return HttpResponse('You are not allowed here!', status=401)
    # Django formset stuff

    # Use model formset and not inline formset for more control over the data
    # being saved (i.e. setting and checking primary fields, etc.)

    if request.method == 'GET':
        listform = ListForm(request.GET or None, instance=list)
        formset = ListFieldFormset(queryset=ListField.objects.filter(list=list, status='active').order_by('order'))
        # Reduce the queryset for select_list field to just active lists in current app
        for form in formset:
            form.fields['select_list'].queryset = List.objects.filter(app=app, status='active')

    elif request.method == 'POST':
        listform = ListForm(request.POST, instance=list)
        formset = ListFieldFormset(data=request.POST)
        print(request.POST)
        # Verify the form submitted is valid
        print('invalid')
        if listform.is_valid() and formset.is_valid():
            print('valid')
            list = listform.save(commit=False)
            list.updated_at = timezone.now()
            list.save() # Save here then update primary field once field is saved
            # Loop through the list field forms submitted
            list_field_order = 0
            for index, form in enumerate(formset):
                if int(index) != int(request.POST.get('form-INITIAL_FORMS')):
                # Save the list field
                    list_field = form.save()
                    list_field.list = list
                    list_field.updated_at = timezone.now()
                    list_field.created_user = request.user
                    list_field.order = list_field_order
                    if list_field.order == 0:
                        list_field.primary = True
                        list_field.required = True
                        list_field.visible = True
                    else:
                        list_field.primary = False
                    list_field.save()

                    list_field_order += 1

            remove_list_field_ids = request.POST.getlist('delete_list_field_ids')
            for list_field_id in remove_list_field_ids:
                try:
                    list_field_object = ListField.objects.get(id=int(list_field_id))
                    list_field_object.status = "deleted"
                    list_field_object.save()
                except: pass
            return redirect('lists', organization_pk=organization_pk, app_pk=app_pk)
        else:
            print(f'List Form Error\t\t\t\t{listform.errors}\nField Type Error\t\t\t\t{formset.errors}')

    context={
        'organization': organization,
        'app': app,
        'listform': listform,
        'formset': formset,
        'type': 'edit-list'
    }

    # TODO eventually handle ajax calls vs. direct link call

    return render(request, 'home/workspace.html', context=context)


@login_required
def archive_list(request, organization_pk, app_pk, list_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)
    if is_unauthorized(request, organization, app):
        return HttpResponse('You are not allowed here!', status=401)
    list.status = "archived"
    list.save()

    # Able to use a redirect here because we did a direct POST request
    return redirect('lists', organization_pk=organization_pk, app_pk=app_pk)

@login_required
def list_settings(request, organization_pk, app_pk, list_pk):

    # Does not / will not use the standard django forms per the comments noted
    # above

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)
    public_link = f'http://{request.get_host()}/forms/?ref={list.public_link}'
    if is_unauthorized(request, organization, app):
        return HttpResponse('You are not allowed here!', status=401)

    context = {
        'organization': organization,
        'app': app,
        'list': list,
        'public_link': public_link
    }

    return render(request, 'home/list-settings.html', context=context)


#===============================================================================
# Records
#===============================================================================
@login_required
def add_record(request, organization_pk, app_pk, list_pk):

    # Not the most 'django' way of doing this, may be ways to improve in the future
    # that better uses the django out of the box forms functionality

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)
    if is_unauthorized(request, organization, app):
        return HttpResponse('You are not allowed here!', status=401)
    fields = []
    for list_field in list.list_fields:
        field_object = {}
        field_object['field_id'] = list_field.field_id
        field_object['field_label'] = list_field.field_label
        field_object['field_type'] = list_field.field_type
        field_object['required'] = list_field.required
        field_object['primary'] = list_field.primary
        field_object['visible'] = list_field.visible
        field_object['order'] = list_field.order
        field_object['id'] = list_field.id
        if list_field.field_type == "choose-from-list":
            field_object['select_record'] = RecordField.objects.filter(record__list=list_field.select_list.id, record__status="active", status="active", list_field__primary=True).values_list('record', 'value')
        fields.append(field_object)
    fields.reverse()

    if request.is_ajax() and request.method == "GET":
        # Call is ajax, just load main content needed here

        html = render_to_string(
            template_name="home/record-create.html",
            context={
                'organization': organization,
                'app': app,
                'list': list,
                'fields': fields
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:
        # If accessing the url directly, load full page

        context = {
            'organization': organization,
            'app': app,
            'list': list,
            'fields': fields,
            'type': 'edit-record',
        }

        return render(request, 'home/workspace.html', context=context)


@login_required
@csrf_exempt
def save_record(request, organization_pk, app_pk, list_pk):

    # This handles both saving and updating a record

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)

    if is_unauthorized(request, organization, app):
        return HttpResponse('You are not allowed here!', status=401)

    record_id = request.POST.get('record_id', None)
    fields = json.loads(request.POST['field_values'])
    print(request.POST)

    # TODO
    # Needs error handling here verify if the form is valid (i.e. all required fields, acceptable data types, etc)

    record = None # Create object globally outside of the if/else

    if record_id is not None:
        # Get the existing record / this is a record being edited
        record = get_object_or_404(Record, pk=record_id)
    else:
        # Add a new record
        record = Record.objects.create(
            list=list,
            status='active',
            created_at=timezone.now(),
            created_user=request.user,
            id=randomstr())
        record.save()
    for field in fields:
            # if field['fieldValue']:
            # if field['fieldValue'] is not None:
                # Only save a RecordField object if there is a value

                if record_id is not None:
                    try:
                        # Update existing record field
                        # TODO only update if the value changed
                        record_field = RecordField.objects.get(status='active', list_field__field_id=field['fieldId'], record=record)
                        if field['fieldType'] == "choose-from-list":
                           record_field.selected_record_id = field['fieldValue']
                           record_field.value = field['selectListValue']
                        #    record_field.id = randomstr()
                        else:
                            record_field.value = field['fieldValue']
                            # record_field.id = randomstr()
                        record_field.save()

                        # Update existing relationship
                        if field['fieldType'] == "choose-from-list":
                            try:
                                record_relation = RecordRelation.objects.get(status='active', list_field__field_id=field['fieldId'], parent_record=record)
                                record_relation.child_record_id = field['fieldValue']
                                record_relation.save()
                            except RecordRelation.DoesNotExist:
                                # Create the record relation / does not exist
                                record_relation = RecordRelation.objects.create(
                                    parent_record=record,
                                    child_record_id=record_field.selected_record_id,
                                    relation_type='choose-from-list',
                                    list_field=record_field.list_field,
                                    status='active',
                                    created_at=timezone.now(),
                                    created_user=request.user,
                                    id=randomstr())
                                record_relation.save()

                    except RecordField.DoesNotExist:
                        # This record field has not been saved before, so create it
                        # TODO this is redundant with below / can be consolidated eventually
                        try:

                            list_field = ListField.objects.get(status='active', field_id=field['fieldId'], list=list)

                            # Create the new record field
                            record_field = RecordField.objects.create(
                                record=record,
                                list_field=list_field,
                                status='active',
                                created_at=timezone.now(),
                                created_user=request.user,
                                id=randomstr())
                            record_field.save()

                            if field['fieldType'] == "choose-from-list":
                                record_field.selected_record_id = field['fieldValue']
                                record_field.value = field['selectListValue']
                            else:
                                record_field.value = field['fieldValue']
                            record_field.save()

                            # Create the record relation if select from list
                            if field['fieldType'] == "choose-from-list":
                                record_relation = RecordRelation.objects.create(
                                    parent_record=record,
                                    child_record_id=record_field.selected_record_id,
                                    relation_type='choose-from-list',
                                    list_field=record_field.list_field,
                                    status='active',
                                    created_at=timezone.now(),
                                    created_user=request.user,
                                    id=randomstr())
                                record_relation.save()

                        except ListField.DoesNotExist:
                            # Easy error handling for now
                            pass

                else:
                    try:

                        # Create new record field

                        list_field = ListField.objects.get(status='active', field_id=field['fieldId'], list=list)

                        record_field = RecordField.objects.create(
                            record=record,
                            list_field=list_field,
                            status='active',
                            created_at=timezone.now(),
                            created_user=request.user,
                            id=randomstr())
                        record_field.save()

                        if field['fieldType'] == "choose-from-list":
                            record_field.selected_record_id = field['fieldValue']
                            record_field.value = field['selectListValue']
                        else:
                            record_field.value = field['fieldValue']
                        record_field.save()

                        # Create the record relation if select from list
                        if field['fieldType'] == "choose-from-list":
                            record_relation = RecordRelation.objects.create(
                                parent_record=record,
                                child_record_id=record_field.selected_record_id,
                                relation_type='choose-from-list',
                                list_field=record_field.list_field,
                                status='active',
                                created_at=timezone.now(),
                                created_user=request.user,
                                id=randomstr())
                            record_relation.save()

                    except ListField.DoesNotExist:
                        # Easy error handling for now
                        pass

    # Redirect based on ajax call from frontend on success

    data_dict = {"success": True}

    return JsonResponse(data=data_dict, safe=False)


@login_required
def record(request, organization_pk, app_pk, list_pk, record_pk):

    # Record details page (placeholder for now)
    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)
    record = get_object_or_404(Record, pk=record_pk)
    comments = RecordComment.objects.filter(record_id=record_pk).order_by('-pk')
    files = RecordFile.objects.filter(record_id=record_pk).order_by('-pk')
    # media = RecordMedia.objects.filter(record_id=record_pk).order_by('-pk')
    if is_unauthorized(request, organization, app):
        return HttpResponse('You are not allowed here!', status=401)

    if request.is_ajax() and request.method == "GET":

        # Call is ajax, just load main content needed here

        html = render_to_string(
            template_name="home/record.html",
            context={
                'organization': organization,
                'app': app,
                'list': list,
                'record': record,
                'record_view': 'record-details',
                'comments' : comments,
                'files':files,
                'user' : request.user

            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:

        context = {
            'organization': organization,
            'app': app,
            'list': list,
            'record': record,
            'type': 'record',
            'record_view': 'record-details',
            'comments' : comments,
            'files':files,
            'user' : request.user

        }

        return render(request, 'home/workspace.html', context=context)

@login_required
def record_details(request, organization_pk, app_pk, list_pk, record_pk):

    # Record details page (placeholder for now)

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)
    record = get_object_or_404(Record, pk=record_pk)
    comments = RecordComment.objects.filter(record_id=record_pk).order_by('-created_at')
    # media = RecordMedia.objects.filter(record_id=record_pk).order_by('-pk')
    files = RecordFile.objects.filter(record_id=record_pk).order_by('-pk')
    if is_unauthorized(request, organization, app):
        return HttpResponse('You are not allowed here!', status=401)

    if request.is_ajax() and request.method == "GET":

        # Call is ajax, just load main content needed here

        html = render_to_string(
            template_name="home/record-details.html",
            context={
                'organization': organization,
                'app': app,
                'list': list,
                'record': record,
                'type': 'record',
                'record_view': 'record-details',
                "comments":comments,
                "files": files,
                'user' : request.user

            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    # TODO add access here for direct link
    # For now just return record details
    if request.method == "GET":

        # If accessing the url directly, load full page

        context = {
            'organization': organization,
            'app': app,
            'list': list,
            'record': record,
            'type': 'record',
            'record_view': 'record-details',
            "comments":comments,
            "files": files,
            "user" : request.user

        }

        return render(request, 'home/workspace.html', context=context)


#=========================================================================================
# Record Links
#=========================================================================================

@login_required
def record_links(request, organization_pk, app_pk, list_pk, record_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)
    if is_unauthorized(request, organization, app):
        return HttpResponse('You are not allowed here!', status=401)

    # Record details page (placeholder for now)
    record = get_object_or_404(Record, pk=record_pk)
    record_relations = RecordRelation.objects.all().filter(status='active', child_record=record, parent_record__status='active')
    records = []
    for relation in record_relations:
        records.append(relation.parent_record)

    if request.is_ajax() and request.method == "GET":

        # Call is ajax, just load main content needed here

        html = render_to_string(
            template_name="home/record-links.html",
            context={
                'organization': organization,
                'app': app,
                'list': list,
                'record': record,
                'records': records

            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:

        # If accessing the url directly, load full page

        context = {
            'organization': organization,
            'app': app,
            'list': list,
            'record': record,
            'records': records,
            'type': 'record',
            'record_view': 'record-links'
        }

        return render(request, 'home/workspace.html', context=context)

@login_required
def edit_record(request, organization_pk, app_pk, list_pk, record_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)
    record = get_object_or_404(Record, pk=record_pk)
    if is_unauthorized(request, organization, app):
        return HttpResponse('You are not allowed here!', status=401)
    # Very similar to the add_record view, but includes the field values previously saved
    # Probably a way to combine these views to consolidate

    # We are not using the following here:
    # 1) Django form.Forms (couldn't find a way to create dynamic forms this approach,
    # but we may be able to find eventually)
    # 2) the models.Model @property for list.list_fields or the record.record_fields >>
    # needed an object with both the field inforation and value included so we can edit prvious values here

    # Instead, only approach could find is building an object here then passing it to the frontend
    # template for rending the form

    fields = []
    for list_field in list.list_fields:

        field_object = {}
        field_object['field_id'] = list_field.field_id
        field_object['field_label'] = list_field.field_label
        field_object['field_type'] = list_field.field_type
        field_object['required'] = list_field.required
        field_object['primary'] = list_field.primary
        field_object['visible'] = list_field.visible
        field_object['order'] = list_field.order
        # Get the field value if it exists
        if list_field.field_type == "choose-from-list":
            field_object['select_record'] = RecordField.objects.filter(record__list=list_field.select_list.id, record__status="active", status="active", list_field__primary=True).values_list('record', 'value')
            try:
                field_object['value'] = RecordField.objects.get(record_id=record_pk, list_field_id=list_field.id, status="active").value
            except:
                pass
        else:
            for record_field in record.record_fields:
                if list_field.id == record_field.list_field.id:
                    field_object['value'] = record_field.value

        fields.append(field_object)
    fields.reverse()

    if request.is_ajax() and request.method == "GET":

        # Call is ajax, just load main content needed here

        html = render_to_string(
            template_name="home/record-create.html",
            context={
                'organization': organization,
                'app': app,
                'list': list,
                'fields': fields,
                'record': record
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:

        # If accessing the url directly, load full page

        context = {
            'organization': organization,
            'app': app,
            'list': list,
            'record': record,
            'fields': fields,
            'type': 'edit-record'
        }

        return render(request, 'home/workspace.html', context=context)

# TODO need view for archiving records
def archive_record(request, organization_pk, app_pk, list_pk, record_pk):
    #   this functional is call when user click on the "Archive Record" button on Record Detail Page
    record = get_object_or_404(Record, pk=record_pk)
    record.status = "archived"
    record.save()
    return redirect('list', organization_pk=organization_pk, app_pk=app_pk, list_pk=list_pk)

#===============================================================================
# Records
#===============================================================================

# Will be used later for replacing the default django pk / id's in urls
def generate_random_string(string_length=10):
    # Not sure this is the best approach, but works okay for now

    random = str(uuid.uuid4()) # Make into string
    random = random.replace("-","") # Just letters and numbers
    return random[0:string_length] # Truncate to correct length

def randStr(chars = string.ascii_uppercase + string.ascii_lowercase + string.digits, N=10):
	return ''.join(random.choice(chars) for _ in range(N))


def post_record_comment(request,organization_pk, app_pk, list_pk, record_pk):
    if request.method == "POST":
        if request.POST['content'] != '':
            record_comment = RecordComment(created_user=request.user,content = request.POST['content'],record_id=record_pk)
            record_comment.id = randomstr()
            record_comment.save()
            final = {}
            final['delete_url'] = record_comment.delete_url()
            final['id'] = record_comment.pk
            final['edit_url'] = record_comment.edit_url()
            final['content'] =record_comment.content
            final =json.dumps(final)
            return JsonResponse(data=final, safe=False)
    else:
        return HttpResponse('You are not allowed here!', status=401)



@csrf_exempt
def post_record_file(request,organization_pk, app_pk, list_pk, record_pk):
    record_file = RecordFile(file=request.FILES['file'],record_id=record_pk,created_user = request.user,group=request.POST['file_group'])
    record_file.id =randomstr()
    record_file.save()
    record_File = RecordFile.objects.get(pk=record_file.pk)
    final = {}
    splited_name = record_file.filename().split('.')
    record_file.name_of_file = splited_name[0]
    record_file.file_extension ='.'+splited_name[-1]
    record_file.save()
    record_File = RecordFile.objects.get(pk=record_file.pk)
    final['file_name'] = splited_name[0]
    final['file_extension'] = '.'+splited_name[-1]
    final['file_url'] = record_File.url()
    if str(record_File.image_thumbnail) != '':
        final['thumbnail'] = record_File.image_thumbnail.url
    else:
        final['thumbnail'] = None
    final['delete_url'] = record_File.delete_url()
    final['edit_url']=record_File.edit_url()
    final['id']=record_file.pk
    final['type'] = record_file.type
    final =json.dumps(final)
    return JsonResponse(data=final, safe=False)


# @csrf_exempt
# def post_record_media(request,organization_pk, app_pk, list_pk, record_pk):
#     record_file = RecordMedia(file=request.FILES['file'],record_id=record_pk,created_user = request.user)
#     record_file.id = randomstr()
#     record_file.save()
#     record_File = RecordMedia.objects.get(pk=record_file.pk)
#     final = {}
#     record_file.name_of_file = record_file.filename()
#     record_file.save()
#     final['file_name'] = record_file.filename()
#     if record_file.type == "V":
#        final['file_url'] = record_File.image_thumbnail.url
#     else:
#         final['file_url'] = record_File.url()
#     final['delete_url'] = record_File.delete_url()
#     final =json.dumps(final)
#     return JsonResponse(data=final, safe=False)



# @csrf_exempt
# def delete_record_media(request,organization_pk, app_pk, list_pk, record_pk,record_media_pk):
#     record_File = RecordMedia.objects.get(pk=record_media_pk)
#     record_File.delete()
#     final = {}
#     final['deleted'] = "deleted"
#     final =json.dumps(final)
#     return redirect(reverse('record',kwargs={
#         'organization_pk':record_File.record.list.app.organization.pk,
#         'list_pk':record_File.record.list.pk,
#         'app_pk':record_File.record.list.app.pk,
#         'record_pk':record_File.record.pk,
#     }))



@csrf_exempt
def delete_record_file(request,organization_pk, app_pk, list_pk, record_pk,record_file_pk):
    record_File = RecordFile.objects.get(pk=record_file_pk)
    record_File.delete()
    final = {}
    final['deleted'] = "deleted"
    final =json.dumps(final)
    return redirect(reverse('record',kwargs={
        'organization_pk':record_File.record.list.app.organization.pk,
        'list_pk':record_File.record.list.pk,
        'app_pk':record_File.record.list.app.pk,
        'record_pk':record_File.record.pk,
    }))


@csrf_exempt
def delete_record_comment(request,record_comment_pk,organization_pk, app_pk, list_pk, record_pk):
    record_Comment = RecordComment.objects.get(pk=record_comment_pk)
    if record_Comment.created_user != request.user:
         HttpResponse('Unauthorized', status=401)
    record_Comment.delete()
    final = {}
    final['deleted'] = "deleted"
    final =json.dumps(final)
    return redirect(reverse('record',kwargs={
        'organization_pk':record_Comment.record.list.app.organization.pk,
        'list_pk':record_Comment.record.list.pk,
        'app_pk':record_Comment.record.list.app.pk,
        'record_pk':record_Comment.record.pk,
    }))

@csrf_exempt
def edit_record_comment(request,organization_pk, app_pk, list_pk, record_pk,record_comment_pk):
    if request.method == "POST":
        comment = RecordComment.objects.get(pk=record_comment_pk)
        if request.user == comment.created_user:
            #print(request.POST['content'])
            comment.content = request.POST['comment-content-%s' % record_comment_pk]
            comment.save()
        else:
            HttpResponse('Unauthorized', status=401)
        return JsonResponse({
            "content":  comment.content
        })
    else:
        return HttpResponse('method not allowed')


# @csrf_exempt
# def edit_file(request,file_id,new_name):
#     file = RecordFile.objects.get(pk=file_id)
#     filename = file.filename
#     filename = filename.split('.')[0]


@csrf_exempt
def edit_record_file(request,organization_pk, app_pk, list_pk, record_pk,record_file_pk):
    record_File = RecordFile.objects.get(pk=record_file_pk)
    new_name = request.POST['content']
    record_File.name_of_file = new_name
    new_name += record_File.file_extension
    initial_path = record_File.file.path
    initial_name = record_File.file.name
    new_path = initial_name.split('/')
    new_path.pop()
    new_path_proto = '/'.join(new_path)
    new_path_proto += '/'
    new_path = settings.MEDIA_ROOT + '/' +  new_path_proto  + new_name
    os.rename(initial_path, new_path)
    record_File.file.name = new_path_proto + new_name
    print(record_File.file.name,record_File.file.url,record_File.file.path)
    record_File.save()
    return JsonResponse({
        "content": record_File.name_of_file,
        "file_url":record_File.file.url
    })


@csrf_exempt
def change_list_public_flag(request, organization_pk, app_pk, list_pk):
    response = {}
    list_data = get_object_or_404(List, pk=list_pk)
    is_public = request.POST.get('is_public')
    if is_public == "true":
        is_public = True
    else:
        is_public = False
    list_data.is_public = is_public
    list_data.save()
    response['status'] = True
    return HttpResponse(json.dumps(response), content_type="application/json")


def add_record_without_login(request):
    try:
        reference = request.GET.get('ref')
        list = get_object_or_404(List, public_link=reference)
        organization = get_object_or_404(Organization, pk=list.app.organization.pk)
        app = get_object_or_404(App, pk=list.app.pk)
        fields = []
        for list_field in list.list_fields:
            field_object = {}
            field_object['field_id'] = list_field.field_id
            field_object['field_label'] = list_field.field_label
            field_object['field_type'] = list_field.field_type
            field_object['required'] = list_field.required
            field_object['primary'] = list_field.primary
            field_object['visible'] = list_field.visible
            field_object['order'] = list_field.order
            field_object['id'] = list_field.id
            if list_field.field_type == "choose-from-list":
                field_object['select_record'] = RecordField.objects.filter(record__list=list_field.select_list.id, record__status="active", status="active", list_field__primary=True).values_list('record', 'value')
            fields.append(field_object)
        fields.reverse()

        if request.is_ajax() and request.method == "GET":
            # Call is ajax, just load main content needed here

            html = render_to_string(
                template_name="home/record-create.html",
                context={
                    'organization': organization,
                    'app': app,
                    'list': list,
                    'fields': fields
                }
            )

            data_dict = {"html_from_view": html}

            return JsonResponse(data=data_dict, safe=False)

        else:
            # If accessing the url directly, load full page

            context = {
                'organization': organization,
                'app': app,
                'list': list,
                'fields': fields,
                'type': 'edit-record-anonymous',
            }

            return render(request, 'home/workspace.html', context=context)
    except Exception as e:
        print(e)
        return redirect('/')


def save_record_without_login(request, organization_pk, app_pk, list_pk):
    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)

    record_id = request.POST.get('record_id', None)
    fields = json.loads(request.POST['field_values'])

    record = None

    if record_id is not None:
        record = get_object_or_404(Record, pk=record_id)
    else:
        record = Record.objects.create(
            list=list,
            status='active',
            created_at=timezone.now(),
            id=randomstr())
        record.save()
    for field in fields:
        if record_id is not None:
            try:
                record_field = RecordField.objects.get(status='active', list_field__field_id=field['fieldId'], record=record)
                if field['fieldType'] == "choose-from-list":
                    record_field.selected_record_id = field['fieldValue']
                    record_field.value = field['selectListValue']
                else:
                    record_field.value = field['fieldValue']
                record_field.save()

                if field['fieldType'] == "choose-from-list":
                    try:
                        record_relation = RecordRelation.objects.get(status='active', list_field__field_id=field['fieldId'], parent_record=record)
                        record_relation.child_record_id = field['fieldValue']
                        record_relation.save()
                    except RecordRelation.DoesNotExist:
                        record_relation = RecordRelation.objects.create(
                            parent_record=record,
                            child_record_id=record_field.selected_record_id,
                            relation_type='choose-from-list',
                            list_field=record_field.list_field,
                            status='active',
                            created_at=timezone.now(),
                            id=randomstr())
                        record_relation.save()

            except RecordField.DoesNotExist:
                try:
                    list_field = ListField.objects.get(status='active', field_id=field['fieldId'], list=list)

                    record_field = RecordField.objects.create(
                        record=record,
                        list_field=list_field,
                        status='active',
                        created_at=timezone.now(),
                        id=randomstr())
                    record_field.save()

                    if field['fieldType'] == "choose-from-list":
                        record_field.selected_record_id = field['fieldValue']
                        record_field.value = field['selectListValue']
                    else:
                        record_field.value = field['fieldValue']
                    record_field.save()

                    if field['fieldType'] == "choose-from-list":
                        record_relation = RecordRelation.objects.create(
                            parent_record=record,
                            child_record_id=record_field.selected_record_id,
                            relation_type='choose-from-list',
                            list_field=record_field.list_field,
                            status='active',
                            created_at=timezone.now(),
                            id=randomstr())
                        record_relation.save()

                except ListField.DoesNotExist:
                    pass

        else:
            try:
                list_field = ListField.objects.get(status='active', field_id=field['fieldId'], list=list)

                record_field = RecordField.objects.create(
                    record=record,
                    list_field=list_field,
                    status='active',
                    created_at=timezone.now(),
                    id=randomstr())
                record_field.save()

                if field['fieldType'] == "choose-from-list":
                    record_field.selected_record_id = field['fieldValue']
                    record_field.value = field['selectListValue']
                else:
                    record_field.value = field['fieldValue']
                record_field.save()

                if field['fieldType'] == "choose-from-list":
                    record_relation = RecordRelation.objects.create(
                        parent_record=record,
                        child_record_id=record_field.selected_record_id,
                        relation_type='choose-from-list',
                        list_field=record_field.list_field,
                        status='active',
                        created_at=timezone.now(),
                        id=randomstr())
                    record_relation.save()

            except ListField.DoesNotExist:
                        pass

    data_dict = {"success": True}

    return JsonResponse(data=data_dict, safe=False)
