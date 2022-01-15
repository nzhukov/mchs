from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.fields.related import ForeignKey


class GDZS(models.Model):
    fullname = models.ForeignKey("CustomUser", on_delete=models.CASCADE, related_name="name", verbose_name="ФИО")
    value = models.BooleanField(null=True, blank=True, verbose_name="ГДЗс")
    possible = models.BooleanField(null=True, blank=True, verbose_name="Подлежит аттестации")
    why_not = models.ForeignKey("NoAttestation", on_delete=models.CASCADE, blank = True, null=True, verbose_name="Почему не подлежит аттестации")

    def __str__(self):
        if self.value == True:
            return "Да"
        else:
            return "Нет"

    class Meta:
        verbose_name_plural="ГДЗС"
        verbose_name="ГДЗС" 

class PassedApprovals(models.Model):
    fullname = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    result = models.BooleanField(blank=True, null=True, verbose_name="Аттестован")
    why = models.CharField(max_length=60, blank=True, null=True, verbose_name="Почему не прошел аттестацию")
    attdate = models.DateField(blank=True, null=True, verbose_name="Дата аттестации")
    profdate = models.DateField(blank=True, null=True, verbose_name="Дата профосмотра")
    approvalsname = models.ForeignKey("Approvals", on_delete=models.CASCADE, blank = True, null = True, verbose_name="Название аттестации")

    def __str__(self):
        return str(self.approvalsname)

    class Meta:
        verbose_name_plural="Аттестации"
        verbose_name="Аттестация" 
    

class Approvals(models.Model):
    value = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name_plural="Виды аттестации"
        verbose_name="Вид аттестации" 

class Post(models.Model):
    fullname = models.ForeignKey("CustomUser", on_delete=models.CASCADE, related_name='person', verbose_name="ФИО")
    value = models.CharField( max_length=30, verbose_name="Должность")
    rtp = models.BooleanField(db_column='RTP', blank=True, null=True, verbose_name="РТП")
    passdate = models.DateField(blank=True, null=True, verbose_name="Дата сдачи на пропуск")

    def __str__(self):
        return self.value

    class Meta:
        verbose_name_plural="Должности"
        verbose_name='Должность' 
    
class NoAttestation(models.Model):
    value = models.TextField(blank=True, null=True, verbose_name="Причина")

    def __str__(self):
        return self.value

    class Meta:
        verbose_name_plural="Причины неаттестации"
        verbose_name='Причина неаттестации' 

class Rank(models.Model):
    value = models.CharField(max_length=30, blank=True, null=True, verbose_name="Звание", unique=True)

    class Meta:
        db_table = 'rank'
        verbose_name = "Звание"
        verbose_name_plural = "Звания"

    def __str__(self):
        return self.value


class Rtp(models.Model):
    value = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'rtp'

class InitialTrainingPeriod(models.Model):
    fullname = models.ForeignKey("CustomUser", on_delete=models.CASCADE, verbose_name="ФИО")
    start = models.DateField(verbose_name="Начало первичной подготовки", null=True, blank=True)
    end = models.DateField(verbose_name="Конец первичной подготовки",  null=True, blank=True)

    class Meta:
        verbose_name = "Период первичной подготовки"
        verbose_name_plural = "Периоды первичной подготовки"

    def __str__(self):
        if self.start == None or self.end == None:
            return "Неполные данные"
        else:   
            return (str(self.start.strftime("%d.%m.%Y")) + " - " + str(self.end.strftime("%d.%m.%Y")))  # форматирование вывода временного отрезка


class MyUserManager(BaseUserManager):
    '''
    Класс, переопределяющий методы создания пользователей
    В данном случае регистрация и вход осуществляются по почте и паролю
    '''
    def create_user(self, email, password):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),  # приведение адреса к нижнему регистру
            fullname = email        # присвоение почты в качестве начального имени пользователя
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    '''
    Класс пользователя, для большей кастомизации наследуется от AbstractBaseUser, из-за чего необходимо 
    переопределять встроенные в иных классах поля и методы
    '''
    email=models.EmailField(max_length=64,verbose_name = "E-mail", unique=True)
    password=models.TextField(verbose_name='Пароль')
    fullname = models.CharField(max_length=50, blank=True, null=True, verbose_name="ФИО")
    gdzs = models.ForeignKey(GDZS, on_delete=models.SET_NULL,blank=True, null=True, verbose_name="ГДЗС") 
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Должность")
    rank = models.ForeignKey(Rank, on_delete=models.SET_NULL,  blank=True, null=True, verbose_name="Звание")
    bdate = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    approvals =  models.ForeignKey(PassedApprovals, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Аттестация")
    period = models.ForeignKey(InitialTrainingPeriod, on_delete=models.SET_NULL, null=True, blank = True, verbose_name="Период первичной подготовки")
    document = models.CharField(max_length=50, blank=True, null=True, verbose_name="Удостоверение")

    is_active = models.BooleanField(default = True)
    is_admin = models.BooleanField(default = False)

    class Meta:
        verbose_name_plural="Пользователи"
        verbose_name='Пользователь'
        ordering=['fullname']

    # переопределение встроенных методов

    def get_full_name(self):
        return self.fullname

    def get_short_name(self):
        return self.fullname

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):  # определяем что будет возвращать вызов объекта
        return self.fullname

    @property
    def is_staff(self):
        return self.is_admin

    USERNAME_FIELD = "email"    # указываем поле, которое считать именем пользователя, по умолчанию используется как логин
    REQUIRED_FIELDS = ['password']  # указываем поля, необходимые для регистрации

    objects = MyUserManager()   # указываем по каким правилам создавать новых пользователей