from django.views.generic import CreateView, TemplateView
from django.db.models import Q
from members.models import Member
from ofahrtbase.models import Ofahrt, Room
from staff.models import StaffRoomAssignment
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from . import forms
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.urls import reverse_lazy
from subprocess import Popen, PIPE
import tempfile
import math
import os
import datetime


def saveroomassignment(request):
    results = {'success': False}
    if request.method == u'GET':
        GET = request.GET
        userid = int(GET['user'])
        roomid = int(GET['room'])
        type = GET['datatype']

        if type == "member":
            user = Member.objects.get(pk=userid)
            if roomid == -1:
                user.room = None
            else:
                room = Room.objects.get(pk=roomid)
                user.room = room
            user.save()
        elif type == "staff":
            user = User.objects.get(pk=userid)
            try:
                room = StaffRoomAssignment.objects.get(user=user)
            except StaffRoomAssignment.DoesNotExist:
                room = StaffRoomAssignment(user=user)

            if roomid == -1:
                room.room = None
            else:
                room.room = Room.objects.get(pk=roomid)
            room.save()

        results = {'success': True}
    return HttpResponse(results)


class SignUpView(CreateView):
    template_name = "members/signup.html"
    success_url = reverse_lazy('members:success')
    form_class = forms.SignupForm

    def form_valid(self, form):
        member = form.save(commit=False)

        ofahrt = Ofahrt.current()
        member.base = ofahrt

        max_members = ofahrt.max_members
        queue_size = ofahrt.queue_tolerance
        members_fin = Member.objects.filter(money_received=True).count()
        members_queue = Member.objects.filter(money_received=False).filter(queue=True).count()

        email = EmailMessage()

        # Einstufung // Fall voll gibt es nicht
        if (members_fin + members_queue) < (max_members + queue_size):
            # Gesamtanmeldung noch nicht ausgelastet, Platz in der Queue
            # Neuanmeldungen fließen direkt in die vorläufige Anmeldeliste
            member.queue = True
            member.queue_deadline = datetime.datetime.now() + datetime.timedelta(7)

            email.subject = settings.MAIL_MEMBERSIGNUP_QUEUE_SUBJECT % (member.base.begin_date.year)
            email.body = settings.MAIL_MEMBERSIGNUP_QUEUE_TEXT % (
            member.first_name, member.base.begin_date.year, settings.BANK_ACCOUNT)

        else:
            # vorläufige Anmeldeliste ist voll, Anmeldungen kommen in die Warteschlange
            member.queue = False
            email.subject = settings.MAIL_MEMBERSIGNUP_SUBJECT % (member.base.begin_date.year)
            email.body = settings.MAIL_MEMBERSIGNUP_TEXT % (
            member.first_name, member.base.begin_date.year, settings.BANK_ACCOUNT)

        email.to = [member.email]
        email.send()

        return super(SignUpView, self).form_valid(form)

    def get_context_data(self, **kwargs):

        ofahrt = Ofahrt.current()

        max_members = ofahrt.max_members
        queue_size = ofahrt.queue_tolerance
        members_fin = Member.objects.filter(money_received=True).count()
        members_queue = Member.objects.filter(money_received=False).filter(queue=True).count()

        context = super(SignUpView, self).get_context_data(**kwargs)
        context["member_reg_open"] = ofahrt.member_reg_open
        context["members_fin"] = members_fin
        context["queue"] = (members_fin + members_queue) < (max_members + queue_size)

        return context


class SuccessView(TemplateView):
    template_name = "members/success.html"


class RoomassignmentView(TemplateView):
    template_name = "members/roomassignment.html"

    @staticmethod
    def get_users_with_no_room():
        out = []
        for user in User.objects.all():
            try:
                obj = StaffRoomAssignment.objects.get(user=user)
            except StaffRoomAssignment.DoesNotExist:
                obj = StaffRoomAssignment(user=user, room=None)
                obj.save()

            if obj.room == None:
                out.append(user)

        return out

    def get_context_data(self, **kwargs):
        context = super(RoomassignmentView, self).get_context_data(**kwargs)
        context["members"] = Member.objects.all().filter(Q(room=None) | Q(room__usecase_sleep=False)).filter(
            money_received=True)
        context["users"] = self.get_users_with_no_room()
        context["usercount"] = len(context["users"])
        context["rooms"] = Room.objects.all().filter(usecase_sleep=True)
        return context


def person_as_pdf(request):
    members = Member.objects.filter(money_received=True).order_by('last_name')
    staff = User.objects.order_by('last_name')
    context = Context({
        'members': members,
        'staff': staff
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
    temp = Room.objects.filter(usecase_sleep=True).order_by('number', 'name')
    rooms = []

    for room in temp:
        if room.get_person_count() > 0:
            rooms.append(room)

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

        ofahrt = Ofahrt.current()

        max_members = ofahrt.max_members

        context = super(MemberlistView, self).get_context_data(**kwargs)
        context["members_cond"] = Member.objects.filter(money_received=False).filter(queue=True)
        context["members_queue"] = Member.objects.filter(money_received=False).filter(queue=False)
        context["members_fin"] = Member.objects.filter(money_received=True)
        context["width"] = math.ceil((context["members_fin"].count() / max_members) * 100)
        context["max_members"] = max_members

        for index, member in enumerate(context["members_cond"]):
            context["members_cond"][index].last_name = member.last_name[:1] + "."

        for index, member in enumerate(context["members_fin"]):
            context["members_fin"][index].last_name = member.last_name[:1] + "."

        for index, member in enumerate(context["members_queue"]):
            context["members_queue"][index].last_name = member.last_name[:1] + "."

        return context
