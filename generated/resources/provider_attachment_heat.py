
# AUTO-GENERATED file from IFMapApiGenerator. Do Not Edit!

from contrail_heat.resources import contrail
try:
    from heat.common.i18n import _
except ImportError:
    pass
from heat.engine import attributes
from heat.engine import constraints
from heat.engine import properties
try:
    from heat.openstack.common import log as logging
except ImportError:
    from oslo_log import log as logging
import uuid

from vnc_api import vnc_api

LOG = logging.getLogger(__name__)


class ContrailProviderAttachment(contrail.ContrailResource):
    PROPERTIES = (
        NAME, FQ_NAME, DISPLAY_NAME, VIRTUAL_ROUTER_REFS
    ) = (
        'name', 'fq_name', 'display_name', 'virtual_router_refs'
    )

    properties_schema = {
        NAME: properties.Schema(
            properties.Schema.STRING,
            _('NAME.'),
            update_allowed=True,
            required=False,
        ),
        FQ_NAME: properties.Schema(
            properties.Schema.STRING,
            _('FQ_NAME.'),
            update_allowed=True,
            required=False,
        ),
        DISPLAY_NAME: properties.Schema(
            properties.Schema.STRING,
            _('DISPLAY_NAME.'),
            update_allowed=True,
            required=False,
        ),
        VIRTUAL_ROUTER_REFS: properties.Schema(
            properties.Schema.LIST,
            _('VIRTUAL_ROUTER_REFS.'),
            update_allowed=True,
            required=False,
        ),
    }

    attributes_schema = {
        NAME: attributes.Schema(
            _('NAME.'),
        ),
        FQ_NAME: attributes.Schema(
            _('FQ_NAME.'),
        ),
        DISPLAY_NAME: attributes.Schema(
            _('DISPLAY_NAME.'),
        ),
        VIRTUAL_ROUTER_REFS: attributes.Schema(
            _('VIRTUAL_ROUTER_REFS.'),
        ),
    }

    update_allowed_keys = ('Properties',)

    def handle_create(self):
        obj_0 = vnc_api.ProviderAttachment(name=self.properties[self.NAME])

        if self.properties.get(self.DISPLAY_NAME) is not None:
            obj_0.set_display_name(self.properties.get(self.DISPLAY_NAME))

        # reference to virtual_router_refs
        if self.properties.get(self.VIRTUAL_ROUTER_REFS):
            for index_0 in range(len(self.properties.get(self.VIRTUAL_ROUTER_REFS))):
                try:
                    ref_obj = self.vnc_lib().virtual_router_read(
                        id=self.properties.get(self.VIRTUAL_ROUTER_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().virtual_router_read(
                        fq_name_str=self.properties.get(self.VIRTUAL_ROUTER_REFS)[index_0]
                    )
                obj_0.add_virtual_router(ref_obj)

        try:
            obj_uuid = super(ContrailProviderAttachment, self).resource_create(obj_0)
        except:
            raise Exception(_('provider-attachment %s could not be updated.') % self.name)

        self.resource_id_set(obj_uuid)

    def handle_update(self, json_snippet, tmpl_diff, prop_diff):
        try:
            obj_0 = self.vnc_lib().provider_attachment_read(
                id=self.resource_id
            )
        except:
            raise Exception(_('provider-attachment %s not found.') % self.name)

        if prop_diff.get(self.DISPLAY_NAME) is not None:
            obj_0.set_display_name(prop_diff.get(self.DISPLAY_NAME))

        # reference to virtual_router_refs
        ref_obj_list = []
        ref_data_list = []
        if self.VIRTUAL_ROUTER_REFS in prop_diff:
            for index_0 in range(len(prop_diff.get(self.VIRTUAL_ROUTER_REFS) or [])):
                try:
                    ref_obj = self.vnc_lib().virtual_router_read(
                        id=prop_diff.get(self.VIRTUAL_ROUTER_REFS)[index_0]
                    )
                except:
                    ref_obj = self.vnc_lib().virtual_router_read(
                        fq_name_str=prop_diff.get(self.VIRTUAL_ROUTER_REFS)[index_0]
                    )
                ref_obj_list.append(ref_obj.fq_name)

            obj_0.set_virtual_router_list(ref_obj_list)
            # End: reference to virtual_router_refs

        try:
            self.vnc_lib().provider_attachment_update(obj_0)
        except:
            raise Exception(_('provider-attachment %s could not be updated.') % self.name)

    def handle_delete(self):
        if self.resource_id is None:
            return

        try:
            self.vnc_lib().provider_attachment_delete(id=self.resource_id)
        except Exception as ex:
            self._ignore_not_found(ex)
            LOG.warn(_('provider_attachment %s already deleted.') % self.name)

    def _show_resource(self):
        obj = self.vnc_lib().provider_attachment_read(id=self.resource_id)
        obj_dict = obj.serialize_to_json()
        return obj_dict


def resource_mapping():
    return {
        'OS::ContrailV2::ProviderAttachment': ContrailProviderAttachment,
    }
