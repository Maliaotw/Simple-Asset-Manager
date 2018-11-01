from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse, FileResponse
from django.http import QueryDict
from asset import models
from asset import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
import pandas as pd


# Create your views here.


# --- 資產 ---

def asset(request):
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
            asset_obj = models.Asset.objects.filter(sn__contains=name, category_id=cate_id, department_id=dent_id)
        elif cate_id:
            asset_obj = models.Asset.objects.filter(sn__contains=name, category_id=cate_id)
        elif dent_id:
            asset_obj = models.Asset.objects.filter(sn__contains=name, department_id=dent_id)
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

            models.Asset.objects.create(manager=manager, sn=sn, category=category, department=dent, price=price)

            ret['status'] = 'ok'
            ret['msg'] = '新增成功'

        else:
            ret['status'] = 'error'
            ret['msg'] = '新增信息輸入不正確!'

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


def asset_add(request):
    ret = {"status": "", "re_html": "", "msg": ""}

    if request.method == 'GET':
        forms_obj = forms.Asset_Add_Form(request=request)


    elif request.method == 'POST':

        print(request.POST)
        forms_obj = forms.Asset_Add_Form(request.POST, request=request)

        print(forms_obj.errors)
        #
        fields = set(list(dict(forms_obj.fields).keys()))
        errors = set(list(forms_obj.errors.keys()))
        #
        errors_fields = list(fields & errors)
        success_fields = list(fields - errors)
        print(errors_fields)
        print(success_fields)
        #

        if forms_obj.is_valid():
            print("ok")
            ret['status'] = 'ok'
            ret['msg'] = '新增成功'
            ret['errors_fields'] = errors_fields
            ret['success_fields'] = success_fields

            forms_obj.save()

        else:
            print("error")
            ret['status'] = 'error'
            ret['msg'] = '輸入不正確!'
            ret['errors_fields'] = errors_fields
            ret['success_fields'] = success_fields

            print(forms_obj.errors)

        return JsonResponse(ret)

    return render(request, "asset/asset_add.html", locals())


def asset_edit(request, pk):
    ret = {"status": "", "re_html": "", "msg": ""}

    asset_obj = models.Asset.objects.get(id=pk)

    if request.method == 'GET':
        forms_obj = forms.Asset_Edit_Form(instance=asset_obj, request=request)

    if request.method == 'POST':

        forms_obj = forms.Asset_Edit_Form(data=request.POST, instance=asset_obj, request=request)

        print(forms_obj.errors)

        fields = set(list(dict(forms_obj.fields).keys()))
        errors = set(list(forms_obj.errors.keys()))

        errors_fields = list(fields & errors)
        success_fields = list(fields - errors)
        print(errors_fields)
        print(success_fields)

        if forms_obj.is_valid():
            print("ok")
            ret['status'] = 'ok'
            ret['msg'] = '修改成功'
            ret['errors_fields'] = errors_fields
            ret['success_fields'] = success_fields
            forms_obj.save()
        else:
            print("error")
            ret['status'] = 'error'
            ret['msg'] = '輸入不正確!'
            ret['errors_fields'] = errors_fields
            ret['success_fields'] = success_fields

        return JsonResponse(ret)

    return render(request, "asset/asset_edit.html", locals())


def asset_input(request):
    
    if request.method == 'POST':
        return HttpResponse("ok")
    

    return render(request, "asset/asset_input.html", locals())


def asset_output(request):
    import csv

    a = models.Asset.objects.all()

    opts = models.Asset.objects.all().model._meta
    model = models.Asset.objects.all().model
    response = HttpResponse(content_type='text/csv; charset=cp936')

    # force download.
    response['Content-Disposition'] = 'attachment;filename=export.csv'
    # the csv writer
    writer = csv.writer(response)

    # ['ID', '資產編號', '價格', '類型', '部門', '負責人', '購買日期', '狀態', '更新日期', '創建日期']
    row_names = [field.verbose_name for field in opts.fields]
    print(row_names)

    # ['id', 'sn', 'price', 'category', 'department', 'manager', 'purchase_date', 'status', 'latest_date', 'create_date']
    field_names = [field.name for field in opts.fields]
    print(field_names)

    # Write a first row with header information
    writer.writerow(row_names)
    # Write data rows
    for obj in models.Asset.objects.all():

        ret = []
        ret.append(obj.id)
        sn = "%s-%s" % (obj.category.code,obj.sn)
        ret.append(sn)
        ret.append(obj.price)
        ret.append(obj.category)
        ret.append(obj.department)
        ret.append(obj.manager)
        ret.append(obj.purchase_date)
        ret.append(obj.get_status_display())
        ret.append(obj.latest_date)
        ret.append(obj.create_date)
        writer.writerow(ret)

    return response

# --- 部門 ---

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
            ret['msg'] = '新增信息輸入不正確!'

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

    return render(request, "department/index.html", locals())


def department_input(request):
    pass


def department_output(request):
    pass


