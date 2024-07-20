from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import DetailView
from institute.models import Block, Student, Official
from students.models import Attendance, RoomDetail, Outing
from django.contrib import messages
from django.http.response import Http404, HttpResponseForbidden
from complaints.models import Complaint
from workers.models import Worker, Attendance as AttendanceWorker


# إضافة السمات ديناميكيًا إلى المثيلات يمكن أن تكون مفيدة للبيانات أو العمليات الحسابية المؤقتة.
#  ومع ذلك ، إذا كنت بحاجة إلى تخزين هذه المعلومات في قاعدة البيانات ، فيجب عليك تعريفها كحقل في النموذج
# Attendance1 = Attendance()
# Attendance1.present_on_date = True
# print(Attendance1.present_on_date)



def official_check(user):
    return user.is_authenticated and user.is_official

def chief_warden_check(user):
    return official_check(user) and user.official.is_chief()


# Create your views here.
@user_passes_test(official_check)
def home(request):
    user = request.user
    official = user.official
    if official.is_chief():
        present_students = Attendance.objects.filter(status='Present')
        absent_students = Attendance.objects.filter(status='Absent')
        complaints = official.related_complaints()
        # print(complaints)

    else:
        if not official.block: 
            raise Http404('You are currently not appointed any block! Please contact Admin')

        student_rooms = official.block.roomdetail_set.all()
        student_ids = student_rooms.values_list('student', flat=True)
        students = Student.objects.filter(pk__in=student_ids)
        present_students = Attendance.objects.filter(student__in=students, status='Present')
        absent_students = Attendance.objects.filter(student__in=students, status='Absent')
        complaints = official.related_complaints()

    return render(request, 'officials/home.html', {'user_details': official, 'present':present_students, 'absent':absent_students, 'complaints':complaints,})


@user_passes_test(official_check)
def profile(request):
    user = request.user
    official = user.official
    complaints = Complaint.objects.filter(user = user)
    return render(request, 'officials/profile.html', {'official': official, 'complaints': complaints})


@user_passes_test(official_check)
@csrf_exempt
def attendance(request):
    user = request.user
    official = user.official
    block = official.block
    attendance_list  = Attendance.objects.filter(student__in=block.roomdetail_set.all().values_list('student', flat=True))
    # print(attendance_list)
    date = None

    if request.method == 'POST' and request.POST.get('submit'):
        date = request.POST.get('date')
        for attendance in attendance_list:
            if request.POST.get(str(attendance.id)): attendance.mark_attendance(date, request.POST.get(str(attendance.id)))

        messages.success(request, f'Attendance marked for date: {date}')

    if request.GET.get('for_date'):
        date = request.GET.get('for_date')
        messages.info(request, f'Selected date: {date}')
        for item in attendance_list:
            # لاحظ انو فيني ضيف اي متغير للوبجيكت حتى لو مانو موجود بالموديل بس ليش معرفت
            # present_on_date متل هادا مانو موجود بس ضفتو
            if item.present_dates and date in set(item.present_dates.split(',')): item.present_on_date = True
            if item.absent_dates and date in set(item.absent_dates.split(',')): item.absent_on_date = True

    return render(request, 'officials/attendance.html', {'official': official, 'attendance_list': attendance_list, 'date': date})


@user_passes_test(official_check)
@csrf_exempt
def attendance_workers(request):
    user = request.user
    official = user.official
    block = official.block
    attendance_list  = AttendanceWorker.objects.filter(worker__in=block.worker_set.all())
    date = None 

    if request.method == 'POST' and request.POST.get('submit'):
        date = request.POST.get('date')
        for attendance in attendance_list:
            if request.POST.get(str(attendance.id)): attendance.mark_attendance(date, request.POST.get(str(attendance.id)))

        messages.success(request, f'Staff Attendance marked for date: {date}')

    if request.GET.get('for_date'):
        date = request.GET.get('for_date')
        messages.info(request, f'Selected date: {date}')
        for item in attendance_list:
            if item.present_dates and  date in set(item.present_dates.split(',')): item.present_on_date = True
            if item.absent_dates and date in set(item.absent_dates.split(',')): item.absent_on_date = True

    return render(request, 'officials/attendance_workers.html', {'official': official, 'attendance_list': attendance_list, 'date': date})


