from django.conf import settings
from django.contrib.admin import widgets as Widgets
from django.core.urlresolvers import reverse
from django.forms import widgets as Widgets2
from django.utils.safestring import mark_safe


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
