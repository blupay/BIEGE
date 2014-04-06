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
import datetime
from models import *
from countries.models import *
from django.core.mail import send_mail

global_popup = None
sess_uname = ''

'''SCHOOL DASHBOARD'''
def dashboard(request):
	if request.user.username == '':
		return HttpResponseRedirect('/beige/')
        try:
	   currentUser = SchoolUsers.objects.get(username=request.user.username)
           school = currentUser.School.schoolName
           students = Students.objects.filter(schoolID=currentUser.School)
           
        except  SchoolUsers.DoesNotExist:
              return HttpResponseRedirect('/beige/')
              
	return render_to_response('school/dashboard.html', {'school':school,'students':students,'request':request.path,'user': request.user})



'''STUDENT SEARCH'''
def stud_search_id(request,term):
        currentUser = SchoolUsers.objects.get(username=request.user.username)
        school = currentUser.School.schoolName
        student_ = ""
        student_trans =""
        
	if request.GET.get('q','') != '':
			term = request.GET.get('q','')
			print term
                        try:
	       		      student_ = Students.objects.get(studentID=term)   
                              student_trans = BeigeTransaction.objects.filter(studentID__studentID = term).order_by("-date_added")
                        except Students.DoesNotExist:
                                return HttpResponseRedirect('/beige/school/records/')
                        
	                return render_to_response('school/search_result.html',{'student_trans':student_trans,'school':school,'student_':student_,'request':request.path,'user':request.user})
        else:
                        errors ="No Match"
                        return render_to_response('school/records.html',{'school':school,'errors':errors,'request':request.path,'user':request.user})


def stud_search_surname(request,term):
	if request.user.username == '':
		return HttpResponseRedirect('/beige')
        currentUser = SchoolUsers.objects.get(username=request.user.username)
        school = currentUser.School.schoolName
        student_ = ""
        student_trans =""
        
	if request.GET.get('q','') != '':
			term = request.GET.get('q','')
			print term
                        try:
	       		      student_ = Students.objects.filter(surname__icontains=term)   
                              #student_trans = BeigeTransaction.objects.filter(studentID__studentID = term)
                        except Students.DoesNotExist:
                              pass
                        
	                return render_to_response('school/search_result_surname.html',{'school':school,'student_':student_,'request':request.path,'user':request.user})
       





'''STUDENT RECORDS'''
def student_records(request):
	if request.user.username == '':
		return HttpResponseRedirect('/beige/')
	currentUser = SchoolUsers.objects.get(username=request.user.username)
        school = currentUser.School.schoolName
	return render_to_response('school/records.html', {'school':school,'request':request.path,'user': request.user})

