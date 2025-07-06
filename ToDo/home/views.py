from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Tasks
from datetime import date
import uuid

class NewTaskForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    task = forms.CharField(label="New Task", max_length=200)
    due_date = forms.DateField(label="Due Date", required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    
# Create your views here.
def index (request):
    if "tasks" not in request.session:
        request.session["tasks"] = []

    if request.method == "POST":
        form = NewTaskForm (request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            due_date = form.cleaned_data["due_date"]
            unique_id = str(uuid.uuid4())
            ans = {
                "id": unique_id,
                "task": task,
                "due_date": due_date.isoformat() if due_date else "",
                "completed": False,
                "flagged": False,
            }

            request.session["tasks"].append(ans)
            request.session.modified = True

            return HttpResponseRedirect (reverse("home:index"))
        else:
            return render (request, "home/index.html", {
                "form": form,
                "tasks": request.session["tasks"],
            })

    filter = request.GET.get("filter", "all")
    tasks = request.session["tasks"]

    if filter == "completed":
        dtasks = [t for t in request.session["tasks"] if t["completed"]]
    elif filter == "flagged":
        dtasks = [t for t in request.session["tasks"] if t["flagged"]]
    elif filter == "today":
        dtasks = [
            t for t in request.session["tasks"]
            if t["due_date"] and str(t["due_date"]) == str(date.today())
        ]
    else:
        dtasks = request.session["tasks"]

    return render (request, 'home/index.html', {
        "tasks": dtasks,
        "form": NewTaskForm()
    })

def finish(request):
    if request.method == "POST":
        # Get the task ID from the POST data
        task_id = request.POST.get("id")   # "a3c67-123-xyz"
        action = request.POST.get("action")

        # Check if tasks exist in the session
        if "tasks" in request.session:
            if action == "done":
                tasks = request.session["tasks"]
                updated_tasks = [t for t in tasks if t["id"] != task_id]

                # Save updated list back to the session
                request.session["tasks"] = updated_tasks
                request.session.modified = True
            else:
                tasks = request.session["tasks"]
                for t in tasks:
                    if t["id"] == task_id:
                        if t["flagged"] == True:
                            t["flagged"] = False
                        else:
                            t["flagged"] = True
                        break

                # Save updated list back to the session
                request.session["tasks"] = tasks
                request.session.modified = True
    return HttpResponseRedirect(reverse("home:index"))

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == "admin" and password == "admin":
            request.session["user"] = username
            return HttpResponseRedirect(reverse("home:index"))
        else:
            return render(request, "home/login.html", {
                "error": "Invalid credentials"
            })
    return render(request, "home/login.html")

def logout(request):
    if "user" in request.session:
        del request.session["user"]
    return HttpResponseRedirect(reverse("home:index"))