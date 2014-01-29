from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError 
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.template import Context, loader
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import User
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm

from django import  forms
from django.forms import ModelForm
from django.template import loader, RequestContext
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.core.xheaders import populate_xheaders
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.loading import get_model
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import render_to_response

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger,InvalidPage

from django import  forms 
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm

from models import *
from countries.models import *


global_popup = None
sess_uname = ''

'''SCHOOL DASHBOARD'''
def dashboard(request):
        try:
	   currentUser = SchoolUsers.objects.get(username=request.user.username)
           school = currentUser.School.schoolName
        except  SchoolUsers.DoesNotExist:
              return HttpResponseRedirect('/beige')
              
	return render_to_response('school/dashboard.html', {'school':school,'request':request.path,'user': request.user})



'''STUDENT SEARCH'''
def stud_search(request,term):
        currentUser = SchoolUsers.objects.get(username=request.user.username)
        school = currentUser.School.schoolName
        student_ = ""
        student_trans =""
        
	if request.GET.get('q','') != '':
			term = request.GET.get('q','')
                        try:
	       		      student_ = Students.objects.get(studentID=term)   
                              student_trans = BeigeTransaction.objects.filter(studentID__studentID = term)
                        except Students.DoesNotExist:
                                return HttpResponseRedirect('/beige/school/records/')
                        
	                return render_to_response('school/search_result.html',{'student_trans':student_trans,'school':school,'student_':student_,'request':request.path,'user':request.user})
        else:
                        errors ="No Match"
                        return render_to_response('school/records.html',{'school':school,'errors':errors,'request':request.path,'user':request.user})


'''STUDENT RECORDS'''
def student_records(request):
	#if request.user.username == '':
	#	return HttpResponseRedirect('/beige')
	currentUser = SchoolUsers.objects.get(username=request.user.username)
        school = currentUser.School.schoolName
	return render_to_response('school/records.html', {'school':school,'request':request.path,'user': request.user})

#class RegisterForm(UserCreationForm):
#	class Meta:
#        	model = User
#        	exclude=['activation_key','key_expires']
#        	fields = ('username', 'first_name','last_name', 'email',)


class RegisterForm1(ModelForm):
	class Meta:
		model = BeigeSchool
		exclude = ['datecreated','programmes','schoolName','postalAddress','phoneNumber','schoolType','location','dateupdated','schoolID']
        	fields  = ()


#class RegisterForm2(ModelForm):
#	class Meta:
#		model = Beige
#		exclude = ['datecreated','dateupdated','schoolID']
#       	fields  = ('schoolName','schoolName','postalAddress','phoneNumber','location','schoolType','programmes',)




def save(self, commit=True):
        form = RegisterForm1()
        for item in self.programme:
            form.programme.add(item)
       
       
        if commit:
            form.save()
        return form

