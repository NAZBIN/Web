from django.shortcuts import render
from django.views.generic import View
from apps.course.models import CourseCategory,Course,Teacher
from utils import restful
from .forms import PubCourseForm

class PubCourse(View):
    def get(self,request):
        context = {
            'categories':CourseCategory.objects.all(),
            'teachers':Teacher.objects.all()
        }
        return render(request,'cms/pub_course.html',context=context)

    def post(self,request):
        form = PubCourseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            category_id = form.cleaned_data.get('category_id')
            video_url = form.cleaned_data.get('video_url')
            cover_url = form.cleaned_data.get("cover_url")
            price = form.cleaned_data.get('price')
            duration = form.cleaned_data.get('duration')
            profile = form.cleaned_data.get('profile')
            teacher_id = form.cleaned_data.get('teacher_id')

            category = CourseCategory.objects.get(pk=category_id)
            teacher = Teacher.objects.get(pk=teacher_id)

            Course.objects.create(title=title, video_url=video_url, cover_url=cover_url, price=price, duration=duration,
                                  profile=profile, category=category, teacher=teacher)
            return restful.ok()
        else:
            return restful.paramserror(message=form.get_errors())