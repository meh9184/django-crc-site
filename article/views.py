# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template.context_processors import csrf
from article.models import Entries, CheckContent,Tags, Url
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from article.pagingHelper import PagingHelper
from django.db.models import Q, F, Count, Max, Min
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from difflib import SequenceMatcher as m
import sys
from django.http import JsonResponse
import collections
import random

def chunker(seq, size):
	return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def home(request):
	if request.method == 'GET':
		articleList = Entries.objects.order_by('-id')
		paginator = Paginator(articleList, 20)
		pages = list(paginator.page_range)
		pages_list=[]
		for page in chunker(pages,10):
			pages_list.append(page)

		page = request.GET.get('current_page')
		pagelistnum = 0
		if page == None:
			pagelistnum = 0
		else:
			pagelistnum = (int(page)-1)/10

		new_pages_list=pages_list[pagelistnum]
		tags = Tags.objects.filter(uid = request.user)

		try:
			contacts = paginator.page(page)
		except PageNotAnInteger:
			contacts=paginator.page(1)
		except EmptyPage:
			contacts = paginator.page(paginator.num_pages)



	return render_to_response('article/list.html', {"contacts": contacts, "user": request.user, "tags" : tags, "pages_list": new_pages_list, "pagelistnum":pagelistnum})

def index(request):
	return render_to_response('article/index.html', {"user":request.user})


def confirmSentence(request):
	if request.method == 'POST':
		id = request.POST.get('id')
		tags = Tags.objects.get(id=id)
		sentence = tags.asentence

	return HttpResponse(sentence)

def editTags(request):

	if request.method == 'POST':
		aid = request.POST.get('aid')
		id = request.POST.get('id')
		asubject = request.POST.get('subject')
		aobejct = request.POST.get('object')
		averb = request.POST.get('verb')
		aetc = request.POST.get('etc')
		Tags.objects.filter(id=id).update(asubject=asubject, aobejct=aobejct, averb=averb, aetc=aetc)
		tags = Tags.objects.filter(aid=aid)

	return render_to_response('article/editTaglist.html', {'tags': tags, 'user':request.user})


def articleBody(request):
	if request.method == 'GET':
		id = request.GET.get('id')
		contacts = Entries.objects.get(id=id)
		tags = Tags.objects.filter(aid=id)

	elif request.method == 'POST':
		id = request.POST.get('id')
		aid = request.POST.get('aid')
		tags = Tags(id=id)
		tags.delete()

		tags = Tags.objects.filter(aid=aid)

		return render_to_response('article/taglist_body.html', {'tags': tags, 'user': request.user})

	return render_to_response('article/body.html', {"contacts": contacts,'tags': tags,  'user': request.user})