@user_passes_test(official_check)
def attendance_log(request):
    user = request.user
    official = user.official
    student = None
    present_attendance = None
    absent_attendance = None
    present_dates = None
    absent_dates = None

    if official.is_chief():
        attendance_list = Attendance.objects.all()
        # print("#############################################")
        # print(attendance_list)
        # print(type(attendance_list))
    else:
        attendance_list = Attendance.objects.filter(student__in = official.block.roomdetail_set.all().values_list('student', flat=True))
        # print("#############################################")
        # print(attendance_list)
        # print(type(attendance_list))

    if request.GET.get('by_regd_no'):
        try:
            # نجلب غرض الاتيندانس والذي يوافق رقم الطالب فيه الرقم المدخل في الصفحة
            student = attendance_list.get(student__regd_no = request.GET.get('by_regd_no')).student
            # print(student)
            if student.attendance.present_dates: present_dates = student.attendance.present_dates.split(',') 
            if student.attendance.absent_dates: absent_dates = student.attendance.absent_dates.split(',')
        except Attendance.DoesNotExist:
            messages.error(request, "Invalid Student Registration No.")

    if request.GET.get('by_date'):
        # from datetime import datetime
        # search_date = datetime.strptime(request.GET.get('by_date'), '%Y-%m-%d').date()
        # formatted_date = search_date.strftime('%m %d %Y')
        # present_attendance = attendance_list.filter(present_dates__contains = formatted_date)
        present_attendance = attendance_list.filter(present_dates__contains = request.GET.get('by_date'))
        # absent_attendance = attendance_list.filter(absent_dates__contains = formatted_date)
        absent_attendance = attendance_list.filter(absent_dates__contains = request.GET.get('by_date'))
        # print("##########################")
        # print(request.GET.get('by_date'))
        # print(type(request.GET.get('by_date')))
        # print(present_attendance)
        # print(absent_attendance)

        if present_attendance.count() == 0 and absent_attendance.count() == 0:
            messages.error(request, "No Attendance Records Found!")

    return render(request, 'officials/attendance_log.html', {'official':official, 'student': student, 'date': request.GET.get('by_date'),'present_attendance': present_attendance, 'absent_attendance': absent_attendance, 'present_dates': present_dates, 'absent_dates': absent_dates})


@user_passes_test(official_check)
def generate_attendance_sheet(request):
    from .utils import AttendanceBookGenerator
    from django.utils import timezone
    from django.http import HttpResponse
    
    year_month = request.GET.get("year_month")
    block_id = request.GET.get("block_id")
    print(year_month)
    print(block_id)

    # يتوافق نوع المحتوى هذا مع نوع MIME لملفات Excel بتنسيق .xlsx ، وهو التنسيق الأحدث المستند إلى XML والذي يستخدمه Microsoft Excel.
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',)
    # تم تعيين رأس "Content-Disposition" لتحديد سلوك كيفية تعامل مستعرض العميل مع الاستجابة
    # في هذه الحالة ، يتم تعيينه على "مرفق" ، مما يعني أنه سيتم التعامل مع الاستجابة كتنزيل ملف
    response['Content-Disposition'] = 'attachment; filename=Attendance({date}).xlsx'.format(date=timezone.now().strftime('%d-%m-%Y'),)
    
    BookGenerator = AttendanceBookGenerator(block_id, year_month)
    workbook = BookGenerator.generate_workbook()
    # كتابة بيانات المصنف إلى كائن الاستجابة ، مما يؤدي إلى إنشاء ملف Excel في الذاكرة بشكل فعال
    workbook.save(response)

    return response

