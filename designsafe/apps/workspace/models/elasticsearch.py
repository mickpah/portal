from __future__ import unicode_literals, absolute_import
from future.utils import python_2_unicode_compatible
import logging
import json
from django.conf import settings
from django.db import models
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import (Search, DocType, Date, Nested,
                               analyzer, Object, Text, Long,
                               InnerObjectWrapper, Boolean, Keyword,
                               GeoPoint, String, MetaField)
from elasticsearch_dsl.query import Q
from elasticsearch import TransportError
from designsafe.libs.elasticsearch.analyzers import path_analyzer

#pylint: disable=invalid-name
logger = logging.getLogger(__name__)
#pylint: enable=invalid-name

@python_2_unicode_compatible
class IndexedApp(DocType):
    uuid = String(fields={'_exact': Keyword()})
    schemaId = String(fields={'_exact': Keyword()})
    internalUsername = String(fields={'_exact': Keyword()})
    associationIds = String(fields={'_exact': Keyword()}, multi=True)
    lastUpdated = Date()
    name = String(fields={'_exact': Keyword()})
    created = Date()
    owner = String(fields={'_exact': Keyword()})
    value = Nested(
        properties={
            'relations': Nested(properties={
                'type': Text(fields={'_exact'}),
                'uuids': Text(fields={'_exact'}, multi=True)
            }),
            'tags': Nested(properties={
                'name': Text(fields={'_exact'}),
                'value': Text(fields={'_exact'}, multi=True)
            }),
            'title': Text(analyzer='english'),
            'description': Text(analyzer='english')
        })

    class Meta:
        index = settings.ES_INDICES['project_entities']['name']
        doc_type = settings.ES_INDICES['project_entities']['documents'][0]['name']
        dynamic = MetaField('strict')