# --- 類型 ---

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

        form_obj = forms.CaryForm(data=put, instance=cary_obj)

        if form_obj.is_valid():
            form_obj.save()

            ret['status'] = 'ok'
            ret['msg'] = '修改成功'

        else:
            ret['status'] = 'error'
            ret['msg'] = '修改信息輸入不正確!'

        return JsonResponse(ret)

    # 刪
    if request.method == 'DELETE':
        print("This is Delete")
        put = QueryDict(request.body)
        id = put.get('id')

        print(put)

        cary_obj = models.Catagory.objects.get(id=id)
        cary_obj.delete()

        ret['msg'] = '成功'
        ret['status'] = 'ok'

        return JsonResponse(ret)

    return render(request, "category/index.html", locals())


def category_input(request):
    pass


def category_output(request):
    pass


# --- 用戶 ---

def user(request):
    ret = {"status": "", "re_html": "", "msg": ""}
    search_field = {}

    user_obj = models.UserProfile.objects.all()
    sex_obj = models.UserProfile.sex_choice

    # print(sex_obj)

    dent_obj = models.Department.objects.all()

    # user forms表單
    form_obj = forms.User_Add_Form()

    if request.GET:
        # GET 字段
        name = request.GET.get("name", '')
        sex_id = request.GET.get("sex_id", '')
        dent_id = request.GET.get("dent_id", '')

        search_field['name'] = name
        search_field['sex_id'] = sex_id
        search_field['dent_id'] = dent_id

        # GET 字段 篩選

        if sex_id and dent_id:
            user_obj = models.UserProfile.objects.filter(name__contains=name, sex=sex_id, dent_id=dent_id)
        elif sex_id:
            user_obj = models.UserProfile.objects.filter(name__contains=name, sex=sex_id)
        elif dent_id:
            user_obj = models.UserProfile.objects.filter(name__contains=name, dent_id=dent_id)
        else:
            user_obj = models.UserProfile.objects.filter(name__contains=name)

    # 分頁功能

    paginator = Paginator(user_obj, 10)  # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        user_obj = paginator.page(page)
    except PageNotAnInteger:
        user_obj = paginator.page(1)
    except EmptyPage:
        user_obj = paginator.page(paginator.num_pages)

    # 增
    if request.method == 'POST':

        print("This is POST")

        form_obj = forms.User_Add_Form(data=request.POST)

        # 驗證錯誤及正常字段
        fields = set(list(dict(form_obj.fields).keys()))
        errors = set(list(form_obj.errors.keys()))

        errors_fields = list(fields & errors)
        success_fields = list(fields - errors)
        print(errors_fields)
        print(success_fields)

        print(form_obj.errors)

        if form_obj.is_valid():

            # 取值
            name = form_obj.cleaned_data.get('name')
            sex = form_obj.cleaned_data.get('sex')
            code = form_obj.cleaned_data.get('code')
            dent = form_obj.cleaned_data.get('dent')
            username = form_obj.cleaned_data.get('username')

            # 創建user
            user = User()
            user.username = username
            user.set_password('12345678')
            user.is_staff = False
            user.save()

            # 創建Userinfo

            # 只取編號不包含部門編號
            code = code[len(dent.block_number):]
            models.UserProfile.objects.create(user=user, name=name, sex=sex, code=code, dent=dent)

            # result
            ret['status'] = 'ok'
            ret['msg'] = '新增成功'
            ret['errors_fields'] = errors_fields
            ret['success_fields'] = success_fields

        else:

            ret['status'] = 'error'
            ret['msg'] = '用戶信息輸入不正確!'
            ret['errors_fields'] = errors_fields
            ret['success_fields'] = success_fields

        return JsonResponse(ret)

    # 改
    if request.method == 'PUT':
        return JsonResponse(ret)

    # 刪
    if request.method == 'DELETE':
        return JsonResponse(ret)

    return render(request, 'user/index.html', locals())


def user_info(request):
    pass