'''SCHOOL REGISTERATION'''
@csrf_exempt
def school_reg(request):
	
    #galore=""
    #us_n = ""
    #p_k = ""
    #superuser=""
    #try:
    	#if request.session["galore"] == "modal":
		#us_n = request.session["us_n"]
		#p_k = request.session["p_k"] 
		#galore = "modal"
		#request.session["galore"] = ""
		#request.session["us_n"] = ""
                #request.session["p_k"] = ""

	#except KeyError:
	#request.session["galore"] = ""

    #form = RegisterForm(request.POST)
    #if request.user.username == '':
	#	return HttpResponseRedirect('/beige/login')
    form1 = RegisterForm1(request.POST)
    #print request.user.is_superuser
    #print 3
    prog   = Programme.objects.all()
    if request.method == 'POST':
       
       print request.user.is_superuser
       if form1.is_valid():
            #form1.save()
            #new_user = form.save();
            #new_user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            #login(request, new_user)
            #salt = sha.new(str(random.random())).hexdigest()[:5]
            #activation_key = sha.new(salt+new_user.username).hexdigest()
            #key_expires = datetime.datetime.today() + datetime.timedelta(2)
            worker = BeigeSchool()
            #sch_prog  = Programme(form1.cleaned_data['programme'])
            #worker.schoolName = form1.cleaned_data["schoolName"]
            #worker.schoolID    = 
           
            #get_program = Programme.objects.filter(name =request.POST['prog1'])
            worker.schoolName  = request.POST['schName']
            worker.postalAddress = request.POST['postAddress']
	    worker.phoneNumber =  request.POST['mobile']
            worker.location = request.POST['loc']
            worker.schoolType = request.POST['type']
            #print form1.cleaned_data['programmes']
           # get_programmes  =  Programme.objects.filter(name = form1.cleaned_data['programmes'] )
	    #worker.programmes = get_programmes
           
            worker.save()
	    #form1.username = "gggg"
	    #form1.username = form.cleaned_data["username"]
	    #form1.lastname = form.cleaned_data["last_name"]
	    #form1.firstname = form.cleaned_data["first_name"]
	    #form1.email = form.cleaned_data["email"]
            #form1.save()
            #request.session["galore"] = "modal"
	    #galore = "on"
	    #request.session["us_n"] = worker.username
            #request.session["p_k"] = new_user.pk
	    #p_k="on"
	    #us_n = "on"
	    return HttpResponseRedirect('/beige/add_school_user')
    else:
            #if us_n !="" and request.user.is_superuser:
		#superuser = "Yes"
		pass
		

    return render_to_response("beige/schoolreg.html", {'request':request.path,'prog':prog,'form1' : form1,
						      'user':request.user})



class RegisterForm2(ModelForm):
	class Meta:
		model = SchoolUsers
		exclude=['School','mobile_number',]
		fields = ()


class SchUserForm(UserCreationForm):
	class Meta:
		model = User
	       	exclude=['activation_key','key_expires', 'first_name','last_name','email',]
        	fields = ('username',)




def save(self, commit=True):
	
       
	user = super(SchUserForm, self).save(commit=False)
		#first_name, last_name = self.cleaned_data["fullname"].split()


	if commit:
                 #user.is_staff = True
		 user.save()
	return user




'''ADDING SCHOOL USER'''
@csrf_exempt
def adduser_sch(request):
	#if request.user.username == '':
	#	return HttpResponseRedirect('/beige/login')
	form = RegisterForm2(request.POST)
        form1 = SchUserForm(request.POST)
        schools = BeigeSchool.objects.all()
	if request.method == 'POST':
       
	       if form.is_valid() and form1.is_valid(): 
	            #form1.first_name = request.POST['first_name']
		    new_user = form1.save();
		    new_user = authenticate(username=request.POST['username'],is_staff = True ,first_name = request.POST['first_name'],password=request.POST['password1'])
		  
		    authUser = User.objects.get(username=request.POST['username'])
		    authUser.username = request.POST['username']
		    authUser.first_name = request.POST['first_name']
		    authUser.last_name = request.POST['last_name']
		    authUser.email     = request.POST['email']
		    #authUser.is_staff = True
		    #authUser.password = request.POST['password1']
		    authUser.save()
		    #login(request, new_user)
		    #salt = sha.new(str(random.random())).hexdigest()[:5]
		    #activation_key = sha.new(salt+new_user.username).hexdigest()
		    #key_expires = datetime.datetime.today() + datetime.timedelta(2)
		    schuser = SchoolUsers()
		    get_school = BeigeSchool.objects.get(schoolName=request.POST['sch'])
		    schuser.School=get_school
		    schuser.mobile_number = request.POST['mobile']
		    
		    schuser.username=request.POST['username']
		    schuser.first_name=request.POST['first_name']
		    schuser.last_name=request.POST['last_name']
		    schuser.email=request.POST['email']
		    #schuser.mobile_number=form1.cleaned_data["mobile_number"]
		    schuser.save()
		    print 4
		    return HttpResponseRedirect('/beige/beige/dashboard/')
	       else:
		    pass 
	return render_to_response("beige/adduser.html", {'request':request.path,'schools':schools,'form' : form,'form1' : form1,'user':request.user})

