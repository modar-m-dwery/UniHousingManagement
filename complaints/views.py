from django.urls import reverse
from .models import Complaint, MedicalIssue
from institute.models import Student
from django.http.response import Http404
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import MedicalIssueUpdationForm
from complaints.forms import ComplaintUpdationForm
import re


class ComplaintDetailView(LoginRequiredMixin, DetailView):
    template_name = 'complaints/show.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # print(self.request.user)
        # print(self.object.user.entity_type)
        # print(self.object.complainee.roomdetail.block.short_name)
        # print(self.object.complainee.roomdetail.room)
        # print(self.object.user.official.block.name)
        # print(self.object.complainee.phone)
        # print(self.object.complainee.email)
        # print(self.request.user.student)
        # اذا كان المستخدم الذي يطلب عرض صفحة تفاصيل الشكوى طالب
        # وايضا اذا كان المستخدم الذي قدم الشكوى لا يساوي الطالب الذي انشاها
        if self.request.user.is_student and (self.object.entity() != self.request.user.student): 
            raise Http404()
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_edit'] = self.object.can_edit(self.request.user)
        if self.model == Complaint:
            # # عند التمرير الى فورم نستخدم انستانس انا من الموديل فهو
            context['form'] = ComplaintUpdationForm(instance=self.object)
        else:
            context['form'] = MedicalIssueUpdationForm(instance=self.object)
        return context


class ComplaintCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'complaints/new.html'
    
    def get_success_message(self, cleaned_data):
        return '{} created successfully!'.format(self.model.__name__)

    def get_success_url(self):
        return self.request.user.home_url()

    def form_valid(self, form):
        form.instance.user = self.request.user

        if self.model == Complaint:
            form.instance.complainee = form.cleaned_data.get('complainee_id') and Student.objects.get(regd_no = form.cleaned_data.get('complainee_id'))
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # يستخدم سطر الكود الذي قدمته وظيفة re.sub من الوحدة النمطية re لإدخال مسافات بين الأحرف الكبيرة في سلسلة
        #  يتم ذلك عادةً لتحويل سلسلة حالة الجمل أو حالة باسكال إلى تنسيق أكثر قابلية للقراءة.
        # =[a-z])[A-Z]  يتطابق هذا الجزء مع أي حرف كبيريسبقه مباشرة حرف صغير
        # (?<!\A) هو بحث خلفي سلبي في التعبير العادي. يتم استخدامه للتأكد من أن النمط لا يسبقه بداية السلسلة (\ A)
        """
            الإدخال: "HelloWorld"
            الإخراج: "Hello World"
        """

        # a = "aHmaD dWERY"
        # c = "Hmad DWERY"
        # b = "abOOalII"
        
        # model_label = re.sub(r'((?<=[a-z]))',r' \1',a) # a Hm a D d WERY
        # model_label = re.sub(r'((?<=[a-z])[A-Z])',r' \1',a) # a Hma D d WERY بس يكون حرف كبير وقبلو فقط حرف صغير بيعمل فراغ قبل
        # model_label = re.sub(r'((?<=[a-z]))',r' \1',b) # a b OOa l II
        # model_label = re.sub(r'((?<=[a-z])[A-Z])',r' \1',b) # ab OOal II
        # model_label = re.sub(r'([A-Z](?<=[a-z]))',r' \1',b) # abOOalII

        # model_label = re.sub(r'((?<!\A))',r' \1',a) # a H m a D d W E R Y 
        # model_label = re.sub(r'((?<!\A)[A-Z])',r' \1',a) # a Hma D d W E R Y 
        # model_label = re.sub(r'((?<!\A)[A-Z])',r' \1',b) # ab O Oal I I 
        # model_label = re.sub(r'((?<!\A)[A-Z])',r' \1',c) # Hmad D W E R Y عندما يجد حرف كبير فينظر هل ماقبله بداية جملة ,وبالتالي يحدث التطابق عندما ياتي حرف كبير وماقبله ليس بدايه جملة فبالتالي يقوم على ترك فراغ ورائه

        # model_label = re.sub(r'((?=[a-z]))',r' \1',a) # aH m aD dWERY يجب ان يكون الحرف الحالي صغير حتى يترك فراغ

        # model_label = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))',r' \0',a) # a ma d ERY

        model_label = re.sub(
        r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))',
        r' \1',
        self.model.__name__
        )
        context['form_title'] = 'Register {}'.format(model_label)
        context['object_name'] = model_label
        # print(context['object_name'])
        return context


class ComplaintUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    def get_success_message(self, cleaned_data):
        # print(self.get_object())
        # print(self.get_object().model_name())
        return '{} updated successfully!'.format(self.get_object().model_name())

    def get_success_url(self):
        # return self.request.user.home_url()
        # print(self.model.__name__)
        # It takes a view name or a URL pattern and returns the corresponding URL for that view or pattern.
        # complaints: This is the namespace of the app
        # {}_detail': This is a format string with curly braces {} to which the model name will be inserted
        # self.get_object(): This seems to be a method that retrieves the object (Complaint instance) associated with the view.
        return reverse('complaints:{}_detail'.format((self.model.__name__).lower()), args=[self.get_object().pk])


class ComplaintDeleteView(LoginRequiredMixin, DeleteView):

    def get_success_url(self):
        return self.request.user.home_url()