@user_passes_test(official_check)
def grant_outing(request):
    user = request.user
    official = user.official
    outings = Outing.objects.filter(student__in=official.block.roomdetail_set.all().values_list('student', flat=True), permission="Pending")

    return render(request, 'officials/grant_outing.html', {'official': official, 'outings': outings})


@user_passes_test(official_check)
def outing_detail(request, pk):
    outing = get_object_or_404(Outing, id=pk)

    if request.POST.get('permission'):
        outing.permission = request.POST.get('permission')
        outing.save()

        messages.success(request, f'Outing successfully {outing.permission.lower()} to {outing.student.name}')
        return redirect('officials:grant_outing')
    return render(request, 'officials/outing_show.html', {'outing': outing})


@user_passes_test(chief_warden_check)
@csrf_exempt
def blockSearch(request):
    user = request.user
    official = user.official
    blocks = Block.objects.all()

    if request.POST:
        block_id = request.GET.get('block')
        # print("###########################")
        # print("request.POST")
        # print("##################")
        # print(block_id)
        
        if request.POST.get('Add'):
        # submitted_id = request.POST.get('id')
        # name = request.POST.get('name')
        # print(name)
        # print(request.POST)
        # submitted_id1 = request.GET.get('id')
        # print(submitted_id)
        # print(submitted_id1)
        # if submitted_id == 'add_id' :
            block = Block.objects.get(id = request.POST.get('block_id'))
            # print("###########################")
            # print("request.POST.get('Add')")
            # print("##################")
            # print(block)
            try:
                student = Student.objects.get(regd_no = request.POST.get('regd_no'))
                if not student.is_hosteller:
                    raise ValidationError("Cannot assign room to day scholars.")
                room_detail = student.roomdetail
                # عند الذهاب الى الادمن وبالاخص الرووم ديتيلس نجد ان لكل طالب روم ديتيلس حتى قبل تحديد هذه الغرفو
                # بالتالي عندما يتحدد البلوك ورقم الغرفة والطابق نستطيع القول ان الطال قد حجز غرفة ولا يجوز ان يحجز واحده اخرى
                if room_detail.block and room_detail.room():
                    messages.error(request, f'Student {student.regd_no} already alloted room in {room_detail.block.name} {room_detail.room()}!')
                else:
                    room_detail.block = block
                    room_detail.floor = request.POST.get('floor')
                    room_detail.room_no = request.POST.get('room_no')
                    room_detail.full_clean()
                    # print(room_detail)
                    room_detail.save()
                    messages.success(request, f'Student {student.regd_no} successfully alloted room in {room_detail.block.name} {room_detail.room()}!')
            except RoomDetail.DoesNotExist as error:
                # Day Scholars have no room detail.
                messages.error(request, "Cannot assign room to day scholars.")
            except ValidationError as error:
                for message in error.messages:
                    messages.error(request, message)
            except Student.DoesNotExist:
                messages.error(request, f'Student not found!')

        if request.POST.get('remove'):
        # if submitted_id == 'remove_id':
            # وقت بكون في سمة بالصفخة بدي التقطا بحطا ضمن حقل مخفي وبحطلا نييم وقيمة
            # واذا بدي قيمة تانيه كمان بدي اعمل ويحد تاني وضفلو النيم والقيمة البدي ياها
            # متل هون بدي الايدي فعملت حقل مخفي سميتو رومديتيلايدي وقيمتو هيي الايدي الفعليه 
            room_detail = RoomDetail.objects.get(id = request.POST.get('roomdetail_id'))
            # print("###########################")
            # print("request.POST.get('remove')")
            # print("###############################")
            # print(room_detail)
            # print(room_detail.block)
            # print(room_detail.floor)
            # print(room_detail.room_no)
            
            room_detail.block = None
            room_detail.floor = None
            room_detail.room_no = None
            room_detail.save()
            messages.success(request, f'Student {room_detail.student.regd_no} removed from room.')

        # http://www.example.com/path/to/resource?param1=value1&param2=value2
        # http://www.example.com: هذا هو عنوان الأساسي 
        # path/to/resource هذا هو مسار المورد على الخادم الذي يريد العميل الوصول إليه
        # فاصل بين عنوان الاساسي  ومعلمات الطلب   ؟ 
        #   param1=value1&param2=value2  هذه هي معلمات الاستعلام وقيمها. يتم فصل المعلمات المتعددة بواسطة علامة العطف
        return redirect(reverse_lazy('officials:blockSearch') + '?block={}'.format(block_id))

    if request.GET.get('block'):
        # print(request.GET.get('block'))       value="{{item.id}}  =   1,2,.....
        from django.core.serializers import serialize
        block = Block.objects.get(id=request.GET.get('block'))
        # print("###########################")
        # print("request.GET.get('block')")
        # print("###########################")
        # print(block)
        block_json = serialize('json', [block])
        # print("###########################")
        # print("block_json")
        # print("########################")
        # print(block_json)
        return render(request, 'officials/block_layout.html',{'blocks':blocks, 'current_block': block, 'current_block_json': block_json})
    # print("###########################")
    # print("not GET OR POST")
    # print("###########################")
    # print(blocks)
    return render(request, 'officials/block_layout.html',{'blocks':blocks})