# add beige users views
class beigeUserForm(ModelForm):
	class Meta:
		model = BeigeUser
		exclude=['added_by','last_updated_by','date_added','date_updated','branch','username','last_name','email','mobile_number',]
		fields = ()


class beigeUserForm(UserCreationForm):
	class Meta:
		model = User
	       	exclude=['activation_key','key_expires', 'first_name','last_name','email',]
        	fields = ('username',)




def save(self, commit=True):
	
       
	user = super(beigeUserForm, self).save(commit=False)
		#first_name, last_name = self.cleaned_data["fullname"].split()


	if commit:
                 #user.is_staff = True
		 user.save()
	return user


'''ADDING BEIGE USER'''
@csrf_exempt
def adduser_beige(request):
	#if request.user.username == '':
	#	return HttpResponseRedirect('/beige/login')
	form = beigeUserForm(request.POST)
        form1 = beigeUserForm(request.POST)
        branch = Branch.objects.all()
	if request.method == 'POST':
       
	       if form.is_valid() and form1.is_valid():
                    form1.save()
		    #new_user = form1.save();
		    #new_user = authenticate(username=request.POST['username'],is_staff = True ,first_name = request.POST['first_name'],password=request.POST['password1'])
		  
		    authUser = User.objects.get(username=request.POST['username'])
		    #new_user.username = request.POST['username']
		    authUser.first_name = request.POST['first_name']
		    authUser.last_name = request.POST['last_name']
		    authUser.email     = request.POST['email']
		    #authUser.is_staff = True
                    authUser.save()
		    #authUser.password = request.POST['password1']
		    #authUser.save()
		    #login(request, new_user)
		    #salt = sha.new(str(random.random())).hexdigest()[:5]
		    #activation_key = sha.new(salt+new_user.username).hexdigest()
		    #key_expires = datetime.datetime.today() + datetime.timedelta(2)
		    beige_user = BeigeUser()
		    get_branch = Branch.objects.get(branch_name=request.POST['branch'])
		    beige_user.branch=get_branch
		    beige_user.mobile_number = request.POST['mobile']
		    
		    beige_user.username=request.POST['username']
		    beige_user.first_name=request.POST['first_name']
		    beige_user.last_name=request.POST['last_name']
		    beige_user.email=request.POST['email']
                    beige_user.added_by = request.user.username
                    beige_user.last_updated_by = request.user.username
		    #schuser.mobile_number=form1.cleaned_data["mobile_number"]
		    beige_user.save()
		    print 4
		    return HttpResponseRedirect('/beige/beige/dashboard/')
	       else:
		    pass 
	return render_to_response("beige/add_beige_user.html", {'request':request.path,'branch':branch,'form' : form,'form1' : form1,'user':request.user})

'''BIEGE DASHBOARD'''
def beige_dashboard(request):
	#if request.user.username == '':
		#return HttpResponseRedirect('/beige/login')
        if request.user.is_superuser != True:
		try:
         		 currentUser_biege = BeigeUser.objects.get(username=request.user.username)
                         if currentUser_biege !=None:
                              	schools = BeigeSchool.objects.all()
				paginator = Paginator(schools, 10)
				page = request.GET.get('page')
    				try:
            				schools = paginator.page(page)
        			except PageNotAnInteger:
        			# If page is not an integer, deliver first page.
            				schools = paginator.page(1)
        			except EmptyPage:
        			# If page is out of range (e.g. 9999), deliver last page of results.
            				schools = paginator.page(paginator.num_pages)
				#schools = BeigeSchool.objects.all()
                                return render_to_response('beige/dashboard.html', {'schools':schools,'request':request.path,'user': request.user})

                except BeigeUser.DoesNotExist:
                                 return HttpResponseRedirect('/beige/login')
                         
        		

        else:
               	schools = BeigeSchool.objects.all()
		paginator = Paginator(schools, 10)
		page = request.GET.get('page')
    		try:
            		schools = paginator.page(page)
        	except PageNotAnInteger:
        			# If page is not an integer, deliver first page.
            		schools = paginator.page(1)
        	except EmptyPage:
        	# If page is out of range (e.g. 9999), deliver last page of results.
            		schools = paginator.page(paginator.num_pages)
				#schools = BeigeSchool.objects.all()
                  
                return render_to_response('beige/dashboard.html', {'schools':schools,'request':request.path,'user': request.user})
         
	