class RegisterForm1(ModelForm):
	class Meta:
		model = BeigeSchool
		exclude = ['datecreated','programmes','schoolName','postalAddress','phoneNumber','schoolType','location','dateupdated','schoolID']
        	fields  = ()

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
    pop =''
    sch =''
    if request.user.username == '':
		return HttpResponseRedirect('/beige/login/')
    try:
    	if request.session['pop']=='on':
                pop = 'on'
                sch = request.session['school']
                #request.session['school'] =''
                request.session['pop'] =''
    except KeyError:
           	request.session['pop'] =''
    if request.method == 'POST':
                
		try:
		        
		    	set_school = BeigeSchool()
		   
		        
		    	set_school.schoolName  = request.POST['schName']
		    	request.session['school'] = request.POST['schName']
		    	
		    	
		    	if request.POST['shortName'] =='':
		    		set_school.schoolName_short ='None'
		    	else:
		    	   	set_school.schoolName_short = request.POST['shortName']
		    	   	
		    	set_school.postalAddress = request.POST['postAddress']
		    	
		    	set_school.phoneNumber =  request.POST['mobile']
		    	
		    	set_school.tel_no   =  request.POST['Tel']
		    	
		    	set_school.email_add = request.POST['e-mail']
		    	
		    	set_school.location = request.POST['loc']
		    	
		    	set_school.schoolType = request.POST['type']
		    	
		   	set_school.save()
		   	request.session['pop']='on'
		   	
		   	return HttpResponseRedirect('/beige/school_reg/')
		except KeyError:
		       return HttpResponseRedirect('/beige/schiol_reg/')
		

    return render_to_response("beige/schoolreg.html", {'sch':sch,'pop':pop,'request':request.path,
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
	if request.user.username == '':
		return HttpResponseRedirect('/beige/login/')
	form = RegisterForm2(request.POST)
        form1 = SchUserForm(request.POST)
        schools = BeigeSchool.objects.all() 
        pi =''
        useR = ''
        password =''
        get_school = ''
        another_school=''
        try:
        	if request.session['school'] != '':
        		get_school = request.session['school']
			request.session['another_school'] = request.session['school']
        		print request.session['school']
        		request.session['school']= ''
        except KeyError:
        	request.session['school'] =''
        try:
		if request.session['pi']== 'on':
		   	pi = 'on'
		   	try: 
		   		useR = request.session['useR']
		   		password = request.session['pass']
		   	except MultiValueDictKeyError:
		   	       	request.session['useR'] =''
		   	       	request.session['pass'] =''
		   	
		        request.session['pi']= ''
		        
		        
		        
        except KeyError:
                request.session['pi']= '' 
                request.session['useR'] =''  
                request.session['pass'] =''  
        
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
		    request.session['pass'] = request.POST['password1']
		    authUser.save()
		    schuser = SchoolUsers()
		    if request.session['another_school'] !='':
		        print request.session['another_school']
		    	get_school = BeigeSchool.objects.get(schoolName=request.session['another_school'])
		    	schuser.School=get_school
			request.session['another_school'] =''
		    else:
			get_school = BeigeSchool.objects.get(schoolName=request.POST['sch'])
			schuser.School=get_school

		    schuser.mobile_number = request.POST['mobile']
		    schuser.username=request.POST['username']
		    schuser.first_name=request.POST['first_name']
		    schuser.last_name=request.POST['last_name']
		    schuser.email=request.POST['email']
		    schuser.active = True
		    request.session['useR'] = request.POST['username']
		    schuser.save()
		    request.session['pi']= 'on'
		    return HttpResponseRedirect('/beige/add_school_user/')
	       else:
		    pass 
	return render_to_response("beige/adduser.html", {'get_school':get_school ,'request':request.path,'password':password,'useR':useR,'pi':pi,'schools':schools,'form' : form,'form1' : form1,'user':request.user})

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
	if request.user.username == '':
		return HttpResponseRedirect('/beige/login/')
	form = beigeUserForm(request.POST)
        form1 = beigeUserForm(request.POST)
        branch = Branch.objects.all()
	#Variable initialization
        currentUser_biege = ''
        ping =''
        get_user =''
        try:
        	if request.session['ping'] =='on':
        	      ping = 'on'
        	      request.session['ping'] =''
        	if request.session['get_user']!='':
        	      get_user = request.session['get_user']
        	      
        except KeyError:
                request.session['ping'] =''
                request.session['get_user'] =''
                
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
		    request.session['get_user'] = authUser.username
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
                    beige_user.active = True
		    beige_user.category = request.POST['category']
		    request.session['ping'] ='on'
		    beige_user.save()
		    return HttpResponseRedirect('/beige/add_beige_user/')
	       else:
		    pass 
	return render_to_response("beige/add_beige_user.html", {'request':request.path,
								'ping':ping,
								'get_user':get_user,
								'currentUser_biege':currentUser_biege,
                                			        'beige_date':datetime.datetime.now,
								'branch':branch,'form' : form,
								'form1' : form1,'user':request.user})

'''BIEGE DASHBOARD'''
@csrf_exempt
def beige_dashboard(request):
	if request.user.username == '':
		return HttpResponseRedirect('/beige/login/')
	approval =''
	
	try:
	      if request.session['approved'] =='on':
	      		approval = 'on'
	      		request.session['approved'] =''
	except KeyError:
	       request.session['approved'] =''
		
        if request.user.is_staff != True:
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
				transaction = BeigeTransaction.objects.filter(tellerID__username=currentUser_biege.username) 
				# capture IP-Address of client request
				x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    				if x_forwarded_for:
        				ip = x_forwarded_for.split(',')[-1].strip()
    				else:
        				ip = request.META.get('REMOTE_ADDR')
    				#Branch tellers
				tellers     = BeigeUser.objects.filter(branch=currentUser_biege.branch,category ="Teller") 
				paginator = Paginator(tellers, 20)
				page = request.GET.get('page')
    				try:
            				tellers = paginator.page(page)
        			except PageNotAnInteger:
        			# If page is not an integer, deliver first page.
            				tellers = paginator.page(1)
        			except EmptyPage:
        			# If page is out of range (e.g. 9999), deliver last page of results.
            				tellers = paginator.page(paginator.num_pages)	
            			try:
            			      tellers_transactions = BeigeTransaction.objects.filter(tellerID__branch=currentUser_biege.branch,approval_status="PENDING").order_by('-date_added')[:5]		                
            			except BeigeTransaction.DoesNotExist:
            			        pass
            			if request.method =='POST':
            			         try:
            			                print request.POST['t']
            			         	get_transaction = BeigeTransaction.objects.get(pk=request.POST['t'])
            			         	get_transaction.approval_status ="APPROVED"
            			         	get_transaction.save()
            			         	request.session['approved']='on'
            			         	return HttpResponseRedirect('/beige/beige/dashboard/')
            			         except BeigeTransaction.DoesNotExist:
            			                pass
                                return render_to_response('beige/dashboard.html', {'currentUser_biege':currentUser_biege,
                                						  'beige_date':datetime.datetime.now,
                                						  
										  'transaction':transaction,'ip':ip,
										  'tellers':tellers,'approval':approval,
										  'tellers_transactions':tellers_transactions,
										  'schools':schools,
										  
										  'request':request.path,
										  'user': request.user})

                except BeigeUser.DoesNotExist:
                                 return HttpResponseRedirect('/beige/login')
                         
        		

        else:
 		currentUser_biege =None
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
                transaction = BeigeTransaction.objects.all()
                results =None  
                # get beige users
                beige_users = BeigeUser.objects.all()
                school_users = SchoolUsers.objects.all()
                try:
                	trans_today = BeigeTransaction.objects.filter(date_added__gte=date.today())
                	trans_today_approved = BeigeTransaction.objects.filter(date_added__gte=date.today(), approval_status="APPROVED")
                	trans_today_pending=BeigeTransaction.objects.filter(date_added__gte=date.today(), approval_status="PENDING")
                except BeigeTransaction.DoesNotExist:
                	pass
                return render_to_response('beige/dashboard.html', {'results':results,'currentUser_biege':currentUser_biege,
                			                   	   'beige_date':datetime.datetime.now,
                			                   	   'trans_today':trans_today,
                			                   	   'trans_today_approved':trans_today_approved,
                			                   	   'trans_today_pending':trans_today_pending,
                			                   	   'beige_users':beige_users,
                			                   	   'school_users':school_users,
                						   'transaction':transaction,'schools':schools,'request':request.path,'user': request.user})


def sch_search(request,term):
        if request.user.username == '':
		return HttpResponseRedirect('/beige')
	try:
        	currentUser_biege = BeigeUser.objects.get(username=request.user.username)
        except BeigeUser.DoesNotExist:
        	return HttpResponseRedirect('/beige/login')  
	if request.GET.get('q','') != '':
			term = request.GET.get('q','')
			print term
                        try:
	       		      results = BeigeSchool.objects.filter(schoolName__icontains=term)   
                              #student_trans = BeigeTransaction.objects.filter(studentID__studentID = term)
                        except BeigeSchool.DoesNotExist:
                              pass
          
   			return render_to_response('beige/dashboard.html', {'results': results,'currentUser_biege':currentUser_biege,
   									   'beige_date':datetime.datetime.now,
                						           'request':request.path,'user': request.user})

def monitor(request):
        tellers_transactions= BeigeTransaction.objects.filter(approval_status="PENDING").order_by("-date_added")[:5]
	return render_to_response('beige/approve.html', {'tellers_transactions': tellers_transactions},context_instance = RequestContext(request))


# search view-dropdown            
def search(request):
    if request.is_ajax():
        q = request.GET.get('q')
        if q is not None:            
            results = BeigeSchool.objects.filter(  
            	Q( schoolName__contains = q ) |
                Q( schoolName_short__contains = q ))          
            return render_to_response('beige/results.html', {'results': results},context_instance = RequestContext(request))
        
	
'''NOT IN USE AT THE MOMENT'''
def beige_payment(request):
	if request.user.username == '':
		return HttpResponseRedirect('/beige/login/')
	try:
        	currentUser_biege = BeigeUser.objects.get(username=request.user.username)
        except BeigeUser.DoesNotExist:
        	return HttpResponseRedirect('/beige/login/') 
	return render_to_response('beige/payment.html', {'currentUser_biege':currentUser_biege,
   							 'beige_date':datetime.datetime.now,
							 'request':request.path,'user': request.user})

'''BEIGE PAYMENT PAGE'''
def payment(request):
        schools = BeigeSchool.objects.all()
        try:
        	currentUser_biege = BeigeUser.objects.get(username=request.user.username)
        except BeigeUser.DoesNotExist:
        	return HttpResponseRedirect('/beige/login/') 
	return render_to_response("beige/payment.html",{'currentUser_biege':currentUser_biege,
   							 'beige_date':datetime.datetime.now,
   							 'schools':schools,'request':request.path,'user':request.user})

'''STUDENT SEARCH''' 
@csrf_exempt    
def student_search(request,term):
	if request.user.username == '':
		return HttpResponseRedirect('/beige/login/')
	try:
        	currentUser_biege = BeigeUser.objects.get(username=request.user.username)
        except BeigeUser.DoesNotExist:
        	return HttpResponseRedirect('/beige/login/') 
        get_students= None     
        wrong_input =''  
        result =''       
	if request.GET.get('q','') != '':
			term = request.GET.get('q','')
			result = str(term)
			request.session['term'] =term
			print term
			print 5
                        try:
				
	       			get_students = Students.objects.filter(studentID__icontains=term) 
                                paginator = Paginator(get_students, 50)
      				page      = request.GET.get('page')	
			except Students.DoesNotExist:
			       wrong_input ='on'
                               return HttpResponseRedirect('/beige/payment/')
        else:
        	try:
                	if request.session['term'] !='':
                        	term = request.session['term']
                                request.session['term'] =''
                except KeyError:
                       	request.session['term'] =''
                try:
		        get_students = Students.objects.filter(studentID__icontains=result) 
			paginator = Paginator(get_students, 50)
			page      = request.GET.get('page')    
		except Students.DoesNotExist:
			wrong_input ='on'
	        	return HttpResponseRedirect('/beige/payment/') 	
	try:
		get_students = paginator.page(page)
	except PageNotAnInteger:
	 	get_students= paginator.page(1)
	except EmptyPage:
		get_students= paginator.page(paginator.num_pages)	
       	return render_to_response('beige/payment.html',{'request':request.path,
       							'currentUser_biege':currentUser_biege,
       							'wrong_input':wrong_input,
   							'beige_date':datetime.datetime.now,
       							'get_students':get_students,
       							'user':request.user})
       
             	


class student_reg(ModelForm):
	class Meta:
		model = Students
		exclude=['studentID','surname','gender','programme','Nationality','contact_Of_Guardian','mobile_number','email','residential_address','schoolID','date_added','date_updated','dateOfBirth','age',]
		fields = ()

def fees_setup(request):
        currentUser = SchoolUsers.objects.get(username=request.user.username)
        school = currentUser.School.schoolName
        return render_to_response("school/fees_setup.html",{'school':school,'request':request.path,'user':request.user})


'''REGISTER STUDENT'''
@csrf_exempt
def register(request):
        if request.user.username == '':
		return HttpResponseRedirect('/beige/')
	pop = ''
	student =''
        currentUser = SchoolUsers.objects.get(username=request.user.username)
        school = currentUser.School.schoolName
        courses =  Programme.objects.filter(program = currentUser.School)
        try:
		if  request.session['mod'] != '':
		     pop = 'on'
		     request.session['mod'] =''
		     student = request.session['student']
        except KeyError:
               request.session['mod'] =''
	if request.method =='POST':
		
        	reg_student = Students()
          	counT   = Country.objects.get(iso =request.POST['count'] )
                reg_student.schoolID = currentUser.School
                reg_student.surname  = request.POST['surname'] 
                request.session['student'] = str (request.POST['surname']) +' '+ str(request.POST['othername'])
                reg_student.othername = request.POST['othername']
                reg_student.email     = request.POST['email']
                reg_student.gender    = request.POST['sex']
                if request.POST['dob'] != '':
                	reg_student.dateOfBirth = request.POST['dob']
                else:
                    	reg_student.dateOfBirth = None
                reg_student.mobile_number = request.POST['mobile']
                print counT.iso
                reg_student.Nationality = counT
                if request.POST['address'] != '': 
                	reg_student.residential_address  = request.POST['address']
                else: 
                        reg_student.residential_address = None
                
                reg_student.Guardian_name = request.POST['guardian']
                reg_student.mobile_guardian = request.POST['mobile_g']
                reg_student.email_of_guardian = request.POST['email_g'] 
               
                      
                reg_student.save()
                request.session['mod'] = 'on'
                
                return HttpResponseRedirect('/beige/school/register/')
                
                
        return render_to_response('school/register.html', {'pop':pop,'student':student,'request':request.path,'courses':courses,'school':school,'user': request.user})


	





class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '    Enter your username','required':'required','autocomplete':'off'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '    Enter your password','required':'required'}))

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
		print 1
   	        uname = request.POST['username']	
		pword = request.POST['password']
		if uname == '' or pword == '':
			print 2
			empty_cred = 'Username or password field cannot be empty!'
		else:
			user = authenticate(username=uname, password=pword)
			if user is not None:
				if user.is_active:
					login(request, user)
					print 3
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
        already_logged_in=''#changes to your code here...had errors to added this to work
	#if request.user.username != '':
		#already_logged_in = 'You are already logged in.'
		#return HttpResponseRedirect('/beige/beige/dashboard')
	wrong_attempt =''
	try:
		if request.session['wrong_attempt'] !='':
			wrong_attempt = request.session['wrong_attempt']
			request.session['wrong_attempt'] =''
	except KeyError:
		request.session['wrong_attempt'] =''
		 	
	if request.method == 'POST':
   	        uname = request.POST['username']	
		pword = request.POST['password']
		if uname == '' or pword == '':
			empty_cred = 'Username or password field cannot be empty!'
		else:
			user = authenticate(username=uname, password=pword)
			if user is not None:
				if user.is_active and user.is_superuser==False:
					login(request, user)
					try:
						bUser = BeigeUser.objects.get(username=uname)
						bUser.online_status = True
						bUser.save()
					except BeigeUser.DoesNotExist:
						pass
					#request.session["uname_sess"] = uname
					return HttpResponseRedirect('/beige/beige/dashboard')
			
				##redirect
				else:
					disabled_accMsg = "Sorry, no access. Contact the administrator."
				
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
        'empty_cred':empty_cred,'wrong_attempt':wrong_attempt,
        'already_logged_in': already_logged_in,
        'user': request.user
    })



