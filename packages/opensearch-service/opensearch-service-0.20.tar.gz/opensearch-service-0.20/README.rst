ElasticSearchService
---------------------


**First install with pip**

    `pip install opensearch-service`

To use , simply do::

     from opensearch_service import OpensearchService

Configure your os Service with your parameters
###################################################

With no authentification define your host(default='localhost' and  port (default=9200)::

    os_service=OpensearchService() # default localhost and port 9200
           OR (ONLY FOR URL DIFFERENT Of localhost AND PORT IS NOT 9200
    os_service=OpensearchService('myurl',9201)

With HTTP basic authentification host, port and additional informations::

    os_service=OpensearchService('localhost',9200,scheme = 'http',http_auth_username = 'myuser',http_auth_password='mypassword')


To import objects in OpenSearch use :
##############################

os_service.import_documents(<index_os>,<list_of_dict>)

where <index_os> is a string like 'myos-index'
where <list_of_dict> is a list of dict like [{'id':'id1','field1':'value1,'field1','field2':'value2'},{'id':'id2','field1':'value3,'field2','field2':'value4'}]::

    list_of_values=[{'_id':'myid1','field1':'value1','field2':'value2','date':'2016-07-15T15:29:50+02:00'},{'_id':'myid2','field1':'value33','field2':'value4','date':'2016-07-15T15:29:50+02:00'}]
    os_service.import_documents('myos-index',list_of_values)

To search Objects in OpenSearch use :
##############################

os_service.get_documents(<index>,<parameter>)

        where <index> is a string like 'myos-index'

        where <parameter> are :
            To Specify a dateField use
                timefield='my_date_field'

                If so, you must specified a start date GREATER OR EQUAL
                   startdate='2020-04-01'
                And a end date LESS than (and not EQUAL)
                   enddate='2020-04-02'

            To Specify your query in a dict format use
                filters={'field1':['value1','valuer2'],'field2:[value]}
            To specify your query you MUST NOT in a dict format use
                exclude={'field1':['value1','valuer2']}
            To specify query with wildcard use
                 {'field1.keyword': 'value*'}
            To get only somme fields use :
                field_to_include={'include':['field1','field2']}

examples ::

    hits=os_service.get_documents('myos-index')
    hits=os_service.get_documents('myos-index',timefield='date',startdate='2020-04-01',enddate='2020-04-02')
    hits=os_service.get_documents('myos-index',filters={'field1':['value1','value3'],'field2':['value4']})
    hits=os_service.get_documents('myos-index',filters={'field1':['value1','value3']},wildcard={'field1.keyword':'value3*'})

examples to get values from search (to have hits)::

     for hit in hits:
        # if you want to access to your value in dict format
        values_in_dictformat=hit.to_dict()
        # OR
        # if you want to access to a specific value
        field1=hit.field1


TO Export a document in json(default) or csv file use :
#######################################################

export_documents(<INDEX>,<FILENAME>,<FORMAT>,<PARAMETER>)

        where <INDEX> is the index to export (strings)
        where <FILENAME> is the file name (string)
        where <FORMAT> can be json (default) ou csv
        where <PARAMETER> is the same than method getDocument() see previous7

example::

    os_service.export_documents('myos-index','osdata.json')
    os_service.export_documents('myos-index','osdata.csv',format='csv')

TO Import a json or csv file use :
##################################

import_documents_from_file(<INDEX>,<FILENAME>)
Note that :
for csv file : default delimiter is ;
for json file: must be list of value like [{"id": "id1"},{"id": "id2"}] <br/>


        where <INDEX> is the index to export (strings)
        where <FILENAME> is the file name (string) : can
        where <FORMAT> is the type of file : json (default) or csv

example::

    os_service.import_documents_from_file('myos-index1','osdata.json')
    os_service.import_documents_from_file('myos-index2','osdata.csv') # if delimiter is ;
    os_service.import_documents_from_file('myos-index3','osdata.csv',delimiter=',') # if delimiter is ,
