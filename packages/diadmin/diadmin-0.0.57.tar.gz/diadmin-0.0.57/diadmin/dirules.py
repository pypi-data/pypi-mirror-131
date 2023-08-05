#
#  SPDX-FileCopyrightText: 2021 Thorsten Hapke <thorsten.hapke@sap.com>
#
#  SPDX-License-Identifier: Apache-2.0
#

import logging
import argparse
from urllib.parse import urljoin
import json
from os import path

import yaml
import pandas as pd

from diadmin.metadata_api import rules
from diadmin.utils.utils import add_defaultsuffix, mksubdir

def main() :
    logging.basicConfig(level=logging.INFO)

    #
    # command line args
    #
    description =  "Download rules, rulebooks and results."
    achoices = ['rules','rulebooks','results']
    fchoices = ['api_json','condensed_json','csv']
    parser = argparse.ArgumentParser(description=description)
    help_config = 'Specifies config_demo.yaml file with the parameters: URL, TENANT, USER, PWD'
    parser.add_argument('type',choices=achoices, help = "Catalog type [connections,containers] only download..")
    parser.add_argument('-f','--format', help='Output format: raw, json or csv.',choices=fchoices,default='json')
    parser.add_argument('-i','--identifier', help='Identifier of rulebook')
    parser.add_argument('-n','--name', help='Name (regex pattern) of rulebook')
    parser.add_argument('-c','--config', help = help_config,default='config.yamls')
    args = parser.parse_args()

    config_file = 'config.yaml'
    if args.config:
        config_file = add_defaultsuffix(args.config,'yaml')
    with open(config_file) as yamls:
        params = yaml.safe_load(yamls)

    conn = {'url': urljoin(params['URL'] , '/app/datahub-app-metadata/api/v1'),
            'auth':(params['TENANT']+'\\'+ params['USER'],params['PWD'])}

    rules_directory = mksubdir('.','rules')

    if args.type == 'rules' :

        rb_id = ""
        if args.name:
            rb_id,rb_name = rules.get_rulebook_id(conn,args.name)
        elif args.identifier :
            rb_id = args.identifier
        rules_dict = rules.get_rules(conn,rb_id)

        rb_id = '_' + rb_id if rb_id else ''

        if args.format == 'api_json':
            output_file = 'rules' + rb_id + '_api.json'
            with open(path.join(rules_directory,output_file),'w') as fp :
                json.dump(rules_dict,fp,indent=4)
        elif args.format == 'condensed_json':
            rules_dict = rules.condense_rules(rules_dict)
            output_file = 'rules' + rb_id + '.json'
            with open(path.join(rules_directory,output_file),'w') as fp :
                json.dump(rules_dict,fp,indent=4)
        elif args.format == 'csv' :
            rules_list = rules.condense_rules(rules_dict)
            rules_list = rules.flat_rules(rules_list)
            df = pd.DataFrame(rules_list)
            output_file = 'rules' + rb_id + '.csv'
            df.to_csv(path.join(rules_directory,output_file),index=False)

    elif args.type == 'rulebooks':
        rulebooks = rules.get_rulebooks(conn)

        if args.format == 'api_json' :
            with open(path.join(rules_directory,'rulebooks_api.json'),'w') as fp :
                json.dump(rulebooks,fp,indent=4)
        elif args.format =='condensed_json':
            rulebooks = rules.condense_rulebooks(rulebooks)
            with open(path.join(rules_directory,'rulebooks.json'),'w') as fp :
                json.dump(rulebooks,fp,indent=4)
        elif args.format == 'csv' :
            rulebooks = rules.condense_rulebooks(rulebooks)
            df = pd.DataFrame(rulebooks)
            df.to_csv(path.join(rules_directory,'rulebooks.csv'),index=False)

    elif args.type == 'results':
        rb_id = ""
        if args.name:
            rb_id, rb_name = rules.get_rulebook_id(conn,args.name)
        elif args.identifier :
            rb_id = args.identifier
        rresults = rules.get_rulebook_results(conn,rb_id)

        if args.format == 'api_json':
            output_file = 'results_api_' + rb_id + '.json'
            with open(path.join(rules_directory,output_file),'w') as fp :
                json.dump(rresults,fp,indent=4)
        elif args.format == 'condensed_json':
            rresults = rules.flat_results(rresults,rb_id)
            output_file = 'results_' + rb_id + '.json'
            with open(path.join(rules_directory,output_file),'w') as fp :
                json.dump(rresults,fp,indent=4)
        elif args.format == 'csv':
            rresults = rules.flat_results(rresults,rb_id)
            df = pd.DataFrame(rresults)
            output_file = 'results_' + rb_id + '.csv'
            df.to_csv(path.join(rules_directory,output_file),index=False)

if __name__ == '__main__':
    main()