class TransForm(ModelForm):
	class Meta:
		model = BeigeTransaction
		exclude=['studentID','amount','feesType','tellerID','transactionID','form','otherFeesType',]
		fields = ()

'''STUDENT DETAILS'''
@csrf_exempt
def student_detail(request, term, showDetails):
	if request.user.username == '':
		return HttpResponseRedirect('/beige/login/')
      	student_        = Students.objects.get(slug=term)
      	form = TransForm(request.POST)
      	try:
        	currentUser_biege = BeigeUser.objects.get(username=request.user.username)
        except BeigeUser.DoesNotExist:
        	return HttpResponseRedirect('/beige/login/') 
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
                              		return HttpResponseRedirect('/beige/st_details/'+str(student_.slug)+'/True/')
                       		if request.POST['amt'] == '':
                              		amount_error = 'on'
                              		return HttpResponseRedirect('/beige/st_details/'+str(student_.slug)+'/True/')
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
				request.session['color'] = 'on'
				print "galore"
				return HttpResponseRedirect('/beige/st_details/'+str(student_.slug)+'/True/')
			else:
				return HttpResponseRedirect('/beige/st_details/'+str(student_.slug)+'/True/')
		elif request.POST.get("Confirm") == "Confirm":
		        newpay  = BeigeTransaction()
		        print request.session["get_fee"]
		        newpay.amount= request.session["amt"]
		        try:
		        	newpay.tellerID =  BeigeUser.objects.get(username=request.user.username)
		        	print 1
		        except BeigeUser.DoesNotExist:
		                return HttpResponseRedirect('/beige/st_details/'+str(student_.slug)+'/True/')
		        newpay.feesType=getFee
		        newpay.studentID= get_Student
		        newpay.payment_by = request.session['paidby']
		        newpay.only_date=datetime.datetime.today().strftime("%Y-%m-%d")
		       
			newpay.save()
		        html_contenT = "Hello\n Your child"+" "+str(get_Student.surname)+" at"+" "+str(get_Student.schoolID.schoolName)+" "+"Has made payment of Fees at Beige Capital" 
                	try:
                       		send_mail('Contact',html_contenT,'get_Student.email_of_guardian',[str(get_Student.email_of_guardian)],fail_silently=True)
                	except KeyError:
                       		pass
		        
			return HttpResponseRedirect('/beige/std_details/'+str(student_.slug)+'/True/')
        return render_to_response('beige/make_payment.html',{'popup':popup,
                   					     'amount_error':amount_error,
      							     'request':request.path,
      							     'fees_all':fees_all,'is_allowed':is_allowed,
      							     'getFee':getFee,
      							     'getAmt':getAmt,
      							     'currentUser_biege':currentUser_biege,
   							     'beige_date':datetime.datetime.now,
      							     'fees':fees,
      							     'form':form,
      							     'student_':student_,
      							     'user':request.user})







