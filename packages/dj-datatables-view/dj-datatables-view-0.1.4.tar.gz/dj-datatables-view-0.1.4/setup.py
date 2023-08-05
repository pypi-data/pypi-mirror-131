# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dj_datatables_view']

package_data = \
{'': ['*']}

install_requires = \
['Django<empty>']

setup_kwargs = {
    'name': 'dj-datatables-view',
    'version': '0.1.4',
    'description': 'Django datatables view fork from django-datatables-view',
    'long_description': 'About\n=====\nFork from django-datatables-view\nCompatible with Django 2+ 3+ 4+\n\ndj-datatables-view is a base view for handling server side\nprocessing for the awesome datatables 1.9.*, 1.10.*, 1.11.*\nhttp://datatables.net\n\ndj-datatables-view simplifies handling of sorting, filtering and\ncreating JSON output, as defined at:\nhttps://datatables.net/examples/server_side\n\nUsage\n=====\n\n1. Install dj-datatables-view\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n::\n\n    pip install dj-datatables-view\n\n2. Edit views.py\n~~~~~~~~~~~~~~~~\n\n*django\\_datatables\\_view* uses **GenericViews**, so your view should\njust inherit from base class: **BaseDatatableView**, and override few\nthings (there is also a DatatableMixin - pure datatables handler that\ncan be used with the mixins of your choice, eg. django-braces). These\nare:\n\n-  **model** - the model that should be used to populate the datatable\n-  **columns** - the columns that are going to be displayed. If not\n   defined then django\\_datatables\\_view will look for \'name\' in the\n   columns definition provided in the request by DataTables, eg.:\n   columnDefs: [{name: \'name\', targets: [0]} (only works for datatables\n   1.10+)\n-  **order\\_columns** - list of column names used for sorting (eg. if\n   user sorts by second column then second column name from this list\n   will be used with order by clause). If not defined then\n   django\\_datatables\\_view will look for \'name\' in the columns\n   definition provided in the request by DataTables, eg.: columnDefs:\n   [{name: \'name\', targets: [0]} (only works for datatables 1.10+)\n-  **filter\\_queryset** - if you want to filter your DataTable in some\n   specific way then override this method. In case of older DataTables\n   (pre 1.10) you need to override this method or there will be no\n   filtering.\n-  **filter\\_method** - returns \'istartswith\' by default, you can\n   override it to use different filtering method, e.g. icontains: return\n   self.FILTER\\_ICONTAINS\n\nFor more advanced customisation you might want to override:\n\n-  **get\\_initial\\_queryset** - method that should return queryset used\n   to populate datatable\n-  **prepare\\_results** - this method should return list of lists (rows\n   with columns) as needed by datatables\n-  **escape\\_values** - you can set this attribute to False in order to\n   not escape values returned from render\\_column method\n\nThe code is rather simple so do not hesitate to have a look at it.\nMethod that is executed first (and that calls other methods to execute\nwhole logic) is **get\\_context\\_data**. Definitely have a look at this\nmethod!\n\nSee example below:\n\n.. code:: python\n\n\n        from dj-datatables-view.base_datatable_view import BaseDatatableView\n        from django.utils.html import escape\n\n        class OrderListJson(BaseDatatableView):\n            # The model we\'re going to show\n            model = MyModel\n\n            # define the columns that will be returned\n            columns = [\'number\', \'user\', \'state\', \'created\', \'modified\']\n\n            # define column names that will be used in sorting\n            # order is important and should be same as order of columns\n            # displayed by datatables. For non sortable columns use empty\n            # value like \'\'\n            order_columns = [\'number\', \'user\', \'state\', \'\', \'\']\n\n            # set max limit of records returned, this is used to protect our site if someone tries to attack our site\n            # and make it return huge amount of data\n            max_display_length = 500\n\n            def render_column(self, row, column):\n                # We want to render user as a custom column\n                if column == \'user\':\n                    # escape HTML for security reasons\n                    return escape(\'{0} {1}\'.format(row.customer_firstname, row.customer_lastname))\n                else:\n                    return super(OrderListJson, self).render_column(row, column)\n\n            def filter_queryset(self, qs):\n                # use parameters passed in GET request to filter queryset\n\n                # simple example:\n                search = self.request.GET.get(\'search[value]\', None)\n                if search:\n                    qs = qs.filter(name__istartswith=search)\n\n                # more advanced example using extra parameters\n                filter_customer = self.request.GET.get(\'customer\', None)\n\n                if filter_customer:\n                    customer_parts = filter_customer.split(\' \')\n                    qs_params = None\n                    for part in customer_parts:\n                        q = Q(customer_firstname__istartswith=part)|Q(customer_lastname__istartswith=part)\n                        qs_params = qs_params | q if qs_params else q\n                    qs = qs.filter(qs_params)\n                return qs\n\n3. Edit urls.py\n~~~~~~~~~~~~~~~\n\nAdd typical django\'s urlconf entry:\n\n.. code:: python\n\n    url(r\'^my/datatable/data/$\', login_required(OrderListJson.as_view()), name=\'order_list_json\'),\n\n4. Define HTML + JavaScript\n~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nExample JS:\n\n.. code:: javascript\n\n    $(document).ready(function() {\n        var oTable = $(\'.datatable\').dataTable({\n            // ...\n            "processing": true,\n            "serverSide": true,\n            "ajax": "{% url \'order_list_json\' %}"\n        });\n        // ...\n    });\n\nAnother example of views.py customisation\n-----------------------------------------\n\n.. code:: python\n\n    from dj-datatables-view.base_datatable_view import BaseDatatableView\n    from django.utils.html import escape\n\n    class OrderListJson(BaseDatatableView):\n        order_columns = [\'number\', \'user\', \'state\']\n\n        def get_initial_queryset(self):\n            # return queryset used as base for futher sorting/filtering\n            # these are simply objects displayed in datatable\n            # You should not filter data returned here by any filter values entered by user. This is because\n            # we need some base queryset to count total number of records.\n            return MyModel.objects.filter(something=self.kwargs[\'something\'])\n\n        def filter_queryset(self, qs):\n            # use request parameters to filter queryset\n\n            # simple example:\n            search = self.request.GET.get(\'search[value]\', None)\n            if search:\n                qs = qs.filter(name__istartswith=search)\n\n            # more advanced example\n            filter_customer = self.request.GET.get(\'customer\', None)\n\n            if filter_customer:\n                customer_parts = filter_customer.split(\' \')\n                qs_params = None\n                for part in customer_parts:\n                    q = Q(customer_firstname__istartswith=part)|Q(customer_lastname__istartswith=part)\n                    qs_params = qs_params | q if qs_params else q\n                qs = qs.filter(qs_params)\n            return qs\n\n        def prepare_results(self, qs):\n            # prepare list with output column data\n            # queryset is already paginated here\n            json_data = []\n            for item in qs:\n                json_data.append([\n                    escape(item.number),  # escape HTML for security reasons\n                    escape("{0} {1}".format(item.customer_firstname, item.customer_lastname)),  # escape HTML for security reasons\n                    item.get_state_display(),\n                    item.created.strftime("%Y-%m-%d %H:%M:%S"),\n                    item.modified.strftime("%Y-%m-%d %H:%M:%S")\n                ])\n            return json_data\n\nYet another example of views.py customisation\n---------------------------------------------\n\nThis sample assumes that list of columns and order columns is defined on\nthe client side (DataTables), eg.:\n\n.. code:: javascript\n\n    $(document).ready(function() {\n        var dt_table = $(\'.datatable\').dataTable({\n            order: [[ 0, "desc" ]],\n            columnDefs: [\n                {\n                    name: \'name\',\n                    orderable: true,\n                    searchable: true,\n                    targets: [0]\n                },\n                {\n                    name: \'description\',\n                    orderable: true,\n                    searchable: true,\n                    targets: [1]\n                }\n            ],\n            searching: true,\n            processing: true,\n            serverSide: true,\n            stateSave: true,\n            ajax: TESTMODEL_LIST_JSON_URL\n        });\n    });\n\n.. code:: python\n\n    class TestModelListJson(BaseDatatableView):\n        model = TestModel\n',
    'author': 'Longbowou',
    'author_email': 'blandedaniel@gmail.com',
    'maintainer': 'Longbowou',
    'maintainer_email': 'blandedaniel@gmail.com',
    'url': 'https://gitlab.com/longbowou/django-datatables-view',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