'''PAYMENT'''
def beige_payment(request):
	#if request.user.username == '':
	#	return HttpResponseRedirect('/beige/login')
	#currentUser = SchoolUsers.objects.get(username1=request.user.username)
        #school = currentUser.School.schoolName
	return render_to_response('beige/payment.html', {'request':request.path,'user': request.user})


class student_reg(ModelForm):
	class Meta:
		model = Students
		exclude=['studentID','surname','gender','programme','Nationality','contact_Of_Guardian','mobile_number','email','residential_address','schoolID','date_added','date_updated','dateOfBirth','age',]
		fields = ()



'''REGISTER STUDENT'''
@csrf_exempt
def register(request):
        #if request.user.username == '':
	#	return HttpResponseRedirect('/beige')
        currentUser = SchoolUsers.objects.get(username=request.user.username)
        school = currentUser.School.schoolName
        courses =  Programme.objects.filter(program = currentUser.School)
        #course = None
        student_form  = student_reg(request.POST)
	#student = Students()
	#errors = []
	if request.method =='POST':
		if student_form.is_valid():
                     
                     #student_form.save() 
                     reg_student = Students()
                     
                    # course  = Programme.objects.all()
                     counT   = Country.objects.get(iso =request.POST['count'] )
                     reg_student.schoolID = currentUser.School
                     reg_student.surname  = request.POST['surname'] 
                     reg_student.othername = request.POST['othername']
                    # reg_student.contact_Of_Guardian = request.POST['guardian']
                     reg_student.email     = request.POST['email']
                     reg_student.gender    = request.POST['sex']
                     #reg_student.dateOfBirth  = student_form.cleaned_data["dateOfBirth"]
                     reg_student.dateOfBirth = request.POST['dob']
                     reg_student.mobile_number = request.POST['mobile']
                     #counT = request.POST['count']
                     print counT.iso
                     reg_student.Nationality = counT
                     #reg_student.programme  = request.POST['prog']
                     reg_student.residential_address  = request.POST['address']
                     print currentUser.School
		     print reg_student.schoolID
                     reg_student.save()
                    
                     
                     return HttpResponseRedirect('/beige/school/dashboard/')
                else:
                    pass
        return render_to_response('school/register.html', {'student_form':student_form,'request':request.path,'courses':courses,'school':school,'user': request.user})


	





class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '    Enter your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '    Enter your password'}))

'''SCHOOL LOGIN'''
@csrf_exempt
def do_login(request):
       # if request.user.username == '':
		#return HttpResponseRedirect('/beige')
	empty_cred = '' #empty login credential variable
	disabled_accMsg = ''
	invalidMsg = ''
	sess_data = ''
        already_logged_in=''#william made changes to your code here...had errors to added this to work
	if request.user.username != '':
		already_logged_in = 'You are already logged in.'
        
	if request.method == 'POST':
   	        uname = request.POST['username']	
		pword = request.POST['password']
		if uname == '' or pword == '':
			empty_cred = 'Username or password field cannot be empty!'
		else:
			user = authenticate(username=uname, password=pword)
			if user is not None:
				if user.is_active:
					login(request, user)
					#request.session["uname_sess"] = uname
					return HttpResponseRedirect('school/dashboard')
			
				##redirect
				else:
					disabled_accMsg = "Sorry, your account has been disabled. Contact the administrator."
				
				##return a disabled account msg
			else:
				invalidMsg = "Username or Password is invalid!"
			
			
	else:
		form = LoginForm()
	form = LoginForm()
	return render_to_response('signin/do_login.html', {
	'form': form,'request':request.path,
	'logged_in': request.user.is_authenticated(),
	'disabled_accMsg': disabled_accMsg,
	'invalidMsg': invalidMsg,
        'empty_cred':empty_cred,
        'already_logged_in': already_logged_in,
        'user': request.user
    })




