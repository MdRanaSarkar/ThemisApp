from django.urls import path
from AttorneysApp.views import (attorneys_search,
                            FilteredAttorneys,
                            AttorneysProfileShown
                            )
urlpatterns = [
    path('search/', attorneys_search, name="searched_attorneys"),
    path('filtered_attorneys/', FilteredAttorneys, name= 'filtered_attorneys'),
    path('attorneyprofile/<int:id>/', AttorneysProfileShown, name='attorneysprofile'),
 ]