'''SCHOOL DETAILS'''
@csrf_exempt
def school_detail(request,term,showDetails):
      if request.user.username == '':
		return HttpResponseRedirect('/beige/login/')
      if request.user.username == '' and request.user.is_staff == False:
      		return HttpResponseRedirect('/')
      try:
      		currentUser_biege = BeigeUser.objects.get(username=request.user.username)
      except currentUser_biege.DoesNotExist:
      		return HttpResponseRedirect('/beige/login/')
      try:
	      school= BeigeSchool.objects.get(slug=term)
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
      except BeigeSchool.DoesNotExist:
      		if request.user.username != '':
			try:
				bUser = BeigeUser.objects.get(username=request.user.username)
				bUser.online_status = False
				bUser.save()
			except BeigeUser.DoesNotExist:
				pass
			logout(request)
			request.session["sess_uname"] = ''
			request.user.username == ''
			request.session['wrong_attempt'] ='False Url!!'
			return HttpResponseRedirect('/beige/login/')
    
		else:
			
			return HttpResponseRedirect('/beige/login/')
      return render_to_response('beige/school_details.html',
      				{'school':school,'beige_date':datetime.datetime.now,
      				'iterm':iterm,'trans_latest':trans_latest,
				'students':students,'currentUser_biege':currentUser_biege, 
				'trans':trans,'amt':amt,
      				'user':request.user})

