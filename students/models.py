from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from institute.constants import FLOOR_OPTIONS

# تفاصيل الغرفة المخصصة للطالب
class RoomDetail(models.Model):
    student = models.OneToOneField('institute.Student', on_delete=models.CASCADE, null=False)
    # يمثل الكتلة المرتبطة بالغرفة
    block = models.ForeignKey('institute.Block', on_delete=models.SET_NULL, null=True, blank=True)
    room_no = models.IntegerField(null=True, blank=True)
    #  وظيفة مضمنة تطبق وظيفة محددة على كل عنصر من عناصر قابلة للتكرار وتعيد مكررًا ينتج عنه النتائج
    floor = models.CharField(max_length=10, choices=list(map(lambda floor: (floor, floor), FLOOR_OPTIONS)), null=True, blank=True)

    def __str__(self):
        if self.floor and self.room_no:
            # يمثل self.block_id المفتاح الأساسي لمثيل Block المرتبط في علاقة المفتاح الخارجي.
            block = self.block_id
            if self.floor == 'Fourth':
                floor = self.floor[:2]
            else:
                floor = self.floor[0]
            return "{regd_no}<{block}: {floor}-{room}>".format(
                regd_no = self.student, 
                block = block,
                floor = floor,
                room = self.room_no
            )
        else:
            return "{}-".format(self.student)

    # ويتم استخدامه للتحقق مما إذا كانت الغرفة قد وصلت إلى أقصى سعتها بناءً على room_no المتوفرة و floor
    def clean(self):
        # يستبعد هذا المثيل الحالي (self) من مجموعة الاستعلام
        # تمت كتابته بهذه الطريقة من اي الذهاب اولا الى البلوك ثم تحديد هذه الغرفة بالتحديد منه لكي نجلب معلومات البلوك الموجوده فيه
        # الغرض من هذا الاستبعاد هو ضمان عدم مراعاة الغرفة الحالية التي يتم التحقق من صحتها عند حساب عدد مثيلات الغرفة الأخرى في نفس الكتلة مع نفس room_no والأرضية
        if self.block.roomdetail_set.exclude(pk=self.pk).filter(room_no=self.room_no, floor=self.floor).count() >= self.block.per_room_capacity():
            raise ValidationError("Room filled to maximum capacity.")
        
        if self.floor not in self.block.available_floors():
            raise ValidationError("Floor not available.")

        student = self.student
        block = self.block
        def valid_gender(student, block):
            return student.gender == block.gender
        
        # اذا كان الطالب سنة اولى بيقعد بغرف من اربع اشخاص
        def valid_year(student, block):
            return  ((student.year == 1 and block.room_type == '4S') or \
                    ((student.year == 2 or student.year == 3) and block.room_type == '2S') or \
                    (student.year == 4 and block.room_type == '1S'))

        if block and not valid_gender(student, block):
            raise ValidationError("{} Student cannot be placed in {} block!".format(student.gender, block.gender))
        if block and not valid_year(student, block):
            raise ValidationError("Year: {} Student cannot be placed in {} block!".format(student.year, block.room_type))
    
    def room(self):
        if self.floor and self.room_no:
            if self.floor == 'Fourth':
                floor = self.floor[:2]
            else:
                floor = self.floor[0]
            return "{}-{}".format(floor, self.room_no)
        else:
            return "-"


