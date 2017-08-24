from django.conf import settings
from django.contrib.admin import widgets as Widgets
from django.core.urlresolvers import reverse
from django.forms import widgets as Widgets2
from django.utils.safestring import mark_safe
import copy
from django import forms
from django.contrib.admin.templatetags.admin_static import static
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


class CustomAdminSplitDateTime(Widgets.AdminSplitDateTime):

    def __init__(self, attrs=None):
        widgets = [Widgets.AdminDateWidget, Widgets.AdminTimeWidget(attrs=None, format='%I:%M %p')]
        forms.MultiWidget.__init__(self, widgets, attrs)


class RelatedFieldWidgetCanAdd(Widgets2.Select):
    def __init__(self, related_model, related_url, *args, **kw):
        super(RelatedFieldWidgetCanAdd, self).__init__(*args, **kw)
        if not related_url:
            rel_to = related_model
            info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
            related_url = 'admin:%s_%s_add' % info
            # Be careful that here "reverse" is not allowed
            self.related_url = related_url

    def render(self, name, value, *args, **kwargs):
        self.related_url = reverse(self.related_url)
        output = [super(RelatedFieldWidgetCanAdd, self).render(name, value, *args, **kwargs)]
        output.append('<a href="%s" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"> ' % \
                      (self.related_url, name))
        output.append('<img src="%sadmin/img/icon_addlink.gif" width="10" height="10" alt="%s"/></a>' % (
            settings.STATIC_URL, 'Add Another'))
        return mark_safe(''.join(output))


class AddAnotherWidgetWrapper(forms.Widget):
    """
    This class is a wrapper to a given widget to add the add icon for the
    admin interface. Modeled after
    django.contrib.admin.widgets.RelatedFieldWidgetWrapper
    """
    def __init__(self, widget, model):
        # self.is_hidden = widget.is_hidden
        self.needs_multipart_form = widget.needs_multipart_form
        self.attrs = widget.attrs
        self.choices = widget.choices
        self.widget = widget
        self.model = model

    def __deepcopy__(self, memo):
        obj = copy.copy(self)
        obj.widget = copy.deepcopy(self.widget, memo)
        obj.attrs = self.widget.attrs
        memo[id(self)] = obj
        return obj

    @property
    def media(self):
        return self.widget.media

    def render(self, name, value, *args, **kwargs):
        model = self.model
        info = (model._meta.app_label, model._meta.object_name.lower())
        self.widget.choices = self.choices
        output = [self.widget.render(name, value, *args, **kwargs)]
        related_url = reverse('admin:%s_%s_add' % info)
        output.append(('<a href="%s" class="add-another" id="add_id_%s" ' +
                      'onclick="return showAddAnotherPopup(this);"> ')
                      % (related_url, name))
        output.append('<img src="%s" width="10" height="10" alt="%s"/></a>'
                      % (static('admin/img/icon_addlink.gif'),
                         _('Add Another')))
        return mark_safe(''.join(output))

    def build_attrs(self, extra_attrs=None, **kwargs):
        "Helper function for building an attribute dictionary."
        self.attrs = self.widget.build_attrs(extra_attrs=None, **kwargs)
        return self.attrs

    def value_from_datadict(self, data, files, name):
        return self.widget.value_from_datadict(data, files, name)

    def _has_changed(self, initial, data):
        return self.widget._has_changed(initial, data)

    def id_for_label(self, id_):
        return self.widget.id_for_label(id_)