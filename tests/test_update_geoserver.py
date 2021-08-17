import geopackager.update_geoserver

OUTPUT_DIR = "output"

LAYERNAME = "test-rest-layer"
GEOSERVER_HOST = "https://geoserver.example.com"


auth = ("admin", "password_goes_here")

workspace_name = "geopackager"


def test_get_datastore():

    r = get_datastore(GEOSERVER_HOST, auth[0], auth[1], workspace_name, "rest_datastore")

    print(r.content)


def test_get_layer():

    r = get_layer(GEOSERVER_HOST, auth[0], auth[1], workspace_name, "rest_datastore", "test-layer1")

    print(r.content)


def test_get_feature_types():

    r = get_feature_types(GEOSERVER_HOST, auth[0], auth[1], workspace_name, "my_new_layer", "test-layer")

    print(r.content)


def test_update_feature_types():

    r = update_feature_types(
        GEOSERVER_HOST,
        auth[0],
        auth[1],
        workspace_name,
        "rest_datastore2",
        "test-layer1",
        "this is my description for the abstract",
        ["keyword1", "keyword2"],
    )

    print(r.content)


def test_update_datastore_and_layer():
    geopackage_output_path = os.path.join(current_dir, OUTPUT_DIR)
    geopackage_file_name = f"{LAYERNAME}.gpkg"

    path = os.path.join(geopackage_output_path, geopackage_file_name)

    file = open(path, "rb")

    r = update_datastore_and_layer_from_file(
        GEOSERVER_HOST,
        auth[0],
        auth[1],
        workspace_name,
        "rest_datastore2",
        "test-layer1",
        file,
        "Description",
        ["keyword1", "keyword2"],
    )

    print(r.content)


# test_update_datastore_and_layer()

# test_get_layer()

# test_update_feature_types()

# test_get_feature_types()
