#!/usr/bin/env python3
import argparse
import logging
from os import environ
from os.path import basename
from sys import argv
from typing import Iterable

from requests import patch

from vang.azdo.list_builds import list_builds

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(basename(__file__))

base_url = 'https://dev.azure.com'


def cancel_build(build_id: str, token: str, organisation: str, project: str, verify_certificate: bool = True,
                 api_version: str = '6.1-preview.6') -> Iterable:
    ids = []
    builds = list_builds(token, organisation, project, verify_certificate)
    for b in builds:
        if b['status'] != 'completed':
            print(b['status'])
            b['status'] = 'Cancelling'
            build_id = b['id']

            url = f'{base_url}/{organisation}/{project}/_apis/build/builds/{build_id}?api-version={api_version}'
            params = {
                'url': url,
                'auth': ('', token),
                'verify': verify_certificate,
                'json': b,
            }
            logger.info(f'params: {str(params).replace(token, "***")}')
            response = patch(**params)
            logger.info(f'response.status_code: {response.status_code}')
            logger.info(f'response.text: {response.text}')
            response.raise_for_status()
            ids.append(build_id)
    return ids


def parse_args(args):  # pragma: no cover
    parser = argparse.ArgumentParser(
        description='Cancel builds')
    parser.add_argument(
        'build_id',
        help='The id of the build to cancel')
    parser.add_argument(
        '--token',
        default=environ.get('AZDO_TOKEN', ''),
        help='The Azure DevOps authorisation token')
    parser.add_argument(
        '--organisation',
        default=environ.get('AZDO_ORGANISATION', ''),
        help='The Azure DevOps organisation')
    parser.add_argument(
        '--project',
        default=environ.get('AZDO_PROJECT', ''),
        help='The Azure DevOps project')
    parser.add_argument(
        '-au',
        '--azure_devops_url',
        default='https://dev.azure.com',
        help='The Azure DevOps REST API base url')

    return parser.parse_args(args)


def main(build_id: str, token: str, organisation: str, project: str, azure_devops_url: str) -> None:  # pragma: no cover
    global base_url
    base_url = azure_devops_url

    build_ids = cancel_build(build_id, token, organisation, project)
    print(build_ids)


if __name__ == '__main__':  # pragma: no cover
    main(**parse_args(argv[1:]).__dict__)
