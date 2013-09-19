from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.forms.formsets import formset_factory, BaseFormSet
from django.core.context_processors import csrf

from app_auth.models import UserProfile, Student, Teacher
from app_essays.models import Essay, EssayResponse, GradingSystem, EssayForm, EssayComment, Grade, EssayResponseForm, EssayResponseGradeForm, EssayCommentForm
from app_classes.models import Class

from datetime import datetime
import operator, pycurl, urllib
import nltk

@login_required(redirect_field_name='', login_url='/')
def new_essay(request):
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	errors = 0;
	if request.method == 'POST':
		form = EssayForm(request.POST, request)
		form.fields['class_name'].queryset = Class.objects.filter(teacher = Teacher.objects.get(user_id = request.user.id))
		if form.is_valid():
			cd = form.cleaned_data
			data = form.save(commit=False)
			data.instructor = Teacher.objects.get(user_id = request.user.id)
			data.status = 1
			data.save()

			students = Class.objects.get(pk=Essay.objects.get(pk=data.pk).class_name.pk).student.all()

			for student in students:
				response = EssayResponse(essay=data, student=student)
				response.save()

			#return HttpResponseRedirect('/essays/')
			return list_essay(request, None, 'New exam has been added.')
		else :
			errors = 1
		
	else:
		form = EssayForm()
		form.fields['class_name'].queryset = Class.objects.filter(teacher = Teacher.objects.get(user_id = request.user.id))
	
	return render(request, 'app_essays/teacher_newExam.html', {'avatar':avatar, 'active_nav':'EXAMS', 'errors':errors, 'form': form})

@login_required(redirect_field_name='', login_url='/')	
def list_essay(request, errors=None, success=None):
	active_nav = "EXAMS"
	userProfile = UserProfile.objects.filter(user_id = request.user.id)
	if not userProfile.exists():
		return redirect("/profile")
	avatar = userProfile.get(user_id = request.user.id).avatar
	#IF USER IS A TEACHER
	if len(Teacher.objects.filter(user_id = request.user.id)) > 0:
		no_on_going_essays = 0
		no_past_essays = 0
		no_on_queue_essays = 0

		on_queue_essays = Essay.objects.filter(instructor_id = Teacher.objects.get(user_id = request.user.id).id, status=1).filter(start_date__gt=timezone.now())
		on_going_essays = Essay.objects.filter(instructor_id = Teacher.objects.get(user_id = request.user.id).id, status=1).filter(start_date__lte=timezone.now(), deadline__gte=timezone.now())
		past_essays = Essay.objects.filter(instructor_id = Teacher.objects.get(user_id = request.user.id).id).filter(deadline__lt=timezone.now())
		
		if (len(on_queue_essays) == 0 ):
			no_on_queue_essays = 1	
		if (len(on_going_essays) == 0 ):
			no_on_going_essays = 1	
		if (len(past_essays) == 0):
			no_past_essays = 1
		return render(request, 'app_essays/teacher_viewExam.html',	{'avatar':avatar, 'active_nav':'EXAMS', 'no_on_queue_essays':no_on_queue_essays,'no_on_going_essays':no_on_going_essays, 'no_past_essays':no_past_essays, 'on_queue_essays':on_queue_essays,'on_going_essays':on_going_essays, 'past_essays':past_essays,'errors':errors, 'success':success})

	#IF USER IS A STUDENT
	elif len(Student.objects.filter(user_id = request.user.id)) > 0:
		#essays = Essay.objects.filter(instructor_id = Teacher.objects.get(user_id = request.user.id).id)
		no_on_going_essay_responses = 0
		no_past_essay_responses = 0

		#on_going_essay_responses = EssayResponse.objects.filter(~Q(status=2), student=Student.objects.get(user_id = request.user.id)).filter(essay__deadline__gte=timezone.now())
		on_going_essay_responses = EssayResponse.objects.filter(~Q(essay__status=-1), student=Student.objects.get(user_id = request.user.id)).filter(essay__start_date__lte=timezone.now(), essay__deadline__gte=timezone.now())
		past_essay_responses = EssayResponse.objects.filter(~Q(essay__status=-1), student=Student.objects.get(user_id = request.user.id)).filter(essay__deadline__lt=timezone.now())

		if (len(on_going_essay_responses) == 0 ):
			no_on_going_essay_responses = 1	
		if (len(past_essay_responses) == 0):
			no_past_essay_responses = 1
		return render(request, 'app_essays/student_viewEssay.html', {'avatar':avatar, 'active_nav':'EXAMS','no_on_going_essay_responses':no_on_going_essay_responses, 'no_past_essay_responses':no_past_essay_responses, 'on_going_essay_responses':on_going_essay_responses, 'past_essay_responses':past_essay_responses, 'errors':errors, 'success':success})
		
@login_required(redirect_field_name='', login_url='/')
def essay_details(request, essay_id=None):
	active_nav = "EXAMS"
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar

	if request.method == 'POST':
		essay_id_post = request.POST.get('essay-id')
		essay = Essay.objects.get(pk=essay_id_post)
		essay.status = -1
		essay.save()
		return redirect('essays:list')
	else:
		students = Class.objects.get(pk=Essay.objects.get(pk=essay_id).class_name.pk).student.all()
		essay = Essay.objects.get(pk=essay_id)
		essay_responses = sorted(EssayResponse.objects.filter(essay_id=essay.pk), key=operator.attrgetter('student.user.last_name', 'student.user.first_name')) # I used this way of sorting because we cannot use order_by() for case insensitive sorting :(
		if essay.deadline >= timezone.now():
			return render(request, 'app_essays/teacher_viewExamInfo_onGoing.html', {'avatar':avatar, 'active_nav':'EXAMS', 'essay':essay, 'essay_responses':essay_responses})
		else: 
			all_graded = EssayResponse.objects.filter(essay_id=essay.pk, grade=None).exists()
			return render(request, 'app_essays/teacher_viewExamInfo_forGrading.html', {'avatar':avatar, 'active_nav':'EXAMS', 'essay':essay, 'essay_responses':essay_responses, 'all_graded':all_graded})
	
