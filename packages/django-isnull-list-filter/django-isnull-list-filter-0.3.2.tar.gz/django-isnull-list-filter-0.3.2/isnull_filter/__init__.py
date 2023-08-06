# -*- coding: utf-8 -*-

__version__ = '0.3.2'

from django.contrib.admin import SimpleListFilter
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


def isnull_filter(field_name, filter_title=None, negate=False, operator='null'):
    class HasRelatedFieldFilter(SimpleListFilter):
        parameter_name = f'{field_name}__is{operator}'
        related_field = field_name

        def __init__(self, request, field, model, model_admin):
            if filter_title:
                self.title = filter_title
            else:
                negate_str = 'not ' if negate else ''

                try:
                    related_field = model._meta.get_field(field_name)
                except FieldDoesNotExist:
                    model.objects.all().query.resolve_ref(field_name)
                    self.title = _(f"Is field '{field_name}' {negate_str}{operator}?")
                    return super(HasRelatedFieldFilter, self).__init__(request, field, model, model_admin)

                if hasattr(related_field, 'related'):
                    related_title = related_field.related.model._meta.verbose_name_plural
                    self.title = _(f"Is related '{related_title}' {negate_str}{operator}?")
                elif hasattr(related_field, 'related_model') and hasattr(related_field.related_model, "_meta"):
                    related_title = related_field.related_model._meta.verbose_name_plural
                    self.title = _(f"Is related '{related_title}' {negate_str}{operator}?")
                else:
                    related_title = related_field.name
                    self.title = _(f"Is field '{related_title}' {operator}?")
            super(HasRelatedFieldFilter, self).__init__(request, field, model, model_admin)

        def lookups(self, request, model_admin):
            return [
                ('true', _('True')),
                ('false', _('False')),
            ]

        def queryset(self, request, queryset):
            filters = Q()

            if self.value() in ('true', 'True'):
                value = True
            elif self.value() in ('false', 'False'):
                value = False
            else:
                value = None

            if value is not None:
                filters = Q(**{f"{self.related_field}__isnull": value})
                if operator == 'blank':
                    blank_filter = Q(**{f"{self.related_field}__exact": ''})
                    if value:
                        filters |= blank_filter
                    else:
                        filters &= ~blank_filter

            if negate:
                return queryset.exclude(filters).distinct()
            else:
                return queryset.filter(filters).distinct()

    return HasRelatedFieldFilter


def isblank_filter(field_name, filter_title=None, negate=False):
    return isnull_filter(field_name, filter_title=filter_title, negate=negate, operator='blank')
