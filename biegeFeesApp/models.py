from django.contrib import admin
from django.db import models
from countries.models import Country

from django.utils.timezone import now
from datetime import date,time
import datetime,random, sha, hashlib
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
# Create your models here.


class Programme(models.Model):
	name = models.CharField(max_length=20,help_text ="Programme Name")
	date_added = models.DateTimeField(auto_now_add=True)
      	date_updated = models.DateTimeField(auto_now=True)
	def __unicode__(self):
              return "%s" %(self.name)
        


class BeigeSchool(models.Model):
	schoolID = models.CharField(max_length=10,blank=False,null=False)
	schoolName = models.CharField(max_length=30,blank=False,null=False)
	postalAddress = models.TextField(blank=False,null=False)
	phoneNumber = models.CharField(max_length=15,blank=False,null=False)
	location = models.CharField(max_length=30,blank=False,null=False)
	schoolType =  models.CharField(max_length=7, choices = (("Private", "Private"), 
                                                    ("Public", "Public")
                                                   ))
        programmes = models.ManyToManyField(Programme, related_name = "program")
	date_added=models.DateTimeField(auto_now_add=True,blank=True,null=True)
     	date_updated=models.DateTimeField(auto_now=True,blank=True,null=True)

	def school_ID(self):
		id_gen = random.randint(10,40)
               	id_gen1 = random.randint(50,90)
               	id_gen2 = random.randint(30,80)     
               	self.schoolID = "%s%s%s%s" %(self.schoolName[:4].upper(),id_gen,id_gen1,id_gen2)
                return self.schoolID
                
        class Meta:
                verbose_name = "School"
                verbose_name_plural ="Schools" 

	def __unicode__(self):
              return "%s-%s" %(self.schoolID,self.schoolName)


	def save(self,*args,**kwargs):
                self.school_ID()
		super(BeigeSchool,self).save(*args, **kwargs)
                return True


	def Number_of_Student(self):
		return "%s" %(self.students_set.count())

	def Number_of_users(self):
		return "%s" %(self.schoolusers_set.count())


class Branch(models.Model):
      branch_name = models.CharField(max_length = 40,blank=False,null=False)
      address   = models.TextField(blank=True,null=True)
      tel       = models.TextField(help_text= "separate by commas")
      added_by   = models.CharField(max_length = 50,blank=True, null = True)
      date_added = models.DateTimeField(auto_now_add=True)
      date_updated = models.DateTimeField(auto_now=True)

      class Meta:
                verbose_name = "Branch"
                verbose_name_plural ="Branches"

      def Number_of_users(self):
		return "%s" %(self.beigeuser_set.count())

      def __unicode__(self):
              return "%s" %(self.branch_name)


	


class BeigeUser(models.Model):
        branch= models.ForeignKey(Branch,blank=False,null=False)
        username =  models.CharField(unique =  True, max_length = 50,blank = True,null = True)
	first_name = models.CharField(max_length = 50,blank = True,null = True)
	last_name = models.CharField(max_length = 50,blank = True,null = True)
	email = models.EmailField(max_length=50, unique=True,blank=True,null=True)
	mobile_number = models.CharField(unique = True, max_length = 50,blank = True,null = True)
        added_by   = models.CharField(max_length = 50,blank=True, null = True)
        last_updated_by = models.CharField(max_length = 50,blank=True, null = True)
	date_added = models.DateTimeField(auto_now_add=True)
        date_updated = models.DateTimeField(auto_now=True)
        
	class Meta:
                verbose_name = "BeigeUser"
                verbose_name_plural ="BeigeUsers"

        def __unicode__(self):
              return "%s" %(self.username)

