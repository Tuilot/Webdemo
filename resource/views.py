from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from common_lib import resource_utils
from common_lib.tool_utils import get_pagination
from resource.models import FileResource


# Create your views here.


def resource_list(request):
    try:
        file_type = request.GET.get('type', default='text')
        search = request.POST.get('keyword', default='')
        page = request.GET.get('page', default=1)
        page = int(page)
        type_list = FileResource.objects.all().filter(type__exact=file_type, file_show_name__contains=search)
        type_count = type_list.count()
        type_list = type_list[(page - 1) * 20: page * 20]
        page_count = (type_count + 19) // 20
        pagination = get_pagination(page, page_count)
        data = {
            'resources': type_list,
            'file_type': file_type,
            'total': type_count,
            'pagination': pagination,
        }
        return render(request, 'resource.html', data)
    except Exception as e:
        return render(request, '404_page.html', {'error_msg': e,
                                                 'btn_msg': '返回首页'})


@csrf_exempt
@login_required(login_url='/account/login')
def resource_upload(request):
    if request.method == 'POST':
        file = request.FILES.get('select_file')
        file_show_name = request.POST.get('file_show_name')
        file_type = request.POST.get('file_type')
        error_msg = upload_file_error(file, file_show_name, file_type)
        if error_msg == {}:
            file.name = resource_utils.random_file_name(file.name)
            FileResource.objects.all().create(
                file=file,
                file_size=file.size,
                file_name=file.name,
                file_show_name=file_show_name,
                type=file_type,
            )
        return render(request, 'resource_hint.html', {'msg': '上传文件成功！',
                                                     'url': '',
                                                     'btn_msg': '继续上传'})

    return render(request, 'resource_upload.html', {'feature': 'upload',
                                                    'choice_file_type': FileResource.ChoiceFileType})


def upload_file_error(file, file_show_name, file_type):
    error_msg = {}
    if file is None:
        error_msg['file'] = '上传文件不能为空'
    if file_show_name is None:
        error_msg['file_show_name'] = '请输入文件名'
    if file_type is None:
        error_msg['file_type'] = '请选择文件类型'
    return error_msg