'''STUDENT SEARCH AT BIEGE'''
@csrf_exempt
def student_search_beige(request,term):
	if request.user.username == '':
		return HttpResponseRedirect('/beige/login')
        get_school = ""
        student_ = ""
        iterm =''
        try:
      		currentUser_biege = BeigeUser.objects.get(username=request.user.username)
      	except currentUser_biege.DoesNotExist:
      		pass
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
                               return HttpResponseRedirect('/beige/school_details/'+str(get_school.slug)+'/True/')
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
	return render_to_response('beige/search_result_beige.html',{'request':request.path,'get_school':get_school,
								    'nstudent_':nstudent_,'beige_date':datetime.datetime.now,
								    'iterm':iterm,
								    'currentUser_biege':currentUser_biege,
								    'student_':student_,
								    'user':request.user})
 
 
@csrf_exempt 
def walk_in (request):
        if request.user.username == '':
		return HttpResponseRedirect('/beige/login/')
        is_allowed = ''
	getAmt = ''   
	try:
        	currentUser_biege = BeigeUser.objects.get(username=request.user.username)
        except BeigeUser.DoesNotExist:
        	return HttpResponseRedirect('/beige/login/') 	
      	try:
      	        schools = BeigeSchool.objects.all()
        	fees_all = FeesCategory.objects.all()
        	try:
        		get_fee = FeesCategory.objects.get(name=request.POST['fee'])
        	except MultiValueDictKeyError:
        	         pass
        except Fees_category_school.DoesNotExist:
                pass
        pop = ''
        get_student = ''
        try:
        	get_student = request.session['get_student']
        	getAmt = request.session['amt']
        except KeyError:
        	request.session['get_student']= ''
        #print request.session['stid']
        try:
        	if request.session['vi'] =='on':
        		pop = 'on'
        		request.session['vi'] =''
        except KeyError:
               request.session['vi'] = ''
        	
	try:
		get_is_allowed = BeigeUser.objects.get(username=request.user.username)
	except BeigeUser.DoesNotExist:
		is_allowed = "no"
		
	if request.method == 'POST':
	       	if request.POST.get("preconfirm") == "preconfirm":
			student = Students()
			get_school = BeigeSchool.objects.get(schoolName = request.POST['school'])
			student.surname  = request.POST['surname']
			request.session['surname'] = request.POST['surname']
			
			student.othername = request.POST['othername']
			request.session['othername'] = request.POST['othername']
			
			student.studentID = request.POST['stid'].upper()
			request.session['stid'] = request.POST['stid'].upper()
			student.schoolID  = get_school
			request.session['school'] = get_school
			try:
				Students.objects.get(studentID = request.POST['stid'].upper()) 
			except Students.DoesNotExist:
			        student.save()
		      	print Students.objects.get(studentID = request.POST['stid'].upper()) 
			#newpay = BeigeTransaction()
			try:
				get_student = Students.objects.get(studentID = request.POST['stid'].upper())
				request.session['get_student'] = get_student
				#newpay.tellerID = BeigeUser.objects.get(username=request.user.username)
				#newpay.amount= request.POST['amt']
				request.session['amt'] = request.POST['amt']
				#newpay.studentID = get_student
				#newpay.payment_by = request.POST['paidby']
				request.session['paidby'] = request.POST['paidby']
				#newpay.feesType = get_fee
				#newpay.mobile = request.POST['mobile']
				request.session['mobile'] = request.POST['mobile']
				#newpay.save()
				request.session['vi'] = 'on'
				request.session['get_fees'] = get_fee
				request.method = ''
				return HttpResponseRedirect('/beige/walk_in/')
				
			except KeyError:
				return HttpResponseRedirect('/beige/walk_in/')
		elif request.POST.get("confirm") == "confirm":
			newpay = BeigeTransaction()
			print request.session['stid']
			print 34
			try:
				get_student = Students.objects.get(studentID = request.session['stid'].upper())
				print get_student
				print 0
				newpay.tellerID = BeigeUser.objects.get(username=request.user.username)
				print 1
				newpay.amount= request.session['amt']
				print 2
				newpay.studentID = get_student
				print 3
				newpay.payment_by = request.session['paidby']
				newpay.feesType = request.session['get_fees']
				newpay.mobile = request.session['mobile']
				newpay.approval_status = "PENDING"
				newpay.only_date=datetime.datetime.today().strftime("%Y-%m-%d")
				newpay.save()
				request.session['color'] ='on'
				return HttpResponseRedirect('/beige/std_details/'+str(get_student.slug)+'/True/')
				
			except Students.DoesNotExist:
				return HttpResponseRedirect('/beige/std_details/'+str(get_student.slug)+'/True/')
        return render_to_response('beige/walkIn.html',{'request':request.path,'schools':schools,'pop':pop,
        						'getAmt':getAmt,'get_student':get_student,
        						'fees_all':fees_all,'is_allowed':is_allowed,
        						'currentUser_biege':currentUser_biege,
        						'beige_date':datetime.datetime.now,
        						'user':request.user})
	      
	