class Students(models.Model):
      studentID = models.CharField(max_length=10,blank=True,null=True)
      schoolID = models.ForeignKey(BeigeSchool,blank=False,null=False)
      surname	 = models.CharField(max_length=20,blank=True,null=True)
      othername = models.CharField(max_length=20,blank=True,null=True)
      email = models.EmailField(max_length=20,unique=True,blank=True,null=True)
      mobile_number = models.CharField(max_length=10,blank=True,null=True)
      gender = models.CharField(max_length=6, choices = (('Male', 'Male'), 
                                                    ('Female', 'Female')
                                                  ))
     # form   = models.CharField(max_length= 5,blank = True, null = True)
      dateOfBirth  = models.DateField(null= True, blank = True)
      age          = models.PositiveIntegerField(blank = True, null = True,help_text = "Generated from date of birth")
      programme = models.CharField(max_length=20,blank=True,null=True)							
      Nationality =  models.ForeignKey(Country,default = "GH")
      residential_address = models.TextField(max_length=100,null= True, blank = True)
      contact_Of_Guardian = models.TextField("Contact-N.O.K",help_text ="Please enter contact details of Next of Kin",max_length = 100,blank =True,null = True)
      date_added = models.DateTimeField(auto_now_add=True)
      date_updated = models.DateTimeField(auto_now=True)
      
      def fullnameC(self):
              return "%s %s" %(self.surname,self.othername)

      def student_ID(self):
                #print self.studentID
                if self.studentID == None:
			id_gen = random.randint(10,40)
                	id_gen1 = random.randint(50,90)
                	id_gen2 = random.randint(30,80)     
                	self.studentID = "%s%s%s%s" %(self.schoolID.schoolName[:4].upper(),id_gen,id_gen1,id_gen2)
                else:
                     return self.studentID
                 
           

      def __unicode__(self):
              return '%s-%s %s' %(self.studentID,self.surname,self.othername)
        
        


      def Age(self):
                
		if self.dateOfBirth:
	                 min_allowed_dob = datetime.datetime(1900,01,01)
	         	 max_allowed_dob = datetime.datetime.now()
			 if int(self.dateOfBirth.strftime("%G")) >= int( min_allowed_dob.strftime("%G") ) and int(self.dateOfBirth.strftime("%G")) <= int(max_allowed_dob.strftime("%G")):
               			 self.age  = "%s" %(int(max_allowed_dob.strftime("%G"))-  int(self.dateOfBirth.strftime("%G")))
               			 return "%s" %(self.age)
                             
			 else:
			 	return "Invalid Date"
		elif self.age and int(self.age[0:3])<=120: 
	        	self.dateOfBirth = None
		        return True
                 
	
	
      def save(self,*args,**kwargs):
                self.student_ID()
                #self.Age()
		super(Students,self).save(*args, **kwargs)
                
                return True
      class Meta:
                verbose_name = "Student"
                verbose_name_plural ="Students"


class FeesCategory(models.Model):
	name = models.CharField(max_length = 20)
	date_added = models.DateTimeField(auto_now_add=True)
        date_updated = models.DateTimeField(auto_now=True)	
	def __unicode__(self):
              return "%s" %(self.name)
   

	class Meta:
                verbose_name = "Fees Category"
                verbose_name_plural ="Fees Categories"


class SchoolUsers(models.Model):
	School = models.ForeignKey(BeigeSchool,blank=False,null=False)
        username =  models.CharField(unique =  True, max_length = 50,blank = True,null = True)
	first_name = models.CharField(max_length = 50,blank = True,null = True)
	last_name = models.CharField(max_length = 50,blank = True,null = True)
	email = models.EmailField(max_length=50, unique=True,blank=True,null=True)
	mobile_number = models.CharField(unique = True, max_length = 50,blank = True,null = True)
	date_added = models.DateTimeField(auto_now_add=True)
        date_updated = models.DateTimeField(auto_now=True)

    
        

        def __unicode__(self):
		return self.username
     

        class Meta:
                verbose_name = "School User"
                verbose_name_plural ="School Users"

	
class BeigeTransaction(models.Model):
	transactionID = models.CharField(max_length = 15, unique = True)
	studentID = models.ForeignKey(Students,blank=False,null=False)
	tellerID = models.CharField(max_length = 10)
	form = models.CharField(max_length=6, choices = (("FORM 1", "FORM 1"), 
                                                    ("FORM 2", "FORM 2"),
						    ("FORM 3", "FORM 3"),
						    ("FORM 4", "FORM 4")
                                                   ))

	feesType = models.ForeignKey(FeesCategory,blank=False,null=False)
	otherFeesType = models.CharField(max_length=20,blank=True, null=True, default=None,help_text ="Enter Other FeesType if applicable")
	amount = models.FloatField('Amount(GHS)',null = False, default = 0.0)
	date_added = models.DateTimeField(auto_now_add=True)
        date_updated = models.DateTimeField(auto_now=True)		
	

        def school(self):
            return self.studentID.schoolID

	def transaction_ID(self):
			id_gen = random.randint(100,400)
                	id_gen1 = random.randint(500,900)
                	id_gen2 = random.randint(300,800)     
                	self.transactionID = "%s%s%s%s%s" %('BEI',id_gen,id_gen1,id_gen2,'TXN')
			return self.transactionID
                
           

	def __unicode__(self):
              return "%s-%s" %(self.transactionID,self.tellerID)
        
        def save(self,*args,**kwargs):
                self.transaction_ID()
                #self.Age()
		super(BeigeTransaction,self).save(*args, **kwargs)
                return True