def articleList(request):
	tags = Tags.objects.filter(uid = request.user)

	if request.method == 'POST':
		start_date = str(request.POST.get('startdate'))
		end_date = str(request.POST.get('enddate'))
		press = request.POST.get('press')
		checks =  request.POST.get('checks[]')
		print(start_date,press,checks)

		if start_date!='' and end_date=='':
			return HttpResponse('Date set Error!! Please set start date and end date exactly!!')
		if start_date=='' and end_date!='':
			return HttpResponse('Date set Error!! Please set start date and end date exactly!!')


		if start_date != "":
			if press != "":
				if checks == "":
					contactss = Entries.objects.filter(aDate__lt=end_date, aDate__gt=start_date, press=press).order_by('-id')
				elif checks == "m":
					contactss = Entries.objects.filter(aDate__lt=end_date, aDate__gt=start_date, press=press, nClass=checks).order_by('-id')
				else:
					contactss = Entries.objects.filter(aDate__lt=end_date, aDate__gt=start_date, press=press, subClass=checks).order_by('-id')

			else:
				if checks == "":
					contactss = Entries.objects.filter(aDate__lt=end_date, aDate__gt=start_date).order_by('-id')
				elif checks == "m":
					contactss = Entries.objects.filter(aDate__lt=end_date, aDate__gt=start_date, nClass=checks).order_by('-id')
				else:
					contactss = Entries.objects.filter(aDate__lt=end_date, aDate__gt=start_date, subClass=checks).order_by('-id')


			paginator = Paginator(contactss, 20)
			pages = list(paginator.page_range)
			pages_list=[]
			for page in chunker(pages,10):
				pages_list.append(page)
			pagelistnum = 0
			new_pages_list=pages_list[pagelistnum]



			try:
				contacts = paginator.page(1)

			except PageNotAnInteger:
				contacts.paginator.page(1)

			except EmptyPage:
				contacts = paginator.page(paginator.num_pages)

			return render_to_response('article/list.html',{"pagelistnum":pagelistnum, "pages_list":new_pages_list,"tags":tags, "contacts": contacts, "user": request.user, "start_date":start_date, "end_date":end_date, "press":press, "checks":checks})

		else:
			if press != "":
				if checks == "m":
					contactss = Entries.objects.filter(nClass = checks, press = press).order_by('-id')
				elif checks == "":
					contactss = Entries.objects.filter(press = press).order_by('-id')
				else:
					contactss = Entries.objects.filter(subClass = checks, press = press).order_by('-id')
			elif press == "":
				if  checks == "m":
					contactss = Entries.objects.filter(nClass = checks).order_by('-id')
				elif checks != "":
					contactss = Entries.objects.filter(subClass = checks).order_by('-id')

			paginator = Paginator(contactss, 20)
			pages = list(paginator.page_range)
			pages_list=[]
			for page in chunker(pages,10):
				pages_list.append(page)

			pagelistnum = 0
			new_pages_list=pages_list[pagelistnum]

			try:
				contacts = paginator.page(1)

			except PageNotAnInteger:
				contacts.paginator.page(1)

			except EmptyPage:
				contacts = paginator.page(paginator.num_pages)

			return render_to_response('article/list.html',{"pagelistnum":pagelistnum, "pages_list":new_pages_list,"tags":tags, "contacts": contacts, "user": request.user, "start_date":start_date, "end_date":end_date, "press":press, "checks":checks})


	elif request.method == 'GET':
		start_date = str(request.GET.get('start_date'))
		end_date = str(request.GET.get('end_date'))
		press = request.GET.get('press')
		nowpage = request.GET.get('current_page')
		checksa =  request.GET.get('checks')
		checksb =  request.GET.get('checks[]')
		checks = 0

		if start_date=='':
			start_date = 'None'

		if end_date=='':
			end_date = 'None'

		if start_date!='None' and end_date=='None':
			return HttpResponse('Date set Error!! Please set start date and end date both of them exactly!!')
		if start_date=='None' and end_date!='None':
			return HttpResponse('Date set Error!! Please set start date and end date both of them exactly!!')

		if press == None:
			press = u''


		if checksa == None:
			checks = checksb
		else:
			checks = checksa

		if checks == None:
			checks = u''

		print(start_date, end_date, press, checks)
		if start_date != 'None':
			if press != '':
				if checks == '':
					contactss = Entries.objects.filter(aDate__lt=end_date, aDate__gt=start_date, press=press).order_by('-id')
				elif checks == "m":
					contactss = Entries.objects.filter(aDate__lt=end_date, aDate__gt=start_date, press=press, nClass=checks).order_by('-id')
				else:
					contactss = Entries.objects.filter(aDate__lt=end_date, aDate__gt=start_date, press=press, subClass=checks).order_by('-id')

			else:
				print('here')
				if checks == '':
					contactss = Entries.objects.filter(aDate__lt=end_date, aDate__gt=start_date).order_by('-id')
				elif checks == "m":
					contactss = Entries.objects.filter(aDate__lt=end_date, aDate__gt=start_date, nClass=checks).order_by('-id')
				else:
					contactss = Entries.objects.filter(aDate__lt=end_date, aDate__gt=start_date, subClass=checks).order_by('-id')


			paginator = Paginator(contactss, 20)
			pagelistnum = 0
			if nowpage == None:
				pagelistnum = 0
			else:
				pagelistnum = (int(nowpage)-1)/10
			pages = list(paginator.page_range)
			pages_list=[]
			for page in chunker(pages,10):
				pages_list.append(page)

			new_pages_list=pages_list[pagelistnum]

			try:
				contacts = paginator.page(nowpage)

			except PageNotAnInteger:
				contacts = paginator.page(1)

			except EmptyPage:
				contacts = paginator.page(paginator.num_pages)




			return render_to_response('article/list.html',{"contacts":contacts,"pagelistnum":pagelistnum, "pages_list":new_pages_list,"tags":tags, "user": request.user,"start_date":start_date, "end_date":end_date, "press":press, "checks":checks})

		else:
			print('aaaaa')
			if press != '':
				if checks == "m":
					contactss = Entries.objects.filter(nClass = checks, press = press).order_by('-id')
				elif checks == '':
					contactss = Entries.objects.filter(press = press).order_by('-id')
				else:
					contactss = Entries.objects.filter(subClass = checks, press = press).order_by('-id')

			elif press == '':
				if  checks == "m":
					contactss = Entries.objects.filter(nClass = checks).order_by('-id')
				elif checks != '':
					contactss = Entries.objects.filter(subClass = checks).order_by('-id')


			paginator = Paginator(contactss, 20)
			pagelistnum = 0
			if nowpage == None:
				pagelistnum = 0
			else:
				pagelistnum = (int(nowpage)-1)/10

			pages = list(paginator.page_range)
			pages_list=[]
			for page in chunker(pages,10):
				pages_list.append(page)

			new_pages_list=pages_list[pagelistnum]

			try:
				contacts = paginator.page(nowpage)

			except PageNotAnInteger:
				contacts = paginator.page(1)

			except EmptyPage:
				contacts = paginator.page(paginator.num_pages)

			return render_to_response('article/list.html',{"contacts":contacts,"pagelistnum":pagelistnum, "pages_list":new_pages_list,"tags":tags, "user": request.user, "start_date":start_date, "end_date":end_date, "press":press, "checks":checks})


