import pathlib
import geopackager.create_geopackage


CURRENT_DIR = pathlib.Path(__file__).parent.absolute()

FILE_NAME = "example_tsgexport.CSV"

LAYERNAME = "test-layer"

DOWNLOADLINK = "https://example.com"


# input_path = os.path.join(CURRENT_DIR, FILE_NAME)
# df = pd.read_csv(input_path)

# df = add_metadata_link(df, DOWNLOADLINK)

# df = add_metadata_keywords(df, [])

# lat_column = guess_lat(list(df.columns))

# long_column = guess_long(list(df.columns))

# validate(df, 'LATITUDE', "LONGITUDE")

# geo_df = df_to_gdf(df, lat_column, long_column)

# works = df.LATITUDE

# no_works = df['LATITUDE']

# geo_df = add_metadata_link(geo_df, DOWNLOADLINK)

# write_shape_file(geo_df, CURRENT_DIR, LAYERNAME)

# write_geopackage_file(geo_df, CURRENT_DIR, LAYERNAME)
