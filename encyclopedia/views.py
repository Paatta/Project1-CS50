from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
from django import forms
from random import randint

from . import util

class Search(forms.Form):
    search_query = forms.CharField(label="Search",widget=forms.TextInput(attrs={'placeholder': 'Search'}))

class Newpage(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write the content here'}))

class Edit(forms.Form):
    edit = forms.CharField(label="",widget=forms.Textarea)

def index(request):

    if request.method=="POST":
        query=Search(request.POST)

        if query.is_valid():
            query = query.cleaned_data["search_query"].lower()
            entries=[entry.lower() for entry in util.list_entries()]

            if query in entries:
                content=util.get_entry(query)
                html_content=markdown2.markdown(content)

                return render(request,"encyclopedia/entry.html",{
                    "html_content":html_content,
                    "entry":query.capitalize(),
                    "searchbox":Search()
                    })

            else :
                results=[entry for entry in util.list_entries() if query in entry.lower()]
                return render(request, "encyclopedia/searchresults.html", {
                    "entries": results,
                    "searchbox":Search()
                    })
        else:
            return render(request,"encyclopedia/index.html",{
                "searchbox":Search()
            })


    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "searchbox":Search()
    })

def entry(request,entry):
    if entry in util.list_entries():
        content=util.get_entry(entry)
        html_content=markdown2.markdown(content)
        return render(request,"encyclopedia/entry.html",{
            "html_content":html_content,
            "entry":entry,
            "searchbox":Search()
            })
    else :
        return render(request,"encyclopedia/error.html",{
        "searchbox":Search()
        })

def create(request):
    if request.method=="POST":
        data=Newpage(request.POST)

        if data.is_valid():
            title=data.cleaned_data["title"]
            html_content=data.cleaned_data["content"]
            entries=[entry.lower() for entry in util.list_entries()]

            if title.lower() in entries:

                return render(request,"encyclopedia/create.html",{
                "error":True,
                "searchbox":Search(),
                "newpage":Newpage(request.POST),
                })


            else:
                util.save_entry(title,html_content)
                return render(request,"encyclopedia/entry.html",{
                "entry":title,
                "html_content":html_content,
                "searchbox":Search()})

        else:
            return render(request,HttpResponseRedirect(reverse,"url 'create'"))

    else:
        return render(request,"encyclopedia/create.html",{
        "error":False,
        "searchbox":Search(),
        "newpage":Newpage()
        })

def editpage(request,entry):

    if request.method=="POST":

        data=Edit(request.POST)

        if data.is_valid():
            content=data.cleaned_data["edit"]
            util.save_entry(entry,content)
            html_content=markdown2.markdown(content)

            return render(request,"encyclopedia/entry.html",{
            "html_content":html_content,
            "entry":entry,
            "searchbox":Search()
            })

        else:

            return render(request,HttpResponseRedirect("url 'editpage'"))

    else:

        content=util.get_entry(entry)
        initial = {'edit': content}
        editpage=Edit(initial=initial)
        return render(request,"encyclopedia/editpage.html",{
        "entry":entry,
        "editpage":editpage
        })

def randompage(request):
    entries=util.list_entries()
    num=randint(0,len(entries)-1)
    entry=entries[num]
    content=util.get_entry(entry)
    html_content=markdown2.markdown(content)

    return render(request,"encyclopedia/entry.html",{
    "html_content":html_content,
    "entry":entry,
    "searchbox":Search()

    })