def keyword(request):
	if request.method == 'POST':
		keyword = request.POST.get('keyword')
		articleList = Entries.objects.filter(title__contains=keyword).order_by('-id')
		paginator = Paginator(articleList, 20)
		pages = list(paginator.page_range)
		pages_list=[]
		for page in chunker(pages,10):
			pages_list.append(page)
		pagelistnum = 0
		new_pages_list=pages_list[pagelistnum]

		try:
			contacts = paginator.page(1)

		except PageNotAnInteger:
			contacts = paginator.page(1)

		except EmptyPage:
			contacts = paginator.page(paginator.num_pages)

		return render_to_response('article/keytable.html',{"pages_list": new_pages_list, "pagelistnum":pagelistnum, "keyword":keyword, "contacts":contacts,'user':request.user})

	elif request.method == 'GET':
		keyword = request.GET.get('keyword')
		nowpage = request.GET.get('current_page')
		pagelistnum = 0
		if nowpage == None:
			pagelistnum = 0
		else:
			pagelistnum = (int(nowpage)-1)/10
		articleList = Entries.objects.filter(title__contains=keyword).order_by('-id')
		paginator = Paginator(articleList, 20)
		pages = list(paginator.page_range)
		pages_list=[]
		for page in chunker(pages,10):
			pages_list.append(page)
		new_pages_list = pages_list[pagelistnum]

		try:
			contacts = paginator.page(nowpage)

		except PageNotAnInteger:
			contacts = paginator.page(1)

		except EmptyPage:
			contacts = paginator.page(paginator.num_pages)

		return render_to_response('article/list.html',{"keyword":keyword, "pages_list": new_pages_list, "pagelistnum":pagelistnum,"keyword":keyword, "contacts":contacts,'user':request.user})

def mainpage(request):
	return render_to_response("article/index.html", {"user":request.user})


def board(request):
	return render_to_response("article/boardTemplate.html")

def serviceNotice(request):
	return render_to_response("article/serviceNotice.html")

"""
def test(request):
	return render_to_response("article/parent.html")


def test2(request):
	return render_to_response("article/2.html")
"""

def loginok(request):
	return render_to_response("article/login_ok.html")


