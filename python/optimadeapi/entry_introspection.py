#!/usr/bin/env python
#
# This file is part of the optimadeapi project, which is covered by the MIT License
# Details are given in the LICENSE file in the root of this project.
# (c) Rickard Armiento, 2016-2017

def get_data(entry, source_database, config):
    if entry == 'structures':
        return {
            'description': "A structure.",
            "properties": {
                "id": "An entry's ID",
                "modification_date": "A date representing when the entry was last modified.",
                "elements": "names of the elements found in the structure.",
                "nelements": "number of elements.",
                "chemical_formula": "The chemical formula for a structure.",
                "formula_prototype": ("The formula prototype obtained by sorting "
                                      "the elements by the occurence number in the reduced chemical formula and "
                                      "replace them with subsequent alphabet letters A, B, C and so on.")
                },
            "formats": ["json"],
            "output_fields_by_format": {
                "json": [
                    "id",
                    "modification_date",
                    "elements",
                    "nelements",
                    "chemical_formula",
                    "formula_prototype",
                    ]
                }
            }
    elif entry == 'calculations':
        return {
            'description': "A computation.",
            "properties": {
                "id": "An entry's ID.",
                "modification_date": "A date representing when the entry was last modified.",
                },
            "formats": ["json"],
            "output_fields_by_format": {
                "json": [
                    "id",
                    "modification_date",
                    ]
                }
            }
    else:
        raise Exception("Unknown entry type requested.")
    