'''PAYMENT DETIALS'''
@csrf_exempt
def payment_detail(request,term, showDetails):
	popup = ''
	color=''
	refresh =''
	this_transaction =''
	student_trans_dated=None
	from_date=''
	to_date=''
        if request.user.username == '':
		return HttpResponseRedirect('/beige/login')
	try:
      		currentUser_biege = BeigeUser.objects.get(username=request.user.username)
      	except currentUser_biege.DoesNotExist:
      		pass
	try:
		if request.session['mod'] =='on':
		    popup = 'modal'
		    request.session['mod'] = ''
		    
		    this_transaction = request.session['std']
		    request.session['std'] = ''
		if request.session['color'] =='on':
		   color = request.session['color']
		   request.session['color'] =''
	except KeyError:
      		request.session["mod"] = ''
      	try:
        	student_ = Students.objects.get(slug=term)
        except Students.DoesNotExist:
        	if request.user.username != '':
			try:
				bUser = BeigeUser.objects.get(username=request.user.username)
				bUser.online_status = False
				bUser.save()
			except BeigeUser.DoesNotExist:
				pass
			logout(request)
			request.session["sess_uname"] = ''
			request.user.username == ''
			request.session['wrong_attempt'] ='False Url!!'
			return HttpResponseRedirect('/beige/login/')
    
		else:
			
			return HttpResponseRedirect('/beige/login/')
        try:
		student_trans = BeigeTransaction.objects.filter(studentID=student_,tellerID__username=request.user).order_by('-date_added')
		paginator = Paginator(student_trans, 10)
		page = request.GET.get('page')
		try:
		    	student_trans = paginator.page(page)
	      	except PageNotAnInteger:
	    		student_trans = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			student_trans = paginator.page(paginator.num_pages)
        except BeigeTransaction.DoesNotExist:
			pass
        #get all transactions on students
        student_trans_all = BeigeTransaction.objects.filter(studentID=student_).order_by('-date_added')
        paginator = Paginator(student_trans_all, 10)
	page = request.GET.get('page')
	try:
            	student_trans_all = paginator.page(page)
      	except PageNotAnInteger:
    		student_trans_all = paginator.page(1)
        except EmptyPage:
        	# If page is out of range (e.g. 9999), deliver last page of results.
        	student_trans_all = paginator.page(paginator.num_pages)
        try:
        	if request.method =="POST":
        	        refresh ='on'
        	        try:
        	        	print request.POST['from_date']
        	        	print request.POST['to_date']
        	        	from_date = request.POST['from_date']
        	        	to_date =request.POST['to_date']
        	        except KeyError:
        	        	pass
        	        try:
        			student_trans_dated = BeigeTransaction.objects.filter(studentID=student_,tellerID__username=request.user,only_date__gte=request.POST['from_date'],only_date__lte=request.POST['to_date']).order_by('-date_added')
        
        		except BeigeTransaction.DoesNotExist:
        			pass
        except KeyError:
                pass
	return render_to_response('beige/search_result.html',{'popup':popup,
							'student_':student_,
							'student_trans':student_trans,
							'student_trans_all':student_trans_all,
							'refresh':refresh,
							'color':color,
							'from_date':from_date,
							'to_date':to_date,
							'beige_date':datetime.datetime.now,
							'currentUser_biege':currentUser_biege,
							'this_transaction':this_transaction,
							'student_trans_dated':student_trans_dated,
							'request':request.path,
							'user':request.user
							})
	
