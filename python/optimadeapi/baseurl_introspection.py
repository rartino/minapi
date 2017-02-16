import sys, os
import cgitb
import json

def get_data(base_url):
    """
    This just inserts a hardcoded introspection string for the baseurl. 
    """
    return [
    {
      "api_version": "v1",
      "available_api_versions": {
        "v1": base_url+"v1/",
      },
      "formats": [
        "json",
      ],
      "entry_types_by_format": {
        "json": [
          "structure",
          "calculation"
        ],
      },
      "available_endpoints": [
        "entry",
        "all",
        "info"
      ]
    }
    ]
