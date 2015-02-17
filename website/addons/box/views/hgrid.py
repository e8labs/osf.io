# -*- coding: utf-8 -*-

import httplib as http

from flask import request
from urllib3.exceptions import MaxRetryError

from framework.exceptions import HTTPError
from website.project.decorators import must_be_contributor_or_public, must_have_addon
from website.util import rubeus

from website.addons.box.client import get_node_client
from website.addons.box.utils import metadata_to_hgrid


@must_be_contributor_or_public
@must_have_addon('box', 'node')
def box_hgrid_data_contents(node_addon, auth, **kwargs):
    """Return the Rubeus/HGrid-formatted response for a folder's contents.

    Takes optional query parameters `foldersOnly` (only return folders) and
    `includeRoot` (include the root folder).
    """
    # No folder, just return an empty list of data
    if node_addon.folder is None and not request.args.get('foldersOnly'):
        return {'data': []}
    node = node_addon.owner
    folder_id = kwargs.get('folder_id', 0)
    # Verify that path is a subdirectory of the node's shared folder
    #if not is_authorizer(auth, node_addon):
    #    abort_if_not_subdir(path, node_addon.folder)
    permissions = {
        'edit': node.can_edit(auth) and not node.is_registration,
        'view': node.can_view(auth)
    }
    client = get_node_client(node)
    file_not_found = HTTPError(http.NOT_FOUND, data=dict(message_short='File not found',
                                                  message_long='The Box file '
                                                  'you requested could not be found.'))

    max_retry_error = HTTPError(http.REQUEST_TIMEOUT, data=dict(message_short='Request Timeout',
                                                   message_long='Box could not be reached '
                                                   'at this time.'))

    try:
        metadata = client.get_folder(folder_id)
    except AttributeError:
            raise file_not_found
    except MaxRetryError:
        raise max_retry_error

    # Raise error if folder was deleted
    if metadata.get('is_deleted'):
        raise file_not_found
    contents = metadata['item_collection']['entries']
    if request.args.get('foldersOnly'):
        contents = [metadata_to_hgrid(file_dict, node, permissions) for
                    file_dict in contents if file_dict['type'] == u'folder']
    else:
        contents = [metadata_to_hgrid(file_dict, node, permissions) for
                    file_dict in contents]
    if request.args.get('includeRoot'):
        root = {'kind': rubeus.FOLDER, 'path': '/', 'name': '/ (Full Box)', 'id': folder_id}
        contents.insert(0, root)
    return contents


def box_addon_folder(node_settings, auth, **kwargs):
    """Return the Rubeus/HGrid-formatted response for the root folder only."""
    # Quit if node settings does not have authentication
    if not node_settings.has_auth or not node_settings.folder:
        return None
    node = node_settings.owner
    root = rubeus.build_addon_root(
        node_settings=node_settings,
        name=node_settings.folder,
        permissions=auth,
        nodeUrl=node.url,
        nodeApiUrl=node.api_url,
        urls={
            'fetch': node.api_url_for('box_hgrid_data_contents',
                path=node_settings.folder)
        }
    )
    return [root]