# @user_passes_test(chief_warden_check)
# @csrf_exempt
# def watercan(request):
#     name = request.COOKIES['username_off']
#     off_details = Officials.objects.get(emp_id=str(name))
#     block_details = Blocks.objects.get(emp_id_id=str(name))

#     if request.method == 'POST':
#         if request.POST.get('submit_btn'):
#             date = request.POST.get('date')
#             received = request.POST.get('received')
#             given = request.POST.get('given')

#             if WaterCan.objects.filter(block=block_details, date=date).exists():
#                 current = WaterCan.objects.get(block=block_details, date=date)
#                 current.received = received
#                 current.given = given
#                 current.save()
#             else:
#                 newCan = WaterCan(block=block_details, date=date, received=received, given=given)
#                 newCan.save()
#             messages.success(request, 'Water Cans Info updated')
#             return redirect('officials:watercan')

#         elif request.POST.get('count_btn'):
#             if request.POST.get('date_hist'):
#                 date_hist = request.POST.get('date_hist')
#                 if WaterCan.objects.filter(block=block_details, date=date_hist).exists():
#                     dateRec = WaterCan.objects.get(block=block_details, date=date_hist).received
#                     dateGiven = WaterCan.objects.get(block=block_details, date=date_hist).given
#                 else:
#                     dateRec = -10
#                     dateGiven = -10
#                 return render(request, 'officials/water-can.html', {'dateRec':dateRec, 'dateGiven':dateGiven, 'dateUsed':dateGiven})

#             elif request.POST.get('month_hist'):
#                 month = int(request.POST.get('month_hist').split('-')[1])
#                 if WaterCan.objects.filter(block=block_details, date__month=month).exists():
#                     month_set = WaterCan.objects.filter(block=block_details, date__month=month).order_by('-date')
#                     month_rec = month_set.aggregate(Sum('received'))['received__sum']
#                     month_given = month_set.aggregate(Sum('given'))['given__sum']
#                     month_used = month_given
#                     return render(request, 'officials/water-can.html', {'month':request.POST.get('month_hist'), 'month_empty':False, 'month_set':month_set, 'month_rec':month_rec, 'month_given':month_given, 'month_used':month_used})
#                 else:
#                     return render(request, 'officials/water-can.html', {'month_empty':True})



#     return render(request, 'officials/water-can.html')


from .forms import StudentForm, WorkerForm
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

class OfficialTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_official