@csrf_exempt                		
def print_trans(request,term, showDetails):
     request.session['mod'] = 'on'
     print term
     try:
	     student_trans = BeigeTransaction.objects.get(slug = term)
	     request.session['std'] = student_trans
	     student = Students.objects.get(studentID=student_trans.studentID.studentID)
	     return HttpResponseRedirect('/beige/std_details/'+str(student.slug)+'/True/')
     except BeigeTransaction.DoesNotExist:
            if request.user.username != '':
			try:
				bUser = BeigeUser.objects.get(username=request.user.username)
				bUser.online_status = False
				bUser.save()
			except BeigeUser.DoesNotExist:
				pass
			logout(request)
			request.session["sess_uname"] = ''
			request.user.username == ''
			request.session['wrong_attempt'] ='False Url!!'
			return HttpResponseRedirect('/beige/login/')
    
	    else:
		        return HttpResponseRedirect('/beige/login/')
     
@csrf_exempt 
def teller_report(request):
        amtSum =0.0
        refresh=''
        trans_dated=None
        amtSumDated=0.0
        from_date=''
        to_date=''
	try:
      		currentUser_biege = BeigeUser.objects.get(username=request.user.username)
      	except currentUser_biege.DoesNotExist:
      		return HttpResponseRedirect('/beige/login/')
        today =date.today()
        
        report_today =  BeigeTransaction.objects.filter(tellerID__username=request.user.username,date_added__gte=today,approval_status="APPROVED")
        for amt in report_today:
                    amtSum += float(amt.amount)
        try:
        	if request.method =="POST":
        	        refresh ='on'
        	        try:
        	        	print request.POST['from_date']
        	        	print request.POST['to_date']
        	        	from_date = request.POST['from_date']
        	        	to_date =request.POST['to_date']
        	        except KeyError:
        	        	pass
        	        try:
        			trans_dated = BeigeTransaction.objects.filter(tellerID__username=request.user,only_date__gte=request.POST['from_date'],only_date__lte=request.POST['to_date'],approval_status="APPROVED").order_by('-date_added')
        			for amt in trans_dated:
                    			amtSumDated+= float(amt.amount)
        		except BeigeTransaction.DoesNotExist:
        			pass
        except KeyError:
                pass
	return render_to_response("beige/tellerReport.html",{'report_today':report_today,
							     'beige_date':datetime.datetime.now,
							     'amtSum':amtSum,'refresh':refresh,
							     'trans_dated':trans_dated,
							     'amtSumDated':amtSumDated,
							     'from_date':from_date,
							     'to_date':to_date,
							     'currentUser_biege':currentUser_biege,
							     'request':request.path,'user':request.user})