@login_required(redirect_field_name='', login_url='/')
def answer_essay(request, essay_response_id):
	active_nav = "EXAMS"
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	essay_response = EssayResponse.objects.get(pk=int(essay_response_id))

	if essay_response.status == 0:
		essay_response.status = 1
		essay_response.time_started = datetime.now()
		essay_response.save()

	if request.method == 'POST':
		form = EssayResponseForm(request.POST, request)
		if form.is_valid():
			response_data = form.cleaned_data['response']
			essay_response.response = response_data
			essay_response.save()

			if 'draft' in request.POST:
				return redirect('essays:answer', essay_response_id=essay_response.pk)

			if 'final' in request.POST:
				essay_response.status = 2
				essay_response.save()
				return redirect('essays:submission', essay_response_id=essay_response.pk)
		else :
			errors = 1
		
	else:
		form = EssayResponseForm(initial={'response':essay_response.response})
		return render(request, 'app_essays/student_answerEssay.html', {'avatar':avatar, 'active_nav':'EXAMS', 'essay_response':essay_response, 'form':form})

@login_required(redirect_field_name='', login_url='/')
def essay_submission(request, essay_response_id):
	active_nav = "EXAMS"
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	essay_response = EssayResponse.objects.get(pk=int(essay_response_id))	
	numbered_response = ''

	if essay_response.response.isspace() or essay_response.response.strip() == '':
		has_submission = 0

	else:
		has_submission = 1
		tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')

		index = 1
		for paragraph in essay_response.response.split("\n"):
			sentences = tokenizer.tokenize(paragraph.strip())		
			numbered_response = numbered_response +"<p>"
			for i, sentence in enumerate(sentences):
				sentences[i] = '<sup>'+ str(index) +'</sup> ' + sentence
				index+=1
			numbered_response = numbered_response+''.join(sentences)+"</p>"

	#IF USER IS A TEACHER
	if len(Teacher.objects.filter(user_id = request.user.id)) > 0:

		if essay_response.grade == None:
			#SPELLING AND GRAMMAR CHECKER
			#c = pycurl.Curl()
			#url_param = "http://localhost:8081/?language=en-US&text="+urllib.quote_plus(essay_response.response)
			#c.setopt(c.URL, str(url_param))
			#c.perform()

			class EvaluateEssayFormSet(BaseFormSet):
				def __init__(self, *args, **kwargs):
					super(EvaluateEssayFormSet, self).__init__(*args, **kwargs)
					for form in self.forms:
						form.empty_permitted = True

			EssayCommentFormSet = formset_factory(EssayCommentForm, formset=EvaluateEssayFormSet)
			if request.method == 'POST': # If the form has been submitted...
				er_form = EssayResponseGradeForm(request.POST) # A form bound to the POST data
				er_form.fields['grade'].queryset = Grade.objects.filter(grading_system = essay_response.essay.grading_system).order_by('value')
				c_formset = EssayCommentFormSet(request.POST, request.FILES)

				if er_form.is_valid() and c_formset.is_valid():
					cd = er_form.cleaned_data
					essay_response.grade = cd['grade']
					essay_response.general_feedback = cd['general_feedback']
					essay_response.save()

					#if c_formset.empty_permitted and not c_formset.has_changed():
					for form in c_formset.forms:
						if form.empty_permitted and form.has_changed():
							c = form.save(commit=False)
							c.essay = essay_response
							c.save()
					return redirect('essays:list')
			else:
				er_form = EssayResponseGradeForm()
				er_form.fields['grade'].queryset = Grade.objects.filter(grading_system = essay_response.essay.grading_system).order_by('value')
				c_formset = EssayCommentFormSet()

			c = {'er_form': er_form,
				 'c_formset': c_formset,
				}
			c.update(csrf(request))
			return render(request, 'app_essays/teacher_viewEssaySubmission.html', {'avatar':avatar, 'active_nav':'EXAMS', 'essay_response':essay_response, 'has_submission':has_submission, 'er_form':er_form, 'c_formset':c_formset, 'numbered_response':numbered_response})
		
		else:
			comments = EssayComment.objects.filter(essay=essay_response)
			return render(request, 'app_essays/teacher_viewEssaySubmission_Graded.html', {'avatar':avatar, 'active_nav':'EXAMS', 'essay_response':essay_response, 'has_submission':has_submission, 'comments':comments, 'numbered_response':numbered_response})

	#IF USER IS A STUDENT
	elif len(Student.objects.filter(user_id = request.user.id)) > 0:
		comments = None
		if essay_response.grade != None:
			comments = EssayComment.objects.filter(essay=essay_response)
		return render(request, 'app_essays/student_viewEssaySubmission.html', {'avatar':avatar, 'active_nav':'EXAMS', 'essay_response':essay_response, 'has_submission':has_submission, 'comments':comments, 'numbered_response':numbered_response})