class ChiefWardenTestMixin(OfficialTestMixin):
    def test_func(self):
        is_official = super().test_func() 
        return is_official and self.request.user.official.is_chief()


class StudentListView(OfficialTestMixin, ListView):
    model = Student
    template_name = 'officials/student_list.html'

    def get_queryset(self):
        if self.request.user.official.is_chief(): return Student.objects.all()
        else: return Student.objects.filter(roomdetail__block=self.request.user.official.block) 

class StudentDetailView(OfficialTestMixin, DetailView):
    model = Student
    template_name = 'officials/student_detail.html'

    def get(self, request, *args, **kwargs):
        response =  super().get(request, *args, **kwargs)
        if not self.request.user.official.is_chief() and (self.object.roomdetail.block != self.request.user.official.block): 
            return HttpResponseForbidden()
        return response


class StudentRegisterView(CreateView):
    template_name = 'officials/student-register-form.html'
    model = Student
    form_class = StudentForm
    # fields = ['user', 'name', 'branch', 'phone', 'account_email', 'email', 'regd_no']
    success_url = reverse_lazy('officials:student_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Register Student'
        return context

class StudentUpdateView(ChiefWardenTestMixin, LoginRequiredMixin, UpdateView):
    template_name = 'officials/student-register-form.html'
    model = Student
    form_class = StudentForm
    success_url = reverse_lazy('officials:student_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Student Details'
        return context

class StudentDeleteView(ChiefWardenTestMixin, LoginRequiredMixin, DeleteView):
    model = Student
    success_url = reverse_lazy('officials:student_list')

class OfficialListView(ChiefWardenTestMixin, ListView):
    model = Official
    template_name = 'officials/official_list.html'

class OfficialRegisterView(ChiefWardenTestMixin, CreateView):
    template_name = 'officials/official-register-form.html'
    model = Official
    fields = ['emp_id', 'name', 'designation', 'phone', 'account_email', 'email', 'block']
    success_url = reverse_lazy('officials:emp_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Register Official'
        return context

class OfficialUpdateView(ChiefWardenTestMixin, LoginRequiredMixin, UpdateView):
    template_name = 'officials/official-register-form.html'
    model = Official
    fields = ['emp_id', 'name', 'designation', 'phone', 'account_email', 'email', 'block']
    success_url = reverse_lazy('officials:emp_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Official Details'
        return context

class OfficialDeleteView(ChiefWardenTestMixin, LoginRequiredMixin, DeleteView):
    model = Official
    success_url = reverse_lazy('officials:emp_list')

class WorkerListView(ChiefWardenTestMixin, ListView):
    model = Worker
    template_name = 'officials/workers_list.html'

class WorkerRegisterView(ChiefWardenTestMixin, CreateView):
    template_name = 'officials/official-register-form.html'
    model = Worker
    form_class = WorkerForm
    success_url = reverse_lazy('officials:workers_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Register Staff'
        return context

class WorkerUpdateView(ChiefWardenTestMixin, LoginRequiredMixin, UpdateView):
    template_name = 'officials/official-register-form.html'
    model = Worker
    form_class = WorkerForm
    success_url = reverse_lazy('officials:workers_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Staff Details'
        return context

class WorkerDeleteView(ChiefWardenTestMixin, LoginRequiredMixin, DeleteView):
    model = Worker
    success_url = reverse_lazy('officials:workers_list')

class ComplaintListView(OfficialTestMixin, LoginRequiredMixin, ListView):
    model = Complaint
    template_name = 'officials/complaint_list.html'

    def get_queryset(self):
        return self.request.user.official.related_complaints(pending=False)

class MedicalIssueListView(OfficialTestMixin, LoginRequiredMixin, ListView):
    model = Complaint
    template_name = 'officials/medical_issue_list.html'

    def get_queryset(self):
        return self.request.user.official.related_medical_issues(pending=False)
