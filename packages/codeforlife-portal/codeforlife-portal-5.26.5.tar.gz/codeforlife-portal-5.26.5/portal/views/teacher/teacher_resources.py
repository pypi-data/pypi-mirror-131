from common.permissions import logged_in_as_teacher
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from portal.strings.teacher_resources import (
    RAPID_ROUTER_RESOURCES_BANNER,
    KURONO_RESOURCES_BANNER,
)


@login_required(login_url=reverse_lazy("teacher_login"))
@user_passes_test(logged_in_as_teacher, login_url=reverse_lazy("teacher_login"))
def teacher_rapid_router_resources(request):
    return render(
        request,
        "portal/teach/teacher_resources.html",
        {"BANNER": RAPID_ROUTER_RESOURCES_BANNER, "rapid_router_resources": True},
    )


@login_required(login_url=reverse_lazy("teacher_login"))
@user_passes_test(logged_in_as_teacher, login_url=reverse_lazy("teacher_login"))
def teacher_kurono_resources(request):
    return render(
        request,
        "portal/teach/teacher_resources.html",
        {"BANNER": KURONO_RESOURCES_BANNER},
    )


@login_required(login_url=reverse_lazy("teacher_login"))
@user_passes_test(logged_in_as_teacher, login_url=reverse_lazy("teacher_login"))
def materials(request):
    return HttpResponseRedirect(reverse_lazy("teaching_resources"))


@login_required(login_url=reverse_lazy("teacher_login"))
@user_passes_test(logged_in_as_teacher, login_url=reverse_lazy("teacher_login"))
def kurono_teaching_packs(request):
    return HttpResponseRedirect(reverse_lazy("kurono_teaching_resources"))
