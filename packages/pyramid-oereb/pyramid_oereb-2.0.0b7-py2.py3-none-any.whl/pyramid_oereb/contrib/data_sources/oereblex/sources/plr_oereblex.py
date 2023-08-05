# -*- coding: utf-8 -*-
import logging

from pyramid_oereb import Config
from pyramid_oereb.contrib.data_sources.oereblex.sources.document import OEREBlexSource
from pyramid_oereb.contrib.data_sources.standard.sources.plr import DatabaseSource

log = logging.getLogger(__name__)


class DatabaseOEREBlexSource(DatabaseSource):
    """
    A source to get models documents attached to public law restrictions in replacement
    of standards documents. Be sure to use a model with an OEREBlex "geolink" integer
    column for plrs that use this source.
    """
    def __init__(self, **kwargs):
        """
        Keyword Arguments:
            name (str): The name. You are free to choose one.
            code (str): The official code. Regarding to the federal specifications.
            geometry_type (str): The geometry type. Possible are: POINT, POLYGON, LINESTRING,
                GEOMETRYCOLLECTION
            thresholds (dict): The configuration of limits and units used for processing.
            text (dict of str): The speaking title. It must be a dictionary containing language (as
                configured) as key and text as value.
            language (str): The language this public law restriction is originally shipped with.
            federal (bool): Switch if it is a federal topic. This will be taken into account in processing
                steps.
            source (dict): The configuration dictionary of the public law restriction
            hooks (dict of str): The hook methods: get_symbol, get_symbol_ref. They have to be provided as
                dotted string for further use with dotted name resolver of pyramid package.
            law_status (dict of str): The multiple match configuration to provide more flexible use of the
                federal specified classifiers "inKraft" or "AenderungMitVorwirkung"
                or "AenderungOhneVorwirkung".
        """
        super(DatabaseOEREBlexSource, self).__init__(**kwargs)
        config = Config.get_oereblex_config()
        config["code"] = self._plr_info.get('code')
        self._oereblex_source = OEREBlexSource(**config)
        self._queried_geolinks = {}

    @staticmethod
    def get_config_value_for_plr_code(url_param_config, plr_code):
        """
        Returns the appropriate configuration entry for a plr within a url_param_config section.
        """
        for url_param_entry in url_param_config:
            if url_param_entry['code'] == plr_code:
                if 'url_param' in url_param_entry:
                    return url_param_entry['url_param']
                else:
                    log.warning("Incorrect configuration: missing url_param for entry {}".format(plr_code))
                    return None
        return None

    def get_document_records(self, params, public_law_restriction_from_db):
        """
        Override the parent's get_document_records method to obtain the models document instead.
        """
        oereblex_params = None
        url_param_config = self._oereblex_source._url_param_config
        if url_param_config:
            plr_code = self._theme_record.code
            oereblex_params = DatabaseOEREBlexSource.get_config_value_for_plr_code(url_param_config, plr_code)
        return self.document_records_from_oereblex(params, public_law_restriction_from_db.geolink,
                                                   oereblex_params)

    def document_records_from_oereblex(self, params, geolink, oereblex_params):
        """
        Create document records parsed from the OEREBlex response with the specified geoLink ID and appends
        them to the current public law restriction.

        Args:
            params (pyramid_oereb.views.webservice.Parameter): The parameters of the extract request.
            geolink (int): The ID of the GEO-Link to request the documents for.
            oereblex_params (string): URL parameter to add to the models request

        Returns:
            list of pyramid_oereb.core.records.documents.DocumentRecord:
                The documents created from the parsed OEREBlex response.
        """
        log.debug("document_records_from_oereblex() start, GEO-Link {}, oereblex_params {}"
                  .format(geolink, oereblex_params))
        identifier = '{}{}'.format(geolink, params.language)
        if identifier in self._queried_geolinks:
            log.debug('skip querying this geolink "{}" because it was fetched already.'.format(identifier))
            log.debug('use already queried instead')
        else:
            self._oereblex_source.read(params, geolink, oereblex_params)
            log.debug("document_records_from_oereblex() returning {} records"
                      .format(len(self._oereblex_source.records)))
            self._queried_geolinks[identifier] = self._oereblex_source.records
        return self._queried_geolinks[identifier]
