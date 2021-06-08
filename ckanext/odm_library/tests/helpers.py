from ckan.tests import factories


class OdmLibraryDataset:
    def __init__(self):
        pass

    def _add_mandatory_fields(self, data_dict):
        """
        Add additional dataset arguments
        :return:
        """
        _mandatory_fields = {
            "notes_translated": {"en": "test"},
            "odm_spatial_range": "km",
            "document_type": "guidelines_manuals_handbooks",
            "version": "2020"
        }
        for k, val in _mandatory_fields.items():
            data_dict[k] = data_dict.get(k, val)
        return data_dict

    def create(self, *args, **kwargs):
        kwargs = self._add_mandatory_fields(kwargs)
        return factories.Dataset(*args, **kwargs)