'''BIEGE LOGIN'''
@csrf_exempt
def beige_login(request):
	
	empty_cred = '' #empty login credential variable
	disabled_accMsg = ''
	invalidMsg = ''
	sess_data = ''
        already_logged_in=''#william made changes to your code here...had errors to added this to work
	#if request.user.username != '':
		#already_logged_in = 'You are already logged in.'
		#return HttpResponseRedirect('/beige/beige/dashboard')
	
	if request.method == 'POST':
   	        uname = request.POST['username']	
		pword = request.POST['password']
		if uname == '' or pword == '':
			empty_cred = 'Username or password field cannot be empty!'
		else:
			user = authenticate(username=uname, password=pword)
			if user is not None:
				if user.is_active:
					login(request, user)
					#request.session["uname_sess"] = uname
					return HttpResponseRedirect('/beige/beige/dashboard')
			
				##redirect
				else:
					disabled_accMsg = "Sorry, your account has been disabled. Contact the administrator."
				
				##return a disabled account msg
			else:
				invalidMsg = "Username or Password is invalid!"
			
			
	else:
		form = LoginForm()
	form = LoginForm()
	return render_to_response('beige/do_login.html', {
	'form': form,'request':request.path,
	'logged_in': request.user.is_authenticated(),
	'disabled_accMsg': disabled_accMsg,
	'invalidMsg': invalidMsg,
        'empty_cred':empty_cred,
        'already_logged_in': already_logged_in,
        'user': request.user
    })


'''STUDENT SEARCH'''     
def student_search(request,term):
	if request.user.username == '':
		return HttpResponseRedirect('/beige/login')
        student_ = ""
        iterm =''
        schools = BeigeSchool.objects.all()
        school_= request.GET.get('school','')
	if request.GET.get('school','') != '' or request.GET.get('q','') != '':
                        get_school = request.GET.get('school','')
			term = request.GET.get('q','')
                        request.session['item']= str(get_school)
                        #print get_school
                        print term
                        try:
				#Students.objects.get(studentID=term)|
	       			student_ = Students.objects.filter(schoolID__schoolName = get_school) 
                                students = Students.objects.filter(studentID=term)
                                
                                for s in students:
                                      if s != '':
					  if get_school != "":
		                                  if s.schoolID.schoolName == get_school:
		                                      student_ = students 
		                                  else:
		                                       return HttpResponseRedirect('/beige/payment/') 
                                          else:
                                              student_ = students    
 				#student_trans = BeigeTransaction.objects.filter(studentID__studentID = term) 
                                paginator = Paginator(student_, 10)
      				page      = request.GET.get('page')
                                nstudent = student_
                        except Students.DoesNotExist:
                               return HttpResponseRedirect('/beige/payment/')
       	else:
                       		iterm = request.session['item']      
                       		nstudent   = Students.objects.filter(schoolID__schoolName = iterm) 
		       		paginator = Paginator(nstudent, 10)
				page = request.GET.get('page')
				student_= nstudent
       	try:
            	        	student_ = paginator.page(page)
       	except PageNotAnInteger:
    				student_ = paginator.page(1)
       	except EmptyPage:
        	# If page is out of range (e.g. 9999), deliver last page of results.
        			student_ = paginator.page(paginator.num_pages)




       	return render_to_response('beige/results_students.html',{'request':request.path,'iterm':iterm,'school_':school_,'schools':schools,'student_':student_,'user':request.user})
       
             	


class TransForm(ModelForm):
	class Meta:
		model = BeigeTransaction
		exclude=['studentID','amount','feesType','tellerID','transactionID','form','otherFeesType',]
		fields = ()

