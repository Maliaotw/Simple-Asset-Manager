from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.http import QueryDict
from asset import models
from asset import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def index(request):

    search_field = {}

    category_obj = models.Catagory.objects.all()
    department_obj = models.Department.objects.all()
    user_obj = models.UserProfile.objects.all()

    if request.GET:

        # GET 字段
        name = request.GET.get("name", '')
        cate_id = request.GET.get("cate_id", '')
        dent_id = request.GET.get("dent_id", '')

        search_field['name'] = name
        search_field['cate_id'] = cate_id
        search_field['dent_id'] = dent_id

        print(search_field)

        # GET 字段 篩選

        if cate_id and dent_id:
            asset_obj = models.Asset.objects.filter(sn__contains=name,category_id=cate_id,department_id=dent_id)
        elif cate_id:
            asset_obj = models.Asset.objects.filter(sn__contains=name,category_id=cate_id)
        elif dent_id:
            asset_obj = models.Asset.objects.filter(sn__contains=name,department_id=dent_id)
        else:
            asset_obj = models.Asset.objects.filter(sn__contains=name)

    else:
        asset_obj = models.Asset.objects.all()


    # 分頁功能

    paginator = Paginator(asset_obj, 10)  # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        asset_obj = paginator.page(page)
    except PageNotAnInteger:
        asset_obj = paginator.page(1)
    except EmptyPage:
        asset_obj = paginator.page(paginator.num_pages)



    if request.method == 'POST':

        ret = {
            'msg': '',
            'status': ''
        }

        print(request.POST)

        '''
        {'sn': ['040'], 'user': ['807'], 'department': ['7'], 'price': ['400'], 'category': ['2']}>

        '''

        form_obj = forms.AssetForm(data=request.POST)

        if form_obj.is_valid():
            # print(form_obj)

            manager = form_obj.cleaned_data['manager']
            sn = form_obj.cleaned_data['sn']
            category = form_obj.cleaned_data['category']
            dent = form_obj.cleaned_data['department']
            price = form_obj.cleaned_data['price']

            models.Asset.objects.create(manager=manager, sn=sn, category=category, department=dent,price=price)

            ret['status'] = 'ok'
            ret['msg'] = '新增成功'

        else:
            ret['status'] = 'error'
            ret['msg'] = '輸入錯誤'

        return JsonResponse(ret)

    if request.method == 'PUT':
        print("This is PUT")
        ret = {"status": "", "re_html": "", "msg": ""}

        put = QueryDict(request.body)
        print(put)
        id = put.get('id')
        asset_obj = models.Asset.objects.get(id=id)

        form_obj = forms.AssetForm(data=put, instance=asset_obj)
        if form_obj.is_valid():

            category = form_obj.cleaned_data['category']
            department = form_obj.cleaned_data['department']
            manager = form_obj.cleaned_data['manager']
            price = form_obj.cleaned_data['price']
            purchase_date = form_obj.cleaned_data['purchase_date']


            asset_obj.category = category
            asset_obj.department = department
            asset_obj.manager = manager
            asset_obj.price = price
            asset_obj.purchase_date = purchase_date
            asset_obj.save()

            ret['status'] = "ok"


        else:
            ret['status'] = 'error'

        return JsonResponse(ret)

    return render(request, "asset/index.html", locals())


def department(request):


    ret = {"status": "", "re_html": "", "msg": ""}


    search_field = {}

    department_obj = models.Department.objects.all()
    user_obj = models.UserProfile.objects.all()

    # 分頁功能

    paginator = Paginator(department_obj, 10)  # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        dent_obj = paginator.page(page)
    except PageNotAnInteger:
        dent_obj = paginator.page(1)
    except EmptyPage:
        dent_obj = paginator.page(paginator.num_pages)

    if request.method == 'POST':


        form_obj = forms.DentForm(data=request.POST)

        if form_obj.is_valid():

            form_obj.save()

            ret['status'] = 'ok'
            ret['msg'] = '新增成功'

        else:
            ret['status'] = 'error'
            ret['msg'] = '輸入錯誤'

        return JsonResponse(ret)



    if request.method == 'PUT':
        print("This is PUT")


        put = QueryDict(request.body)
        print(put)
        dent_id = put.get('id')
        dent_obj = models.Department.objects.get(id=dent_id)
        user_id = put.get('user')


        if user_id:
            user_obj = models.UserProfile.objects.get(id=user_id)
            dent_obj.user = user_obj
        else:

            dent_obj.user = None

        dent_obj.save()

        ret['msg'] = '成功'
        ret['status'] = 'ok'

        return JsonResponse(ret)

    if request.method == 'DELETE':
        print("This is Delete")
        put = QueryDict(request.body)
        id = put.get('id')
        dent_obj = models.Department.objects.get(id=id)
        dent_obj.delete()

        ret['msg'] = '成功'
        ret['status'] = 'ok'

        return JsonResponse(ret)



    
    return render(request, "asset/department.html", locals())


def category(request):


    ret = {"status": "", "re_html": "", "msg": ""}

    search_field = {}

    category_obj = models.Catagory.objects.all()

    # 分頁功能

    paginator = Paginator(category_obj, 10)  # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        cary_obj = paginator.page(page)
    except PageNotAnInteger:
        cary_obj = paginator.page(1)
    except EmptyPage:
        cary_obj = paginator.page(paginator.num_pages)


    # 增
    if request.method == 'POST':

        print("This is POST")

        form_obj = forms.CaryForm(data=request.POST)

        if form_obj.is_valid():

            form_obj.save()

            ret['status'] = 'ok'
            ret['msg'] = '新增成功'

        else:
            ret['status'] = 'error'
            ret['msg'] = '輸入錯誤!'


        return JsonResponse(ret)

    # 改
    if request.method == 'PUT':

        print("This is PUT")

        put = QueryDict(request.body)
        print(put)
        cary_id = put.get('id')
        name = put.get('name')
        code = put.get('code')

        cary_obj = models.Catagory.objects.get(id=cary_id)

        form_obj = forms.CaryForm(data=put,instance=cary_obj)

        if form_obj.is_valid():
            form_obj.save()

            ret['status'] = 'ok'
            ret['msg'] = '新增成功'

        else:
            ret['status'] = 'error'
            ret['msg'] = '輸入錯誤!'






        return JsonResponse(ret)


    # 刪
    if request.method == 'DELETE':

        print("This is DELETE")

        return JsonResponse(ret)








    return render(request, "asset/category.html", locals())


def user(request):
    user_obj = models.UserProfile.objects.all()
    return render(request, 'user/index.html', locals())