def signup(request):
	if request.method == "POST":
		userform = UserCreationForm(request.POST)
		if userform.is_valid():
			userform.save()
			return render_to_response("article/signup_ok.html")
	elif request.method == "GET":
		userform = UserCreationForm()

	return render_to_response("article/signup.html", {"userform": userform,})

def tags(request):
	# reload(sys)
	sys.setdefaultencoding('utf-8')

	if request.method == 'POST':
		atitle = request.POST.get('title')
		asubject = request.POST.get('subject')
		aobject = request.POST.get('object')
		averb = request.POST.get('verb')
		aid = request.POST.get('aid')
		acomplement = request.POST.get('complement')
		aetc = request.POST.get('aetc')
		asentence = request.POST.get('sentence')
		subjectflag = request.POST.get('subjectflag')
		objectflag = request.POST.get('objectflag')
		verbflag = request.POST.get('verbflag')
		etcflag = request.POST.get('etcflag')
		passiveflag = request.POST.get('passiveflag')
		checkflag = request.POST.get('ratioflag')
		articleDate = request.POST.get('adate')
		tempaDate = articleDate[0:10]
		apress = request.POST.get('apress')
		uid = request.user
		tempobjs = Tags.objects.filter(Q(articleDate__contains = tempaDate))
		print(checkflag)


		if checkflag == '0':
			ratio_flag = 0
			sum_obj = []
			str_sum_obj = ""
			for tempobj in tempobjs:
				tttsubject = tempobj.asubject
				tttobject = tempobj.aobejct
				tttverb = tempobj.averb
				tttpress = tempobj.apress
				tttdate = tempobj.articleDate
				subjectstr = m(None,asubject.encode('utf-8'), tttsubject.encode('utf-8'))
				objectstr = m(None,aobject.encode('utf-8'), tttobject.encode('utf-8'))
				verbstr = m(None,averb.encode('utf-8'), tttverb.encode('utf-8'))
				subjectratio = subjectstr.ratio()
				objectratio = objectstr.ratio()
				verbratio = verbstr.ratio()
				sumratio = (subjectratio+objectratio+verbratio)/3
				print(subjectratio , objectratio, verbratio)
				print(sumratio)
				strsumratio = str(sumratio*100)
				tttstr = "Press: " + tttpress +  "\nDate: " + tttdate + "\nS: " + tttsubject +"\nO: " + tttobject + "\nV: " + tttverb + "\nRatio: " + strsumratio + "%\n--------------------------\n"

				if sumratio > 0.88:
					ratio_flag = 1
					sum_obj.append(tttstr)

			for sumobj in sum_obj:
				str_sum_obj += sumobj


			if ratio_flag == 1:
				return HttpResponse('fail - 동일한 태그가 같은 날짜에 존재합니다.\n(유사성 비율이 88% 이상시 동일 태그로 간주.)\n*만일 유사성과 상관없이 저장하고 싶으시면 태그중복검사를 무시로 설정하세요.\n\n•유사한 태그 리스트↓\n-----------------------------------------------------\n'+str_sum_obj)
			else:
				tags_obj = Tags(asubject=asubject,aobejct=aobject,averb=averb,asentence=asentence,aid=aid,acomplement=acomplement,aetc=aetc,atitle=atitle, subjectflag=subjectflag, objectflag=objectflag, verbflag=verbflag, etcflag=etcflag, passiveflag=passiveflag, articleDate=articleDate, apress=apress, uid=uid)
				tags_obj.save()
				return HttpResponse('success - 저장 성공하였습니다.')

		else:
			tags_obj = Tags(asubject=asubject,aobejct=aobject,averb=averb,asentence=asentence,aid=aid,acomplement=acomplement,aetc=aetc,atitle=atitle, subjectflag=subjectflag, objectflag=objectflag, verbflag=verbflag, etcflag=etcflag, passiveflag=passiveflag, articleDate=articleDate, apress=apress, uid=uid)
			tags_obj.save()
			return HttpResponse('success')


	else:
		return HttpResponse('fail to connection method')