class StudentInline(admin.TabularInline):
	model = Students
	extra = 1

	
class BeigeUserAdmin(admin.ModelAdmin):
	list_display = ('username','first_name','last_name','email','mobile_number','branch','added_by','last_updated_by','date_added','date_updated',)
	ordering = ['-date_added']
        list_filter = ('branch__branch_name',)
        search_fields = ('username','mobile_number',)
        readonly_fields = ('added_by','last_updated_by',)
        obj = BeigeUser()
        def save_model(self, request,obj,form,change):
             obj.last_updated_by = request.user.username
             if  obj.added_by == "":
                        obj.added_by = request.user.username
             obj.save()




class BeigeBranchAdmin(admin.ModelAdmin):
       list_display = ('branch_name','tel','Number_of_users','added_by','date_added','date_updated',)
       ordering = ['-date_added']
       list_filter = ('date_added','added_by',)
       search_fields = ('name',)
       readonly_fields = ('added_by',)
       obj = Branch()
       def save_model(self, request,obj,form,change):
             if  obj.added_by == "":
                 obj.added_by= request.user.username
             obj.save()
class SchoolUserAdmin(admin.ModelAdmin):
	list_display = ('username','first_name','last_name','email','School','date_added','date_updated',)
	ordering = ['-date_added']





class ProgrammeAdmin(admin.ModelAdmin):
       
        list_display =('name','date_added','date_updated',)
	list_filter = ('name',)
	search_fields = ('name',)
	
	#inlines = [TransactionInline]
	ordering = ('-date_added',)
        date_hierarchy    = 'date_added'
        



class BeigeSchoolAdmin(admin.ModelAdmin):
       
        list_display =('schoolID','schoolName','postalAddress','phoneNumber','location','schoolType','Number_of_Student','Number_of_users','date_added','date_updated',)
	list_filter = ('schoolName','schoolType')
	search_fields = ('schoolID','schoolName','location','schoolType',)
	
	inlines = [StudentInline]
	ordering = ('-date_added',)

        #fieldsets = ( (None, {'fields':('schoolID','schoolName','programmes','postalAddress','phoneNumber','location','schoolType')}),)

        readonly_fields       = ('schoolID',)
        date_hierarchy    = 'date_added'
        list_per_page = 50




class StudentsAdmin(admin.ModelAdmin):
       
        list_display =('studentID','schoolID','surname','othername','gender','Age','email','mobile_number','programme','Nationality','residential_address','date_added','date_updated')
	list_filter = ('gender','programme')
	search_fields = ('studentID','^schoolID__schoolID','surname','othername','gender','email','mobile_number')
	
	#inlines = [TransactionInline]
	ordering = ('-date_added',)

        fieldsets = ( (None, {'fields':('studentID','schoolID','surname','othername','gender','dateOfBirth','email','mobile_number','age','programme','Nationality','residential_address','contact_Of_Guardian')}),)

        readonly_fields       = ('studentID','age',)
        date_hierarchy    = 'date_added'
        list_per_page = 50



class FeesCategoryAdmin(admin.ModelAdmin):
       
        list_display =('name','date_added','date_updated',)
	list_filter = ('name',)
	search_fields = ('name',)
	
	#inlines = [TransactionInline]
	ordering = ('-date_added',)
        date_hierarchy    = 'date_added'




class BeigeTransactionAdmin(admin.ModelAdmin):
       
        list_display =('transactionID','studentID','school','tellerID','feesType','amount','date_added','date_updated')
	list_filter = ('studentID__schoolID',)
	search_fields = ('transactionID','^studentID__studentID','tellerID','form','feesType','otherFeesType')
	
	#inlines = [TransactionInline]
	ordering = ('-date_added',)

        fieldsets = ( (None, {'fields':('transactionID','studentID','tellerID','form','feesType','otherFeesType','amount')}),)

        readonly_fields   = ('transactionID','studentID','tellerID')
        date_hierarchy    = 'date_added'
        list_per_page = 50

admin.site.register(BeigeUser,BeigeUserAdmin)
admin.site.register(Branch,BeigeBranchAdmin)
admin.site.register(SchoolUsers,SchoolUserAdmin)
admin.site.register(Programme,ProgrammeAdmin)
admin.site.register(BeigeSchool,BeigeSchoolAdmin)
admin.site.register(Students,StudentsAdmin)
admin.site.register(FeesCategory,FeesCategoryAdmin)
admin.site.register(BeigeTransaction,BeigeTransactionAdmin)

