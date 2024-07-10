# Author: Travis Crotteau
# Date: 20240710
# Title: RFParser.py
# Purpose: To parse incoming Recorded Future logs.  The script parses fields out of 
# the hits field in the log.  Meant to be used with a playbook.

def parse_fields(hits):

    parsed_fields = {}

    for hit_index, hit in enumerate(hits):

        # First iterate though entities, which is a list of dicts
        entities = hit['entities']
        for entity_index, entity in enumerate(entities):
            entity_type = entity['type']
            parsed_fields[f'{entity_type}_{hit_index}.{entity_index}'] = entity['name']

        # Then parse document information for hit
        documents = hit['document']
        parsed_fields[f'title_{hit_index}'] = documents['title']
        parsed_fields[f'doc_url_{hit_index}'] = documents['url']

        #Then parse source information for hit from document dictionary
        source = documents['source']
        parsed_fields[f'hit_source_{hit_index}'] = source['name']

        #Then parse description in hit
        parsed_fields[f'description_{hit_index}'] = hit['fragment']

    return parsed_fields

def main():

    # get hits field
    hits = demisto.getArg('hits')
    hits = json.loads(hits)

    # set alert fields
    output_fields = parse_fields(hits)

    # output results
    demisto.results(output_fields)

if __name__ in ('__main__','builtins'):
    main()
