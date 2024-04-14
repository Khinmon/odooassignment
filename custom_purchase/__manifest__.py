# -*- coding: utf-8 -*-
{
    'name': "custom_purchase",

    'summary': "This is my assignment",

    'description': """
Modify the model of Purchase module to have additional fields to save the total weight of the items in Tons, and cost per Ton. The following picture shows the illustration of the requirement. Total Weight and Cost per Ton are the new fields to be added to the model.
    """,

    'author': "kkm",
    'depends': ['purchase'],

    # always loaded
    'data': [
        'views/purchase_views.xml',
    ],
}