def tagList(request):
	tagsList = Tags.objects.order_by('-articleDate')
	paginator = Paginator(tagsList, 10)
	page = request.GET.get('current_page')

	presslist=[]
	for taglist in tagsList:
		presslist.append(taglist.apress)

	presscounter = collections.Counter(presslist)
	presses = presscounter.keys()


	try:
		contacts = paginator.page(page)

	except PageNotAnInteger:
		contacts = paginator.page(1)

	except EmptyPage:
		contacts = paginator.page(paginator.num_pages)

	return render_to_response('article/visualtaglist.html',{"contacts":contacts,"user":request.user, "presses":presses})


def datatest(request):
	id = request.GET.get('id')
	aadate = request.POST.get('aaDate')
	print(aadate)

	if id=='':
		contacts = Tags.objects.filter(articleDate__lte=aadate)
		dayday = Tags.objects.all()
	else:
		dayday = Tags.objects.filter(Q(asubject= id )|Q(aobejct= id))
		contacts = Tags.objects.filter(Q(articleDate__lte=aadate), Q(asubject= id )|Q(aobejct= id))


	maxDay = dayday.aggregate(Max('articleDate'))
	minDay = dayday.aggregate(Min('articleDate'))
	dayList =[]
	dayList.append(maxDay)
	dayList.append(minDay)

	temp_nodes_lists = []
	temo_link_lists = []
	temp_lists = []

	for contact in contacts:
		if contact.asubject != "":
			if contact.aobejct != "":
				temp_lists.append(contact.asubject.encode('utf8'))
				temp_lists.append(contact.aobejct.encode('utf8'))
			else:
				temp_lists.append(contact.asubject.encode('utf8'))
				temp_lists.append('noRelation')
		else:
			temp_lists.append('noRelation')
			temp_lists.append(contact.aobejct.encode('utf8'))



	counter = collections.Counter(temp_lists)
	keys = counter.keys()
	values = counter.values()

	for i in range(0,len(keys)):
		temp_dic = {}
		temp_dic['id'] = keys[i]
		temp_dic['weight'] = values[i]
		temp_dic['group'] = random.randint(1,10)
		temp_nodes_lists.append(temp_dic)

	temp_link_lists = []
	for contact in contacts:
		if contact.asubject != "":
			if contact.aobejct != "":
				temp = []
				temp.append(contact.asubject)
				temp.append(contact.aobejct)
				temp.append(contact.averb)
				temp_link_lists.append(temp)
			else :
				countflaga = 0
				for tempcontact in contacts:
					if tempcontact.asubject != "":
						if tempcontact.aobejct != "":
							if contact.asubject == tempcontact.asubject:
								countflaga += 1;
							elif contact.asubject == tempcontact.aobejct:
								countflaga += 1;

				if countflaga == 0:
					temp = []
					temp.append(contact.asubject)
					temp.append('noRelation')
					temp.append(contact.averb)
					temp_link_lists.append(temp)
		else:
			countflagb = 0
			for tempcontact in contacts:
				if tempcontact.asubject != "":
					if tempcontact.aobejct != "":
						if contact.aobejct == tempcontact.asubject:
							countflagb += 1;
						elif contact.aobejct == tempcontact.aobejct:
							countflagb += 1;

			if countflagb == 0:
				temp = []
				temp.append('noRelation')
				temp.append(contact.aobejct)
				temp.append(contact.averb)
				temp_link_lists.append(temp)


	temp_link_set = [list(t) for t in set(tuple(element) for element in temp_link_lists)]
	link_lists = []
	for s in temp_link_set:
		temp_dic = {}
		temp_verb = []
		temp_dic['source'] = s[0]
		temp_dic['target'] = s[1]
		temp_dic['value'] = 0;
		for l in temp_link_lists:
			if s[0] == l[0] and s[1] == l[1]:
				temp_dic['value'] += 1;
				tempverbstr = str("Ⓐ"+l[2].encode('utf-8'))
				temp_verb.append(tempverbstr);
				temp_dic['verb'] = temp_verb;
			elif s[0] == l[1] and s[1] == l[0]:
				temp_dic['value'] += 1;
				tempverbstr = str("Ⓟ"+l[2].encode('utf-8'))
				temp_verb.append(tempverbstr);
				temp_dic['verb'] = temp_verb;
		link_lists.append(temp_dic)



	final_link_lists = []

	for l in range(0, len(link_lists)):
		if l == len(link_lists)-1:
			check = 0
			for k in range(0, len(final_link_lists)):
				if (final_link_lists[k].get('source') == link_lists[l].get('source') and final_link_lists[k].get('target') == link_lists[l].get('target')) or (final_link_lists[k].get('target') == link_lists[l].get('source') and final_link_lists[k].get('source') == link_lists[l].get('target')):
					check = 1
					break
				else:
					check = 0

			if check == 1:
				break
			elif check == 0:
				final_link_lists.append(link_lists[l])

		for z in range(l+1, len(link_lists)):
			if link_lists[l].get('source') == link_lists[z].get('source') and link_lists[l].get('target') == link_lists[z].get('target'):
				print('same')
			elif link_lists[l].get('target') == link_lists[z].get('source') and link_lists[l].get('source') == link_lists[z].get('target'):
				print('same')
			else:
				if len(final_link_lists) == 0:
					final_link_lists.append(link_lists[l])
				else:
					check = 0
					for k in range(0, len(final_link_lists)):
						if (final_link_lists[k].get('source') == link_lists[l].get('source') and final_link_lists[k].get('target') == link_lists[l].get('target')) or (final_link_lists[k].get('target') == link_lists[l].get('source') and final_link_lists[k].get('source') == link_lists[l].get('target')):
							check = 1
							break
						else:
							check = 0

					if check == 1:
						break
					elif check == 0:
						final_link_lists.append(link_lists[l])


	miserables = {}
	miserables['nodes'] = temp_nodes_lists
	miserables['links'] = final_link_lists
	miserables['day'] = dayList


	return JsonResponse(miserables,safe = False)