'''STUDENT DETAILS'''
@csrf_exempt
def student_detail(request, id, showDetails=False):
	if request.user.username == '':
		return HttpResponseRedirect('/beige/login')
      	student_        = Students.objects.get(pk=id)
      	form = TransForm(request.POST)
      	
      	try:
        	fees = Fees_category_school.objects.filter(School=student_.schoolID,status = True)
        	fees_all = FeesCategory.objects.all()
        except Fees_category_school.DoesNotExist:
                pass
        popup =""
        amount_error =''
	getFee = ""
	getAmt = ""
	get_Teller = ''
	get_Student = ''
	newpay = None
	is_allowed = ''
	try:
	    if request.session["newpay"] != None:
		newpay = request.session["newpay"]
		request.session["newpay"] = None
            #if request.session['error'] != '':
            #error = request.session["error"]
                #request.session['error'] = ''
            if request.session["get_fee"] != "":
		getFee = request.session["get_fee"]
		#request.session["get_fee"] = ""
	    if request.session["amt"] != "":
		getAmt = request.session["amt"]
		#request.session["amt"] = ""
    	    if request.session["modal"] == 'on':
		popup = "modal"		
	        request.session["modal"]=""
	    if request.session['get_teller'] !='':
	       get_Teller =request.session['get_teller']
	       #request.session['get_teller'] = ''
	    if request.session['get_student'] != '':
	       get_Student = request.session['get_student'] 
	       #request.session['get_student']  = ''
	    
        except KeyError:
		request.session["modal"] = ""
		request.session["get_fee"] = ""
		request.session["amt"] = ""
		request.session["newpay"] = None
	try:
		get_is_allowed = BeigeUser.objects.get(username=request.user.username)
	except BeigeUser.DoesNotExist:
		is_allowed = "no"
		
	if request.method == 'POST':
		if request.POST.get("preConfirm") == "preConfirm":
			if form.is_valid():
                        #form.save()
				newpay = BeigeTransaction()
				
                        	try:
                             		get_fee = FeesCategory.objects.get(name=request.POST['fee'])
			     		request.session["get_fee"] = get_fee	
                       		except MultiValueDictKeyError:
                              		return HttpResponseRedirect('/beige/st_details/'+str(student_.pk)+'/True/')
                       		if request.POST['amt'] == '':
                              		amount_error = 'on'
                              		return HttpResponseRedirect('/beige/st_details/'+str(student_.pk)+'/True/')
				newpay.amount = request.POST['amt']
				try:
					newpay.tellerID = BeigeUser.objects.get(username=request.user.username)
					request.session['get_teller'] = newpay.tellerID
				except BeigeUser.DoesNotExist:
				        
				        request.session['get_teller'] = request.user.username 
				newpay.feesType = get_fee
                        	request.session["get_fee"] = get_fee
                        	print request.session["get_fee"]
			        request.session["amt"] = request.POST['amt']
		        	#newpay.otherFeesType = form.cleaned_data['fessType']
			        #newpay.form = forms.cleaned_data['form']
                                print student_.studentID
                                try:
                                        if request.POST['paid'] == '':
                                           	request.session['paidby'] = 'Self'
                                        else:
                                		request.session['paidby'] = request.POST['paid']
                                except KeyError:
                                        request.session['paidby'] = 'Self'
			        newpay.studentID = student_
			        request.session['get_student'] =newpay.studentID
			        #newpay.transactionID = forms.cleaned_data['transactionID']
			        #request.session["newpay"] = newpay
                       		request.session["modal"] = 'on' 
				#newpay.save()
				print "galore"
				return HttpResponseRedirect('/beige/st_details/'+str(student_.pk)+'/True/')
			else:
				return HttpResponseRedirect('/beige/st_details/'+str(student_.pk)+'/True/')
		elif request.POST.get("Confirm") == "Confirm":
		        newpay  = BeigeTransaction()
		        print request.session["get_fee"]
		        newpay.amount= request.session["amt"]
		        try:
		        	newpay.tellerID =  BeigeUser.objects.get(username=request.user.username)
		        	print 1
		        except BeigeUser.DoesNotExist:
		                return HttpResponseRedirect('/beige/st_details/'+str(student_.pk)+'/True/')
		        newpay.feesType=getFee
		        newpay.studentID= get_Student
		        newpay.payment_by = request.session['paidby']
			newpay.save()
		        print "galore galore galore"
			return HttpResponseRedirect('/beige/std_details/'+str(student_.pk)+'/True/')
        return render_to_response('beige/make_payment.html',{'popup':popup,'amount_error':amount_error,'request':request.path,'fees_all':fees_all,'is_allowed':is_allowed,'getFee':getFee,'getAmt':getAmt,'fees':fees,'form':form,'student_':student_,'user':request.user})


