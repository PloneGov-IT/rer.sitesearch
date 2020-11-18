# -*- coding: utf-8 -*-
from collective.z3cform.datagridfield import BlockDataGridFieldFactory
from plone.app.registry.browser import controlpanel
from rer.sitesearch import _
from rer.sitesearch.interfaces import IRerSiteSearchSettingsForm
from rer.sitesearch.interfaces import IRERSiteSearchSettings
from z3c.form import field
from zope.interface import implementer


class RERSiteSearchSettingsEditForm(controlpanel.RegistryEditForm):
    """
    """

    schema = IRERSiteSearchSettings
    id = "RERSiteSearchSettingsEditForm"
    label = _(u"Site Search settings")
    description = _(
        u"help_sitesearch_settings_editform",
        default=u"Set site search configurations",
    )

    fields = field.Fields(IRERSiteSearchSettings)
    fields["types_grouping"].widgetFactory = BlockDataGridFieldFactory
    fields["available_indexes"].widgetFactory = BlockDataGridFieldFactory

    def updateWidgets(self):
        """
        Hide some fields
        """
        super(RERSiteSearchSettingsEditForm, self).updateWidgets()

        self.widgets["types_grouping"].allow_reorder = True
        # self.widgets["types_grouping"].main_table_css_class = ""
        # self.widgets["available_indexes"].main_table_css_class = ""


@implementer(IRerSiteSearchSettingsForm)
class RERSiteSearchSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    """
    """

    form = RERSiteSearchSettingsEditForm