import json
import logging
import pandas as pd

from opensearchpy import OpenSearch

from opensearchpy import helpers
from opensearch_dsl import Search, Index
from opensearch_dsl import Q, Search

class OpensearchService:
    """
    Class designed to ease request to OpenSearch (extract and import).
    """

    # Logging
    _FORMAT = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    _logger = None

    def __init__(self, host='localhost', port=9200, **kwargs):
        """
        Constructor.
        :param host: opensearch host (eg localhost)
        :param port: opensearch port (eg 9200)
        :param kwargs:
        doc_type is different from '_doc' (default value)
        timefield (if needed for requests based on dates)
        """

        # Logging
        logging.basicConfig(format=self._FORMAT, level=logging.WARNING)
        self._logger = logging.getLogger(__name__)
        logging.getLogger(__name__).setLevel(logging.INFO)

        self.host = host
        self.port = port
        user = kwargs.get('http_auth_username')
        passwd = kwargs.get('http_auth_password')
        api_key = kwargs.get('api_key')
        ssl_context = kwargs.get('ssl_context')
        with_authent = (user is not None) and (passwd is not None)
        with_api_key = (api_key is not None)
        with_ssl_context = (ssl_context is not None)
        if kwargs.get('doc_type'):
            self.doc_type = kwargs.get('doc_type')
        else:
            self.doc_type = '_doc'
        if (with_authent):  # ajout parametre extra (authent http basic)
            self._logger.info("log with auth")
            self.scheme = kwargs.get('scheme')
            if self.scheme == 'https':
                if with_ssl_context:
                    self.os = OpenSearch(hosts=[self.host], port=self.port,
                                            http_auth=(user, passwd),
                                            scheme=self.scheme,
                                            ssl_context=ssl_context)
                else:
                    self.os = OpenSearch(hosts=[self.host], port=self.port,
                                            http_auth=(user, passwd),
                                            verify_certs=False,
                                            connection_class=RequestsHttpConnection,
                                            scheme=self.scheme)
            else:
                self.os = OpenSearch(hosts=[self.host], port=self.port,
                                        http_auth=(user, passwd),
                                        scheme=self.scheme)
        elif with_api_key:
            self.os = OpenSearch(hosts=[self.host], port=self.port, api_key=api_key)
        else:
            self.os = OpenSearch(hosts=[self.host], port=self.port)

        if kwargs.get('timefield'):
            self.timefield = kwargs.get('timefield')

    def getClient(self):
        return self.os

    def get_client(self):
        return self.getClient()

    def setDoc_type(self, doc_type):
        self.doc_type = doc_type

    def set_doc_type(self, doc_type):
        self.setDoc_type(doc_type)

    def get_mapping(self, index):
        """
        Returns os index mapping
        :param index: os index
        :return: mapping as returned by opensearch-dsl package
        """
        dslIndex = Index(using=self.os, name=index)
        return dslIndex.get_mapping()

    def put_mapping(self, index, mapping_body):
        """
        Put os index mapping
        :param index: os index
        :param mapping_body: mapping body
        :param **kwargs: extra parameters (eg: timeout)
        """
        self.os.indices.put_mapping(index=index, body=mapping_body)

    def _build_search(self, index, **kwargs):
        """
        Internal method building the quering with respect to opensearch-dsl package.
        :param index: index for search
        :param kwargs: see getDocumentsCount and getDocuments
        :return:
        """
        startdate = kwargs.get('startdate', None)
        if startdate:
            timefield = kwargs.get('timefield')
            enddate = kwargs.get('enddate', 'now')
        filters = kwargs.get('filters', None)
        exclude = kwargs.get('exclude', None)
        ranges = kwargs.get('ranges', None)
        fields_to_include = kwargs.get('field_to_include', None)
        wildcards = kwargs.get('wildcard', None)
        start_from = kwargs.get('from_', None)
        size = kwargs.get('size', None)
        sort_ = kwargs.get('sort', None)

        search = Search(using=self.os, index=index, doc_type=self.doc_type)\
            .params(request_timeout=2000)

        if startdate:
            if startdate != enddate:
                timeRange = {timefield: {'gte': startdate, 'lt': enddate}}
            else:
                timeRange = {timefield: {'gte': startdate, 'lte': enddate}}
            search = search.filter('range', **timeRange)
        if filters:
            for key, val in filters.items():
                search = search.filter('terms' if isinstance(val, list) else 'term', **{key: val})
        if exclude:
            for ex in exclude.keys():
                search = search.exclude('terms', **{ex: exclude[ex]})
        if ranges:
            # ranges are expected in format:
            # [{field:{'gte':value, 'lte':value}}, {field: {'gte': value}}, {field: {'lte': value}}]
            for range_filter in ranges:
                search = search.filter('range', **range_filter)
        if fields_to_include:
            for field in fields_to_include.keys():
                search = search.source(**{field: fields_to_include[field]})
        if wildcards:
            for wild in wildcards:
                search = search.filter('wildcard', **{wild: wildcards[wild]})
        if start_from:
            search = search.extra(**{"from_": start_from})
        if size:
            search = search.extra(**{"size": size})
        if sort_:
            search = search.sort(*sort_)

        self._logger.info(json.dumps(search.to_dict()))

        return search

    def get_documents_count(self, index, **kwargs):
        """
        Returns document count in the index according to options
        :param index: index for search
        :param kwargs:
        startdate, timefield, endate:
            for time ranges, only documents with a date greater than equal to startdate and strictly
            lower than enddate according to timefield will be requested.
            If startdate is equal to enddate, document from startdate will be requested.
            Date format is expected to be compliant with opensearch (eg 'YYYY-MM-dd')
        filters:
            dictionary with all fields to use for filtering with their expected values in an array:
                {field: [value1, value2], field2: value1}.
        exclude:
            same as filters, but used to exclude documents.
        ranges:
            if there is a filter accoring to a numerical field value.
            Ranges are expected in format:
            [{field:{'gte':value, 'lte':value}}, {field:{'gte':value}}, {field:{'lte':value}}]
        wildcards:
            like filters, but used with * as wildcard
        :return:
        number of documents in index matching constraints.
        """
        return self._build_search(index, **kwargs).count()

    def get_documents(self, index, **kwargs):
        """
        Returns document  in the index according to options
        :param index: index for search
        :param kwargs:
        startdate, timefield, endate:
            for time ranges, only documents with a date greater than equal to startdate and strictly
            lower than enddate according to timefield will be requested.
            If startdate is equal to enddate, document from startdate will be requested.
            Date format is expected to be compliant with opensearch (eg 'YYYY-MM-dd')
        filters:
            dictionary with all fields to use for filtering with their expected values in an array:
                {field: [value1, value2], field2: value1}.
        exclude:
            same as filters, but used to exclude documents.
        ranges:
            if there is a filter accoring to a numerical field value.
            Ranges are expected in format:
            [{field:{'gte':value, 'lte':value}}, {field:{'gte':value}}, {field:{'lte':value}}]
        fields_to_include:
            Limit the returned documents to the fields in this list.
        wildcards:
            like filters, but used with * as wildcard
        from_, size:
            Can be used for pagination. If given, a list of documents with lenght 'size' will be
            returned, starting from the 'from_'th document.
        sort_:
            A list of fields used to sort the returned documents, with or without a specified order:
            [{"post_date": {"order": "asc"}}, "user", {"name": "desc"}, {"age": "desc"}]
        :return:
        document in index matching constraints as returned by opensearch-dsl package (Hits)
        """
        return self._build_search(index, **kwargs).params(request_timeout=2000).scan()

    def get_field_values(self, index, field, **kwargs):
        """
        Returns a dict with all possible values for field in ES and associated count
        :param index: os index
        :param field: field to consider
        :param kwargs:
        :return: dict key=field value, value: count
        """
        search = self._build_search(index, **kwargs)
        search.aggs.bucket('fieldCounts', 'terms', field=field, size=10000)
        fieldValues = {}
        for bucket in search.execute().aggregations.fieldCounts.buckets:
            fieldValues[bucket.key] =  bucket.doc_count
        return fieldValues

    def export_documents(self, index, filename, **kwargs):
        """
        Write documents  from the index according to options into a file
        :param index: index for search
        :param filename: file for data export (including path)
        :param kwargs:
        startdate, timefield, endate : for time ranges, only documents with a date greater than equal to startdate and strictly lower than enddate according to timefield will be requested.
         If startdate is equal to enddate, document from startdate will be requested. Date format is expected to be compliant with opensearch (eg 'YYYY-MM-dd')
        ranges : if there is a filter accoring to a numerical field value. Ranges are expected in format : [{field:{'gte':value, 'lte':value}}, {field:{'gte':value}}, {field:{'lte':value}}]
        filters : disctionnary with all fields to use for filtering with their expected values in an array : {field:[value1, value2], field2:[value1]}.
        :return: na
        """
        documentsGenerator = self.get_documents(index, **kwargs)
        documents = []
        format=kwargs.get('format','json')
        for doc in documentsGenerator:
            doc_with_id={**doc.to_dict(),'_id':doc.meta.id}
            documents.append(doc_with_id)
        self.__export_documents(documents,filename,exportformat=format)

    def __export_documents(self,documents,filename,exportformat):
        with open(filename, 'w') as f:
            if exportformat=='csv':
                df = pd.DataFrame(data=documents)
                df.to_csv(filename, encoding='utf-8', sep=';', index=False)
            else:
                f.write(json.dumps(documents))


    def import_documents(self, index, documents, **kwargs):
        """
        Import documents (array of dict) into opensearch index
        :param index: opensearch index (created if doesn't exist)
        :param documents: array of dict. For updates, each document (dict) must containg a value for key '_id'
        :return: response
        """
        self._logger.info('%s documents to index into %s', len(documents), index)
        response = None
        if 'pipeline' in kwargs:
            pipeline_name = kwargs.get("pipeline")
            response = helpers.bulk(self.os, documents, index=index, doc_type=self.doc_type, pipeline=pipeline_name)
        else:
            response = helpers.bulk(self.os, documents, index=index, doc_type=self.doc_type)

        # It returns a tuple with summary information - 
        # number of successfully executed actions and either list of errors or number of errors if stats_only is set to True.
        return response

    def import_documents_from_file(self, index, filename, delimiter=';'):
        """
        Load json data into opensearch
        :param index: opensearch index (created if doesn't exist)
        :param filename: json or csv file (For updates, each document (dict) must containg a value for key '_id')
        :param delimiter : define delimiter (only for csv files)
        :return: na
        """

        with open(filename, 'r') as f:
            if filename.endswith('.csv'):
                df=pd.read_csv(f, delimiter=delimiter,keep_default_na=False)
                documents=df.to_dict('records')
            elif filename.endswith('.json'):
                documents = json.load(f)
            else:
                raise Exception('File must be .csv or .json')
        helpers.bulk(self.os, documents, index=index, doc_type=self.doc_type)

    def get_allindex_accordingindexwithwildcard(self,indexwithwildcard):
        indexs=self.os.indices.get('*')
        indexwithoutwildcard=indexwithwildcard[:-1]
        return [x for x in indexs if x.startswith(indexwithoutwildcard)]

    def delete_index(self,index_to_delete):
        self.os.indices.delete(index=index_to_delete, ignore=[400, 404])
        
    def parallel_import_documents(self, index, documents, **kwargs):
        """
        Import documents (array of dict) into opensearch index
        :param index: opensearch index (created if doesn't exist)
        :param documents: array of dict. For updates, each document (dict) must containg a value for key '_id'
        :return: na
        """
        
        self._logger.info('%s documents to index into %s', len(documents), index)
        doc_count = 0        
        
        if len(documents) > 0:
            for success, info in helpers.parallel_bulk(self.os, documents,chunk_size=20000, index=index, doc_type="_doc", request_timeout=3600, raise_on_exception=False, raise_on_error=False, **kwargs):
                if not success:
                    self._logger.error(f'A document failed: {info}')
                else:
                    doc_count += 1
        
        self._logger.info('%s documents indexed into %s', doc_count, index)
        
        return doc_count        

    def get_documents_with_q(self, index, query=Q(), source=None, add_index_name = False):
        """
        Get documents from opensearch index
        :param index: opensearch index
        :param query: os query
        :param source: extra properties for search
        :return: dataframe with os data
        """
        
        s = Search(using=self.os, index=index)
        if source:
            s = s.source(source)
        # Dotted fields, replace . by __
        q = s.query(query)
        #print(str(q.to_dict()).replace("'",'"'))
        results = s.query(query).scan()
        
        if add_index_name:
            all_dicts = []
            for hit in results:
                result_dict = hit.to_dict()
                result_dict['_index'] = hit.meta.index
                all_dicts.append(result_dict)
                
            fa = pd.DataFrame.from_dict(all_dicts)
        else:
            fa = pd.DataFrame([hit.to_dict() for hit in results])
        
        return fa    