def tagkeyword(request):

	pressList = Tags.objects.all()
	presslist=[]
	for press in pressList:
		presslist.append(press.apress)

	presscounter = collections.Counter(presslist)
	presses = presscounter.keys()


	if request.method == 'POST':
		keyword = request.POST.get('keyword')
		apress = request.POST.get('press')

		if keyword != "":
			tagsList = Tags.objects.filter(Q(asubject__contains=keyword) | Q(aobejct__contains=keyword)).order_by('-articleDate')
			paginator = Paginator(tagsList, 10)

			try:
				contacts = paginator.page(1)

			except PageNotAnInteger:
				contacts.paginator.page(1)

			except EmptyPage:
				contacts = paginator.page(paginator.num_pages)

			return render_to_response('article/tagkeytable.html',{"contacts":contacts,"presses":presses})

		else:
			tagsList = Tags.objects.filter(apress=apress).order_by('-articleDate')
			paginator = Paginator(tagsList, 10)

			try:
				contacts = paginator.page(1)

			except PageNotAnInteger:
				contacts.paginator.page(1)

			except EmptyPage:
				contacts = paginator.page(paginator.num_pages)

			return render_to_response('article/tagkeytable.html',{"contacts":contacts,"presses":presses})



	elif request.method == 'GET':
		keyword = request.GET.get('keyword')
		page = request.GET.get('page')
		apress = request.GET.get('press')

		if keyword != "":
			tagsList = Tags.objects.filter(Q(asubject__contains=keyword) | Q(aobejct__contains=keyword)).order_by('-articleDate')
			paginator = Paginator(tagsList, 10)

			try:
				contacts = paginator.page(page)

			except PageNotAnInteger:
				contacts.paginator.page(1)

			except EmptyPage:
				contacts = paginator.page(paginator.num_pages)

			return render_to_response('article/tagkeytable.html',{"contacts":contacts,"presses":presses})

		else:
			tagsList = Tags.objects.filter(apress=apress).order_by('-articleDate')
			paginator = Paginator(tagsList, 10)

			try:
				contacts = paginator.page(page)

			except PageNotAnInteger:
				contacts.paginator.page(1)

			except EmptyPage:
				contacts = paginator.page(paginator.num_pages)

			return render_to_response('article/tagkeytable.html',{"contacts":contacts,"presses":presses})


def tagBody(request):
	id = request.GET.get('id')

	return render_to_response('article/newnetwork.html', {'id':id})

