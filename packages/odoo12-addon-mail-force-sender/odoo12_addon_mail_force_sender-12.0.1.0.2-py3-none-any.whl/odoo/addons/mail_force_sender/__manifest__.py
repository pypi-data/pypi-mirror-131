# Copyright 2021-Coopdevs Treball SCCL (<https://coopdevs.org>)
# - César López Ramírez - <cesar.lopez@coopdevs.org>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Mail Force Sender",
    "version": "12.0.1.0.2",
    "depends": ["base","mail"],
    "author": "Coopdevs Treball SCCL",
    "category": "Discuss",
    "website": "https://coopdevs.org",
    "license": "AGPL-3",
    "summary": """
        Force mail sender email address
    """,
    "data": ['data/ir_config_parameter.xml'],
    "installable": True,
    "post_load": "post_load_hook",
}