def user_add(request):
    ret = {"status": "", "re_html": "", "msg": ""}

    if request.method == 'GET':
        forms_obj = forms.User_Add_Form()

    if request.method == 'POST':

        print("This is POST")

        form_obj = forms.User_Add_Form(data=request.POST)
        print(request.POST)

        print(form_obj.errors)
        #
        fields = set(list(dict(form_obj.fields).keys()))
        errors = set(list(form_obj.errors.keys()))
        #
        errors_fields = list(fields & errors)
        success_fields = list(fields - errors)
        print(errors_fields)
        print(success_fields)
        #
        print(form_obj.errors)
        #
        if form_obj.is_valid():
            print("ok")

            name = form_obj.cleaned_data.get('name')
            sex = form_obj.cleaned_data.get('sex')
            code = form_obj.cleaned_data.get('code')
            dent = form_obj.cleaned_data.get('dent')
            username = form_obj.cleaned_data.get('username')
            birthday = form_obj.cleaned_data.get('birthday')
            in_service = form_obj.cleaned_data.get('in_service')
            is_staff = form_obj.cleaned_data.get('is_staff')
            password1 = form_obj.cleaned_data.get('password1')
            password2 = form_obj.cleaned_data.get('password2')

            # 創建user

            # 驗證passwd
            if password1 and password2:
                passwd = password1
            else:
                passwd = "12345678"

            user = User()
            user.username = username
            user.set_password(passwd)
            user.is_staff = is_staff
            user.save()

            # 創建Userinfo

            # 只取編號不包含部門編號
            code = code[len(dent.block_number):]
            models.UserProfile.objects.create(
                user=user,
                name=name,
                sex=sex,
                code=code,
                dent=dent,
                birthday=birthday,
                in_service=in_service

            )

            ret['status'] = 'ok'
            ret['msg'] = '新增成功'
            ret['errors_fields'] = errors_fields
            ret['success_fields'] = success_fields

        else:

            ret['status'] = 'error'
            ret['msg'] = '用戶信息輸入不正確!'
            ret['errors_fields'] = errors_fields
            ret['success_fields'] = success_fields

        return JsonResponse(ret)

    return render(request, "user/user_add.html", locals())


def user_edit(request, pk):
    # pk = 804

    userinfo_obj = models.UserProfile.objects.get(id=pk)

    if request.method == 'GET':
        forms_user_obj = forms.UserForm(instance=userinfo_obj.user, request=request)
        forms_userproinfo_obj = forms.UserProfileForm(instance=userinfo_obj, request=request)

    if request.method == 'POST':

        print(request.POST)

        forms_user_obj = forms.UserForm(request.POST, instance=userinfo_obj.user, request=request)
        forms_userproinfo_obj = forms.UserProfileForm(request.POST, instance=userinfo_obj, request=request)

        # 確認表單提交無誤
        if forms_user_obj.is_valid() and forms_userproinfo_obj.is_valid():
            print("ok")

            # 取值

            username = forms_user_obj.cleaned_data.get('username')
            is_staff = forms_user_obj.cleaned_data.get('is_staff')

            password1 = forms_user_obj.cleaned_data.get('password1')
            password2 = forms_user_obj.cleaned_data.get('password2')

            name = forms_userproinfo_obj.cleaned_data.get('name')
            in_service = forms_userproinfo_obj.cleaned_data.get('in_service')
            birthday = forms_userproinfo_obj.cleaned_data.get('birthday')
            sex = forms_userproinfo_obj.cleaned_data.get('sex')
            code = forms_userproinfo_obj.cleaned_data.get('code')
            dent = forms_userproinfo_obj.cleaned_data.get('dent')

            userinfo = forms_user_obj.save(commit=False)
            # 修改密碼
            if password1 and password2:
                userinfo.user.set_password(password1)

            # 修改用戶

            userinfo.save()

            # 修改用戶profifle
            code = code[len(dent.block_number):]

            userproinfo_obj = forms_userproinfo_obj.save(commit=False)
            userproinfo_obj.code = code
            userproinfo_obj.save()


        else:
            print("error")
            print(forms_user_obj.errors)
            print(forms_userproinfo_obj.errors)

    return render(request, "user/user_edit.html", locals())


def user_input(request):
    pass


def user_output(request):
    pass


# --- 測試 ---

def test1(request):
    print("this is test1")

    forms_obj = forms.test1Form()
    print(models.Catagory.objects.filter(id=2))
    print([models.Catagory.objects.get(id=2)])
    data = {'id': '', 'cary': models.Catagory.objects.filter(id=2), 'dent': models.Department.objects.filter(id=8)}
    print(data)
    forms_obj1 = forms.test1Form(data)

    # forms_obj1.fields["cary"].queryset=models.Catagory.objects.filter(id=2)
    # forms_obj1.fields["dent"].queryset=models.Department.objects.filter(id=8)

    print("forms_obj1.errors", forms_obj1.errors)

    if request.method == "POST":
        print(request.POST)

        print("forms_obj.errors", forms_obj.errors)

    return render(request, "test/test1.html", locals())


def test2(request):
    userinfo_obj = models.UserProfile.objects.get(id=796)
    # dent_obj = models.Department.objects.all()

    if request.method == 'GET':
        forms_user_obj = forms.UserForm(instance=userinfo_obj.user, request=request)
        forms_userproinfo_obj = forms.UserProfileForm(instance=userinfo_obj, request=request)

    elif request.method == 'POST':

        print(request.POST)

        forms_user_obj = forms.UserForm(request.POST, instance=userinfo_obj.user, request=request)
        forms_userproinfo_obj = forms.UserProfileForm(request.POST, instance=userinfo_obj, request=request)

        if forms_user_obj.is_valid() and forms_userproinfo_obj.is_valid():
            print("ok")
        else:
            print("error")

        print(forms_user_obj.errors)
        print(forms_userproinfo_obj.errors)

    return render(request, "test/test2.html", locals())