def payment(request):
        schools = BeigeSchool.objects.all()
        
	return render_to_response("beige/payment.html",{'schools':schools,'request':request.path,'user':request.user})







'''SCHOOL DETAILS'''
def school_detail(request, id, showDetails=False):
      if request.user.username == '':
		return HttpResponseRedirect('/beige/login')
      if request.user.username == '' and request.user.is_superuser == False:
      		return HttpResponseRedirect('/')
      
      school= BeigeSchool.objects.get(pk=id)
      request.session["sch"] = school
      students 		= Students.objects.filter(schoolID=school)
      trans    		= BeigeTransaction.objects.filter(studentID__schoolID=school).order_by('-date_added')[:10]
      get_schoolFees_setup = Fees_category_school.objects.filter(School=school,status = True)
      trans_latest 	= BeigeTransaction.objects.filter(studentID__schoolID=school)
      amt = 0.0
      get_amt =[]
      for amt in trans_latest:
           get_amt.append(amt.amount) 
      for amt in get_amt:
          amt += amt
      print amt
      paginator 	= Paginator(students, 10)
      page 		= request.GET.get('page')
      try:
            students = paginator.page(page)
      except PageNotAnInteger:
        			# If page is not an integer, deliver first page.
            students = paginator.page(1)
      except EmptyPage:
        	# If page is out of range (e.g. 9999), deliver last page of results.
            students = paginator.page(paginator.num_pages)
      iterm=''		#schools = BeigeSchool.objects.all()
      return render_to_response('beige/school_details.html',
      				{'school':school, 'iterm':iterm,'trans_latest':trans_latest,
				'students':students,'trans':trans,'amt':amt,
      				'user':request.user})

'''STUDENT SEARCH AT BIEGE'''
def student_search_beige(request,term):
	if request.user.username == '':
		return HttpResponseRedirect('/beige/login')
        get_school = ""
        student_ = ""
        iterm =''
	if request.GET.get('q','') != '':
			term = request.GET.get('q','')
                        request.session['item']= str(term)
                        try:   
				get_school = request.session["sch"]
	       			student_ = Students.objects.filter(schoolID = get_school,studentID__icontains=term)|Students.objects.filter(schoolID= get_school,surname__icontains=term)|Students.objects.filter(schoolID = get_school,othername__icontains=term)
                                nstudent_= student_
	       			paginator = Paginator(student_, 10)
		        	page = request.GET.get('page')
                                term =""
                        except Students.DoesNotExist:
                               return HttpResponseRedirect('/beige/school_details/'+str(get_school.pk)+'/True/')
        else:
                get_school = request.session["sch"]
                print request.session['item']
                iterm = request.session['item']
		nstudent_ = Students.objects.filter(schoolID = get_school,studentID__icontains=iterm)|Students.objects.filter(schoolID= get_school,surname__icontains=iterm)|Students.objects.filter(schoolID = get_school,othername__icontains=iterm)
	       	paginator = Paginator(nstudent_, 10)
		page = request.GET.get('page')
		student_= nstudent_
	try:
            	student_ = paginator.page(page)
      	except PageNotAnInteger:
    		student_ = paginator.page(1)
        except EmptyPage:
        	# If page is out of range (e.g. 9999), deliver last page of results.
        	student_ = paginator.page(paginator.num_pages)
        #iterm = ''
        #request.session['item'] = ''
	return render_to_response('beige/search_result_beige.html',{'request':request.path,'get_school':get_school,'nstudent_':nstudent_,'iterm':iterm,'student_':student_,'user':request.user})
        
	
