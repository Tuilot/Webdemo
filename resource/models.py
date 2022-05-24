from django.db import models

# Create your models here.


class FileResource(models.Model):
    ChoiceFileType = (
        ('text', '文档'),
        ('picture', '相册'),
        ('audio', '音频'),
        ('video', '视频'),
        ('others', '其他')
    )
    file = models.FileField()
    file_size = models.IntegerField(default=0)
    file_name = models.CharField(max_length=300, default='')
    file_show_name = models.CharField(max_length=300, default='')
    type = models.CharField(max_length=300, default='', choices=ChoiceFileType)
    upload_time = models.DateTimeField(auto_now_add=True)
    view_count = models.IntegerField(default=0)
    download_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-upload_time']