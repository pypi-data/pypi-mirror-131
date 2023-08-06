# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 - 2021 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

from datacite import schema43
from flask import current_app as app
from invenio_rdm_records.resources.serializers.datacite import DataCite43XMLSerializer
from lxml import etree


def datacite_etree(pid, record):
    """Dump the record (search result) into a DataCite XML format for OAI-PMH."""
    data_dict = DataCite43XMLSerializer().dump_one(record["_source"])
    return schema43.dump_etree(data_dict)


def oai_datacite_etree(pid, record):
    """Dump the record (search result) into a OAI DataCite XML format for OAI-PMH."""
    datacentre_symbol_text = app.config["CONFIG_TUW_OAI_DATACENTRE_SYMBOL"]
    resource_dict = DataCite43XMLSerializer().dump_one(record["_source"])

    nsmap = {
        None: "http://schema.datacite.org/oai/oai-1.1/",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    }

    attribs = {
        f"{{{nsmap['xsi']}}}schemaLocation": "http://schema.datacite.org/oai/oai-1.1/ http://schema.datacite.org/oai/oai-1.1/oai.xsd",  # noqa
    }

    # prepare the structure required by the 'oai_datacite' metadataPrefix
    oai_datacite = etree.Element("oai_datacite", nsmap=nsmap, attrib=attribs)
    schema_version = etree.SubElement(oai_datacite, "schemaVersion")
    datacentre_symbol = etree.SubElement(oai_datacite, "datacentreSymbol")
    payload = etree.SubElement(oai_datacite, "payload")

    # dump the record's metadata as usual
    resource = schema43.dump_etree(resource_dict)
    payload.append(resource)

    # set up the elements' contents
    schema_version.text = "4.3"
    datacentre_symbol.text = datacentre_symbol_text

    return oai_datacite