'''PAYMENT DETIALS'''
def payment_detail(request,id, showDetails=False):
	popup = ''
	this_transaction =''
        if request.user.username == '':
		return HttpResponseRedirect('/beige/login')
	try:
		if request.session['mod'] =='on':
		    popup = 'modal'
		    request.session['mod'] = '' 
		    this_transaction = request.session['std']
		    request.session['std'] = ''
		    
	except KeyError:
      		request.session["mod"] = ''
        student_ = Students.objects.get(pk = id)
        student_trans = BeigeTransaction.objects.filter(studentID=student_).order_by('-date_added')[:5]
        paginator = Paginator(student_trans, 10)
	page = request.GET.get('page')
	try:
            	student_trans = paginator.page(page)
      	except PageNotAnInteger:
    		student_trans = paginator.page(1)
        except EmptyPage:
        	# If page is out of range (e.g. 9999), deliver last page of results.
        	student_trans = paginator.page(paginator.num_pages)
      
	return render_to_response("beige/search_result.html",{'popup':popup,'student_':student_,'student_trans':student_trans,'this_transaction':this_transaction,'request':request.path,'user':request.user})
	
                		
def print_trans(request,id, showDetails=False):
     request.session['mod'] = 'on'
     student_trans = BeigeTransaction.objects.get(pk = id)
     request.session['std'] = student_trans
     student = Students.objects.get(studentID=student_trans.studentID.studentID)
     return HttpResponseRedirect('/beige/std_details/'+str(student.pk)+'/True/')


	
    

# BEIGE CHANGE PASSWORD
class ChangPassForm(PasswordChangeForm):
 
	class Meta:
		model = User
		#exclude=['activation_key','key_expires']
		fields = ()


'''CHANGE PASSWORD'''
def password_change(request,
                    template_name='beige/changepass.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    current_app=None, extra_context=None):
    '''
    if post_change_redirect is None:
        post_change_redirect = reverse('django.contrib.auth.views.password_change_done')
    '''
    if request.user.username == '':
		return HttpResponseRedirect('/beige/login')
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('beige/changedpass.html',{'user':request.user})
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)







#SCHOOL CHANGE PASSWORD
class ChangPassForm1(PasswordChangeForm):
 
	class Meta:
		model = User
		#exclude=['activation_key','key_expires']
		fields = ()


'''CHANGE PASSWORD'''
def school_password_change(request,
                    template_name='school/changepass.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    current_app=None, extra_context=None):
    '''
    if post_change_redirect is None:
        post_change_redirect = reverse('django.contrib.auth.views.password_change_done')
    '''
    if request.user.username == '':
		return HttpResponseRedirect('/beige')
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('school/changedpass.html',{'user':request.user})
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)





#LOGOUT
@csrf_exempt
def do_logout(request):
	if request.user.username == '' or request.user.is_active == False:
		request.user.username = ''
		request.session["sess_uname"] = ''
		return HttpResponseRedirect('/beige/login')
	try:
    		if request.user.username != '':
			logout(request)
			request.session["sess_uname"] = ''
			request.user.username == ''
			return HttpResponseRedirect('/beige/login')
    
		else:
			
			return HttpResponseRedirect('/beige/login')
		

        except KeyError:
		logout(request)
		request.session["sess_uname"] = ''
		request.user.username == ''
		return HttpResponseRedirect('/beige/login')


#excel upload


class ImportExcelForm(forms.Form):
    file  = forms.FileField(label= "Choose excel to upload") 
    
def test_flowcell(request):
    c = RequestContext(request, {'other_context':'details here'})
    if request.method == 'POST': # If the form has been submitted...
        form = ImportExcelForm(request.POST,  request.FILES) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            excel_parser= ExcelParser()
            success, log  = excel_parser.read_excel(request.FILES['file'] )
            if success:
                return redirect(reverse('admin:index') + "pages/flowcell_good/") ## redirects to aliquot page ordered by the most recent
            else:
                errors = '* Problem with flowcell * <br><br>log details below:<br>' + "<br>".join(log)
                c['errors'] = mark_safe(errors)
        else:
            c['errors'] = form.errors 
    else:
        form = ImportExcelForm() # An unbound form
    c['form'] = form
    return render_to_response('school/file_upload.html')  