@csrf_exempt	
def teller_details(request,term, showDetails):
        request.session['teller_slug'] = term 
        get_trans =None
        get_teller =None
        amtSum =0.0
        refresh=''
        trans_dated=None
        amtSumDated=0.0
        from_date=''
        to_date=''
        try:
      		currentUser_biege = BeigeUser.objects.get(username=request.user.username)
      	except currentUser_biege.DoesNotExist:
      		return HttpResponseRedirect('/beige/login/')
      		
        try:
	      if request.session['teller_slug'] !='':
	             today =date.today()
	             try:
        	     		report_today =  BeigeTransaction.objects.filter(tellerID__slug=request.session['teller_slug'],date_added__gte=today,approval_status="APPROVED").order_by("-date_added")
	      	     		get_trans = BeigeTransaction.objects.filter(tellerID__slug = request.session['teller_slug']).order_by("-date_added")
	      	     		get_teller =  BeigeUser.objects.get(slug = request.session['teller_slug'])
	      	    
	      	    		print get_trans
	      	     except BeigeTransaction.DoesNotExist:
			     if request.user.username != '':
					try:
						bUser = BeigeUser.objects.get(username=request.user.username)
						bUser.online_status = False
						bUser.save()
					except BeigeUser.DoesNotExist:
						pass
					logout(request)
					request.session["sess_uname"] = ''
					request.user.username == ''
					request.session['wrong_attempt'] ='False Url!!'
					return HttpResponseRedirect('/beige/login/')
		    
			     else:
					return HttpResponseRedirect('/beige/login/')
		     except BeigeUser.DoesNotExist:
			     if request.user.username != '':
					try:
						bUser = BeigeUser.objects.get(username=request.user.username)
						bUser.online_status = False
						bUser.save()
					except BeigeUser.DoesNotExist:
						pass
					logout(request)
					request.session["sess_uname"] = ''
					request.user.username == ''
					request.session['wrong_attempt'] ='False Url!!'
					return HttpResponseRedirect('/beige/login/')
		    
			     else:
					return HttpResponseRedirect('/beige/login/')
		  
			      	       
	except KeyError:
	      request.session['teller_slug'] =''
	try:
        	if request.method =="POST":
        	        refresh ='on'
        	        try:
        	        	print request.POST['from_date']
        	        	print request.POST['to_date']
        	        	from_date = request.POST['from_date']
        	        	to_date =request.POST['to_date']
        	        except KeyError:
        	        	pass
        	        try:
        	                if request.session['teller_slug'] !='':
        				trans_dated = BeigeTransaction.objects.filter(tellerID__slug=request.session['teller_slug'],only_date__gte=request.POST['from_date'],only_date__lte=request.POST['to_date'],approval_status="APPROVED").order_by('-date_added')
        				for amt in trans_dated:
                    				amtSumDated+= float(amt.amount)
        		except KeyError:
        			pass
        except KeyError:
                pass
	return render_to_response("beige/tellerDetails.html",{'beige_date':datetime.datetime.now,
							     'refresh':refresh,
							     'from_date':from_date,
							     'trans_dated':trans_dated,
							     'to_date':to_date,
							     'get_trans':get_trans,
							     'get_teller':get_teller,
							     'report_today':report_today,
							     
							     'currentUser_biege':currentUser_biege,
							     'request':request.path,'user':request.user})
	

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
                    password_change_form=PasswordChangeForm,beige_date=datetime.datetime.now,
                    current_app=None, extra_context=None):
    '''
    if post_change_redirect is None:
        post_change_redirect = reverse('django.contrib.auth.views.password_change_done')
    '''
    currentUser_biege=None
    if request.user.username == '':
		return HttpResponseRedirect('/beige/login')
   	
    try:
      		currentUser_biege = BeigeUser.objects.get(username=request.user.username)
      		
    except currentUser_biege.DoesNotExist:
           	return HttpResponseRedirect('/beige/login/')
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('beige/changedpass.html',{'currentUser_biege':currentUser_biege,'beige_date':datetime.datetime.now,'user':request.user})
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





#LOGOUT-BEIGE
@csrf_exempt
def do_logout(request):
	if request.user.username == '' or request.user.is_active == False:
		request.user.username = ''
		request.session["sess_uname"] = ''
		return HttpResponseRedirect('/beige/login/')
	try:
    		if request.user.username != '':
			try:
				bUser = BeigeUser.objects.get(username=request.user.username)
				bUser.online_status = False
				bUser.save()
			except BeigeUser.DoesNotExist:
				pass
			logout(request)
			request.session["sess_uname"] = ''
			request.user.username == ''
			return HttpResponseRedirect('/beige/login/')
    
		else:
			
			return HttpResponseRedirect('/beige/login/')
		

        except KeyError:
		logout(request)
		request.session["sess_uname"] = ''
		request.user.username == ''
		return HttpResponseRedirect('/beige/login/')


#LOGOUT-SCHOOL
@csrf_exempt
def do_logouT(request):
	if request.user.username == '' or request.user.is_active == False:
		request.user.username = ''
		request.session["sess_uname"] = ''
		return HttpResponseRedirect('/beige/')
	try:
    		if request.user.username != '':
			logout(request)
			
			request.session["sess_uname"] = ''
			request.user.username == ''
			return HttpResponseRedirect('/beige/')
    
		else:
			
			return HttpResponseRedirect('/beige/')
		

        except KeyError:
		logout(request)
		request.session["sess_uname"] = ''
		request.user.username == ''
		return HttpResponseRedirect('/beige/')

