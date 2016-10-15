from django.views.generic import CreateView, TemplateView
from django.db.models import Q
from members.models import Member
from ofahrtbase.models import Ofahrt, Setting, Room
from django.core.mail import EmailMessage
#from pyofahrt import settings
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from django.template.loader import get_template
from django.urls import reverse_lazy
from subprocess import Popen, PIPE
import tempfile
import math
import os


def saveroomassignment(request):
    results = {'success':False}
    if request.method == u'GET':
        GET = request.GET
        userid = int(GET['user'])
        roomid = int(GET['room'])

        user = Member.objects.get(pk=userid)

        if roomid == -1:
            user.room = None
        else:
            room = Room.objects.get(pk=roomid)
            user.room = room
        user.save()

        results = {'success':True}
    return HttpResponse(results)

class SignUpView(CreateView):
    template_name = "members/signup.html"
    success_url = reverse_lazy('members:success')
    model = Member
    fields = ['first_name', 'last_name', 'gender', 'email', 'birth_date', 'food_preference', 'food_handicaps', 'free_text']

    def form_valid(self, form):
        member = form.save(commit=False)
        member.base = Ofahrt.current()

        email = EmailMessage()
        email.subject = settings.MAIL_MEMBERSIGNUP_SUBJECT % (member.base.begin_date.year)
        email.body = settings.MAIL_MEMBERSIGNUP_TEXT % (member.first_name, member.base.begin_date.year, settings.BANK_ACCOUNT)
        email.to = [member.email]
        email.send()

        return super(SignUpView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SignUpView, self).get_context_data(**kwargs)
        context["member_reg_open"] = Setting.get_Setting("member_reg_open")
        return context


class SuccessView(TemplateView):
    template_name = "members/success.html"



class RoomassignmentView(TemplateView):
    template_name = "members/roomassignment.html"

    def get_context_data(self, **kwargs):
        context = super(RoomassignmentView, self).get_context_data(**kwargs)
        context["users"] = Member.objects.all().filter(Q(room=None) | Q(room__usecase_sleep=False))
        context["rooms"] = Room.objects.all().filter(usecase_sleep=True)
        return context

def person_as_pdf(request):
    members = Member.objects.order_by('last_name')
    context = Context({
            'members': members,
        })
    template = get_template('members/RaumzuteilungB.tex')
    rendered_tpl = template.render(context).encode('utf-8')
    with tempfile.TemporaryDirectory() as tempdir:
        for i in range(2):
            process = Popen(
                ['pdflatex', '-output-directory', tempdir],
                stdin=PIPE,
                stdout=PIPE,
            )
            process.communicate(rendered_tpl)

        print(os.listdir(tempdir))
        with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
            pdf = f.read()
    r = HttpResponse(content_type='application/pdf')
    r.write(pdf)
    return r


def room_as_pdf(request):
    rooms = Room.objects.order_by('name')
    context = Context({
            'rooms': rooms,
        })
    template = get_template('members/RaumzuteilungA.tex')
    rendered_tpl = template.render(context).encode('utf-8')
    with tempfile.TemporaryDirectory() as tempdir:
        for i in range(2):
            process = Popen(
                ['pdflatex', '-output-directory', tempdir],
                stdin=PIPE,
                stdout=PIPE,
            )
            process.communicate(rendered_tpl)

        with open(os.path.join(tempdir, 'texput.log'), 'rb') as f:
            print(f.read())
        with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
            pdf = f.read()
    r = HttpResponse(content_type='application/pdf')
    r.write(pdf)
    return r



class MemberlistView(TemplateView):
    template_name = "members/memberlist.html"

    def get_context_data(self, **kwargs):
        context = super(MemberlistView, self).get_context_data(**kwargs)
        context["members_cond"] = Member.objects.filter(money_received = False)
        context["members_fin"] = Member.objects.filter(money_received = True)
        context["width"] = math.ceil((context["members_fin"].count() / 70.) * 100)

        for index, member in enumerate(context["members_cond"]):
            context["members_cond"][index].last_name = member.last_name[:1] + "."

        for index, member in enumerate(context["members_fin"]):
            context["members_fin"][index].last_name = member.last_name[:1] + "."

        return context
