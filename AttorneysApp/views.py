from django.shortcuts import render
from AttorneysApp.models import AttorneysProfile
from django.shortcuts import render, get_object_or_404

# Create your views here.


def attorneys_search(request):
    context = {}
    if request.method == 'POST':
        searched_data =  request.POST.get('searchkeywords')
        print(searched_data)
        try:
            status = AttorneysProfile.objects.filter(name__icontains=searched_data)
            print(status)
        except AttorneysProfile.DoesNotExist:
            status = None
        print({"attorneys":status, "SearchAbout": searched_data})
        return render(request,'Attorneys/filtered_attorneys.html', {"attorneys":status, "SearchAbout": searched_data})
    return render(request, 'Attorneys/seaching_temp.html', context)


def FilteredAttorneys(request):
    context = {}
    return render(request, 'Attorneys/filtered_attorneys.html', context)

def AttorneysProfileShown(request, id):
    attorneydetails = get_object_or_404(AttorneysProfile, id = id)
    context = {"attorneysDetails" : attorneydetails}
    print(context)
    return render(request, 'Attorneys/attorneys_profile.html', context)