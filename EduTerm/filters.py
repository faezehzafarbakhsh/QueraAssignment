from django_filters import rest_framework as filters
from EduTerm import models as eduterm_models



class TermFilters(filters.FilterSet):
    class Meta:
        model=eduterm_models.Term
        fields=['name','exam_start_date','term_end_date', ]
        

