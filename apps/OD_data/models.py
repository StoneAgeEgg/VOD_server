from django.db import models

# Create your models here.

class UploadRecord(models.Model):
    """每次提交记录"""
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name='视频名或图像名')
    run_time = models.IntegerField(verbose_name='运算时间', default=0)
    data_size = models.IntegerField(verbose_name='数据大小', help_text='数据大小为1时，输入为单张图片；大于1时为视频总帧数', default=0)
    upload_time = models.DateField(verbose_name='提交时间', auto_now_add=True)

    class Meta:
        verbose_name = '提交记录'
        verbose_name_plural = '提交记录'
        db_table = 'od_upload_record'


class OneFrameData(models.Model):
    """单图像检测结果"""
    id = models.AutoField(primary_key=True)
    record = models.ForeignKey(to='UploadRecord', on_delete=models.CASCADE, related_name='one_frame_result', verbose_name='提交记录', db_index=True)
    annotation = models.CharField(max_length=32, verbose_name='检测框数据')

    class Meta:
        verbose_name = '检测结果'
        verbose_name_plural = '检测结果'
        db_table = 'od_oneframe_result'



class LabelCategory(models.Model):
    """标签种类"""
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=32, verbose_name='标签种类')

    class Meta:
        verbose_name = '标签种类'
        verbose_name_plural = '标签种类'
        db_table = 'od_label_categoty'   