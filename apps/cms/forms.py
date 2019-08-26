from django import forms
from apps.forms import FormMixin
from apps.news.models import News,Banner
from apps.course.models import Course

class EditNewsCategoryForm(forms.Form,FormMixin):
    pk = forms.IntegerField(error_messages={"required":"请传入关键字id"})
    name = forms.CharField(max_length=100)

class WriteNewsForm(forms.ModelForm,FormMixin):
    category = forms.IntegerField()
    class Meta:
        model = News
        exclude = ['pub_time','author','category']

class AddBannerForm(forms.ModelForm,FormMixin):
    class Meta:
        model = Banner
        fields = ['priority','link_to','image_url']

class UpdateBannerForm(forms.ModelForm,FormMixin):
    pk = forms.IntegerField()
    class Meta:
        model = Banner
        fields = ['priority','link_to','image_url']

class EditNewsForm(forms.ModelForm,FormMixin):
    category = forms.IntegerField()
    pk = forms.IntegerField()
    class Meta:
        model = News
        exclude = ['pub_time','author','category']

class PubCourseForm(forms.ModelForm,FormMixin):
    category_id = forms.IntegerField()
    teacher_id = forms.IntegerField()
    class Meta:
        model = Course
        exclude = ("category",'teacher')