#  نموذج الحضور سجلات حضور الطالب.
class Attendance(models.Model):
    OPTIONS = (
        ('Present','Present'),
        ('Absent','Absent')
    )
    student = models.OneToOneField('institute.Student', on_delete=models.CASCADE, null=False)
    # التواريخ التي يتم فيها وضع علامة على الطالب غائبًا
    present_dates = models.TextField(
        null=True,
        blank=True,
        help_text="Dates format 'MM DD YYYY'. For example: '2 22 2022'."
    )
    # حالة الحضور للتاريخ المحدد
    absent_dates = models.TextField(
        null=True,
        blank=True,
        help_text="Dates format 'MM DD YYYY'. For example: '2 22 2022'."
    )
    status = models.CharField(max_length=10, choices=OPTIONS, null=True, blank=True)

    def __str__(self):
        return str(self.student)

    #  يحدّث سجلات الحضور لتاريخ وحالة محددين
    def mark_attendance(self, date, status):
        # "حاضر" أو "غائب"
        # يتم تحديث التواريخ الغائبة عن طريق إزالة التاريخ من مجموعة التواريخ الغائبة.
        if status == 'present':
            # 1  "2023-07-20،2023-07-19،2023-07-18"
            # 2 لتقسيم سلسلة إلى قائمة بالتواريخ الفردية
            # 3  بعد ذلك تحويل قائمة التواريخ إلى مجموع سبب تحويلها إلى مجموعة هو إزالة أي تواريخ مكررة
            absent_dates = self.absent_dates and set(self.absent_dates.split(',')) or set()
            # بما ان حالة الشخص حاضر او موجود بالتالي يجب ازلة التاريخ المحدد من سجل الغياب
            absent_dates.discard(date)
            # تحويل التواريخ الغائبة المحدثة مرة أخرى إلى سلسلة وتخزينها في السمة 
            self.absent_dates = ','.join(absent_dates)
            if not self.present_dates: 
                self.present_dates = date
            else:
                self.present_dates = ','.join(set(self.present_dates.split(',') + [date]))
        elif status == 'absent':
            present_dates = self.present_dates and set(self.present_dates.split(',')) or set()
            present_dates.discard(date)
            self.present_dates = ','.join(present_dates)
            if not self.absent_dates: 
                self.absent_dates = date
            else:
                self.absent_dates = ','.join(set(self.absent_dates.split(',') + [date]))
        if timezone.now().date() == timezone.datetime.strptime(date, "%Y-%m-%d").date():
                self.status = status.title()

        self.save()


# نزهة أو إجازة يقدمه الطالب
class Outing(models.Model):
    # معلق , ممنوح , مرفوض
    PERMIT_OPTIONS = (
        ('Pending','Pending'),
        ('Granted', 'Granted'),
        ('Rejected', 'Rejected')
    )

    student = models.ForeignKey('institute.Student', on_delete=models.CASCADE, null=False)
    fromDate = models.DateTimeField(null=False)
    toDate = models.DateTimeField(null=False)
    purpose = models.CharField(max_length=150, null=False)
    permission = models.CharField(max_length=20, choices=PERMIT_OPTIONS, default='Pending', null=False)

    def is_upcoming(self):
        return self.fromDate > timezone.now()

    # إذا كان طلب الخروج قادمًا ولديه حالة إذن "معلق".
    # مشيرة إلى أن الخروج قابل للتحرير
    def is_editable(self):
        # للتحقق مما إذا كان الخروج قادمًا
        # يمثل حالة الإذن للنزهة المخزنة في حقل الإذن
        return self.is_upcoming() and self.permission == 'Pending'

    class Meta:
        ordering = ['-fromDate']


# نموذج المستند المستندات المرتبطة بالطالب
class Document(models.Model):
    student = models.OneToOneField('institute.Student', on_delete=models.CASCADE, null=False)
    application = models.FileField(null=True, blank=True)
    # وثيقة نموذج التعهد
    undertaking_form = models.FileField(null=True, blank=True)
    # الإيصال
    receipt = models.FileField(null=True, blank=True)
    # مستند الإفادة الخطية للباحث اليوم
    day_scholar_affidavit = models.FileField(null=True, blank=True)
    # مستند بطاقة Aadhar
    aadhar_card = models.FileField(null=True, blank=True)

    def __str__(self) -> str:
        return 'Document: {} - {}'.format(self.id, self.student.regd_no)


# تفاصيل رسوم الطالب
class FeeDetail(models.Model):
    student = models.OneToOneField('institute.Student', on_delete=models.CASCADE, null=False)
    has_paid = models.BooleanField(null=True, default=False)
    # المبلغ الذي يدفعه الطالب
    amount_paid = models.FloatField(null=True, blank=True,default=0)
    # اسم البنك
    bank = models.CharField(max_length=100,null=True, blank=True)
    # رقم challan
    challan_no = models.CharField(max_length=64,null=True, blank=True)
    # تاريخ الدفع
    dop = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return 'Bank Detail: {} - {}'.format(self.id, self.student.regd_no)