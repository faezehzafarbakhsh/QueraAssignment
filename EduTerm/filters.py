from django_filters import rest_framework as filters
from EduTerm import models as eduterm_models



class Termfilters(filters.filterset):
    class Meta:
        model=eduterm_models.Term
        fields=['name','exam_start_date','term_end_date',' active_term', ]
        

