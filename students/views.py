# عندما يكون العلاقة بين جدولين واحد لواحد نسطيع الوصول من اي جدول الى الاخر باستخدام اسم الجدول
# عند وجود علاقه واحد لاكثر فنستطيع الوصول الى خصائص الجدول اما باستخدام _سيت او من خلال الريليتد نيم

from django.shortcuts import render
from django.http import Http404
from institute.models import Student
from students.models import Outing
from complaints.models import Complaint, MedicalIssue
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from .forms import OutingForm


class StudentTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_student

def student_check(user):
    return user.is_authenticated and user.is_student


# راجع الديكور حيث يتم استدعاء الديكور والذي يحوي ايضا على ديكور وارب الذي يحافظ على البيانات الوصفية لدالة الهوم
# وبحيث يتم تنفيذ ما بداخله
# الحفاظ على البيانات الوصفية الأصلية (مثل الاسم وسلسلة المستندات والوحدة النمطية)
@user_passes_test(student_check)
def home(request):
    user = request.user
    student = user.student
    modelname = MedicalIssue.model_name(request)
    # "2023-07-19،2023-07-20،2023-07-21" فسيكون عدد التواريخ الحالية 3
    present_dates_count = (student.attendance.present_dates and len(set(student.attendance.present_dates.split(',')))) or 0
    absent_dates_count = (student.attendance.absent_dates and len(set(student.attendance.absent_dates.split(',')))) or 0
    outing_count = len(student.outing_set.all())
    complaints = Complaint.objects.filter(user = user, status="Registered") | Complaint.objects.filter(user = user, status="Processing") 
    medicalissue = MedicalIssue.objects.filter(user = user, status="Registered")
    # print(modelname)

    return render(request, 'students/home.html', {'student': student, 'present_dates_count':present_dates_count, 'absent_dates_count':absent_dates_count, 'outing_count': outing_count, 'complaints':complaints, 'medicalissue': medicalissue})


class OutingListView(StudentTestMixin, ListView):
    model = Student
    template_name = 'students/outing_list.html'
    context_object_name = 'outing_list'

    def get_queryset(self):
        # print(self.request)
        # print(self.request.user)
        # print(self.request.user.student)

        # """
        # انا اريد ان اذهب من جدول اليوزر الى الستودينت ثم الاوتينغ ثم اعود الى الستودينت
        # لكن الطريقة الاولى خاطئة ستعيد كويريسيت وبالتالي لن استطيع الوصول الى محتويات الاوبجيكت ولا الاستعلام
        # بتالالي هنا تكمن فوائد الاستعلام فاليوس
        # print(self.request.user.student.outing_set.filter(student = self.request.user.student))
        # print(self.request.user.student.outing_set.filter(student = self.request.user.student).values('fromDate'))
        # """
        # print(self.request.user.student.outing_set.all())
        # print(self.request.student.purpose)
        # print(self.request.user.student.outing_set.explain())
        # from 1 --->  manny using _set
        return self.request.user.student.outing_set.all()


class OutingCreateView(StudentTestMixin, SuccessMessageMixin, CreateView):
    model = Outing
    form_class = OutingForm
    template_name = 'students/outing_form.html'
    success_url = reverse_lazy('students:outing_list')
    success_message = 'Outing application successfully created!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Outing Application'
        return context

    def form_valid(self, form):
        form.instance.student = self.request.user.student
        return super().form_valid(form)


class OutingUpdateView(StudentTestMixin, SuccessMessageMixin, UpdateView):
    model = Outing
    form_class = OutingForm
    template_name = 'students/outing_form.html'
    success_url = reverse_lazy('students:outing_list')
    success_message = 'Outing application successfully updated!'

    def get(self, request, *args, **kwargs):
        response =  super().get(request, *args, **kwargs)
        # print(self.object.student)
        # print(self.object)
        # print(self.request.user.student)
        if not (self.object.student == self.request.user.student and self.object.is_editable()): 
            raise Http404('Cannot edit the outing application.')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Outing Application'
        return context

    # get, get_context_data يتم تنفيذهما مع اظهار الفورم اما
    # form_valid يتم تنفيذه بعد عمل سابميت للفورم
    def form_valid(self, form):
        # print(form.instance.student)
        # print(form.instance)
        form.instance.student = self.request.user.student
        return super().form_valid(form)


@user_passes_test(student_check)
def attendance_history(request):
    student = request.user.student
    # print(student.attendance.present_dates)
    # print(student.attendance.present_dates.split(','))
    # print(student.attendance.absent_dates.split(','))
    present_dates = (student.attendance.present_dates and student.attendance.present_dates.split(',')) or None
    absent_dates = (student.attendance.absent_dates and student.attendance.absent_dates.split(',')) or None

    return render(request, 'students/attendance_history.html', {'student': student, 'present_dates': present_dates, 'absent_dates': absent_dates})