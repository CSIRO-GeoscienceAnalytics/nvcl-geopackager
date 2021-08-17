from io import BytesIO
import os
import pathlib
import requests
import json

current_dir = pathlib.Path(__file__).parent.absolute()


def create_workspace(host: str, username: str, password: str, workspace_name: str):
    credentials = (username, password)
    workspace_data = {"workspace": {"name": workspace_name}}
    headers = {"Content-Type": "application/json"}
    r = requests.post(
        f"{host}/geoserver/rest/workspaces", headers=headers, auth=credentials, data=json.dumps(workspace_data)
    )

    r.raise_for_status()
    return r


def get_datastore(host: str, username: str, password: str, workspace_name: str, datastore_name: str):
    credentials = (username, password)
    headers = {"Content-Type": "application/json"}
    r = requests.get(
        f"{host}/geoserver/rest/workspaces/{workspace_name}/datastores/{datastore_name}",
        headers=headers,
        auth=credentials,
    )

    r.raise_for_status()
    return r


def update_datastore(host: str, username: str, password: str, workspace_name: str, datastore_name: str, update_data):
    credentials = (username, password)
    headers = {"Content-Type": "application/json"}
    r = requests.put(
        f"{host}/geoserver/rest/workspaces/{workspace_name}/datastores/{datastore_name}",
        headers=headers,
        auth=credentials,
        data=json.dumps(update_data),
    )

    r.raise_for_status()
    return r


def update_datastore_and_layer_from_file(
    host: str,
    username: str,
    password: str,
    workspace_name: str,
    datastore_name: str,
    layer_name: str,
    geopackage_file: BytesIO,
    description: str,
    keywords: list,
):
    credentials = (username, password)
    params = {"update": "overwrite"}
    headers = {"Content-type": "application/x-sqlite3"}

    try:
        r = requests.put(
            f"{host}/geoserver/rest/workspaces/{workspace_name}/datastores/{datastore_name}/file.gpkg",
            headers=headers,
            auth=credentials,
            data=geopackage_file,
            params=params,
        )

        r.raise_for_status()

        # This extra update is to set the connection params correctly.
        # Without it the datastore (and layer) will still work but the datasore will not be editable from the geoserver admin UI.
        datastore = get_datastore(host, username, password, workspace_name, datastore_name)

        datastore_details = json.loads(datastore.content)

        connection_params = datastore_details["dataStore"]["connectionParameters"]

        # check if the missing connection params are already present.  If not append them to the list and update.
        if len(next((x for x in connection_params["entry"] if x["@key"] == "Batch insert size"), [])) < 1:
            connection_params["entry"].append({"@key": "Batch insert size", "$": "1"})
            connection_params["entry"].append({"@key": "fetch size", "$": "1000"})
            connection_params["entry"].append({"@key": "Expose primary keys", "$": "true"})

            new_config = {"dataStore": {"description": description, "connectionParameters": connection_params}}
        else:
            new_config = {"dataStore": {"description": description}}

        update_datastore(host, username, password, workspace_name, datastore_name, new_config)

        update_feature_types(
            host, username, password, workspace_name, datastore_name, layer_name, description, keywords
        )

        return r

    except requests.exceptions.HTTPError as err:
        print(err)
        raise


def get_layer(host: str, username: str, password: str, workspace_name: str, datastore_name: str, layer_name: str):
    credentials = (username, password)
    headers = {"Content-Type": "application/json"}
    r = requests.get(
        f"{host}/geoserver/rest/workspaces/{workspace_name}/layers/{layer_name}", headers=headers, auth=credentials
    )

    r.raise_for_status()
    return r


def get_feature_types(
    host: str, username: str, password: str, workspace_name: str, datastore_name: str, feature_name: str
):
    credentials = (username, password)
    headers = {"Content-Type": "application/json"}
    r = requests.get(
        # f"{host}/geoserver/rest/workspaces/{workspace_name}/datastores/{datastore_name}/featuretypes/{feature_name}.json",
        f"{host}/geoserver/rest/workspaces/{workspace_name}/datastores/{datastore_name}/featuretypes/",
        headers=headers,
        auth=credentials,
    )

    r.raise_for_status()
    return r


def update_feature_types(
    host: str,
    username: str,
    password: str,
    workspace_name: str,
    datastore_name: str,
    feature_name: str,
    description: str,
    keywords: list,
):
    credentials = (username, password)
    headers = {"Content-Type": "application/json"}

    keyword_list = ["features", feature_name]
    keyword_list.extend(keywords)

    feature_data = {"featureType": {"abstract": description, "keywords": {"string": keyword_list}}}

    r = requests.put(
        f"{host}/geoserver/rest/workspaces/{workspace_name}/datastores/{datastore_name}/featuretypes/{feature_name}.json",
        headers=headers,
        auth=credentials,
        data=json.dumps(feature_data),
    )

    r.raise_for_status()
    return r
