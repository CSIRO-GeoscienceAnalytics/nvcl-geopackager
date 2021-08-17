import pandas as pd
import geopandas as gpd
import os
import pathlib
import shutil

from shapely.geometry import Point

OUTPUT_DIR = "output"


def guess_lat(all_columns):
    likely = next(x for x in all_columns if x.startswith("LATITUDE"))
    if likely:
        return likely
    else:
        likely = next(x for x in all_columns if x.upper().startswith("LAT"))
    return likely


def guess_long(all_columns):
    likely = next(x for x in all_columns if x.startswith("LONGITUDE"))
    if likely:
        return likely
    else:
        likely = next(x for x in all_columns if x.upper().startswith("LONG"))
    return likely


def df_to_gdf(input_df: pd.DataFrame, lat_column: str, long_column: str) -> gpd.GeoDataFrame:
    """
    Convert a DataFrame with longitude and latitude columns
    to a GeoDataFrame.
    """
    # df = input_df.copy()
    geometry = [Point(xy) for xy in zip(input_df.loc[:, long_column], input_df.loc[:, lat_column])]
    return gpd.GeoDataFrame(input_df, crs=4326, geometry=geometry)


def df_to_gdf2(input_df: pd.DataFrame) -> gpd.GeoDataFrame:
    """
    Convert a DataFrame with longitude and latitude columns
    to a GeoDataFrame.
    """
    df = input_df.copy()
    geometry = [Point(xy) for xy in zip(df.LATITUDE, df.LONGITUDE)]
    return gpd.GeoDataFrame(df, crs=4326, geometry=geometry)


def write_shape_file(input_df, base_dir: pathlib.Path, layer_name: str):
    shape_output_path = os.path.join(base_dir, OUTPUT_DIR, layer_name)
    os.makedirs(shape_output_path, exist_ok=True)
    shape_file_name = f"{layer_name}.shp"
    # this will write multiple files to the passed in directory
    input_df.to_file(filename=os.path.join(shape_output_path, shape_file_name), driver="ESRI Shapefile")

    # this will create a zipped file containing all the files above
    shutil.make_archive(os.path.join(base_dir, OUTPUT_DIR, layer_name), "zip", os.path.join(base_dir, OUTPUT_DIR))


def write_geopackage_file(input_df, base_dir: pathlib.Path, layer_name: str):
    geopackage_output_path = os.path.join(base_dir, OUTPUT_DIR)
    os.makedirs(geopackage_output_path, exist_ok=True)
    geopackage_file_name = f"{layer_name}.gpkg"
    input_df.to_file(filename=os.path.join(base_dir, geopackage_file_name), driver="GPKG")


def add_metadata_link(df: pd.DataFrame, collection_link: str) -> pd.DataFrame:
    df["COLLECTION_URI"] = collection_link
    return df


def add_metadata_keywords(df: pd.DataFrame, collection_keywords: list) -> pd.DataFrame:
    if len(collection_keywords) == 1:
        df["KEYWORDS"] = collection_keywords[0]
    elif len(collection_keywords) > 1:
        df["KEYWORDS"] = ",".join(collection_keywords)
    return df


def validate(input_df, lat_column_name, long_column_name):
    messages = []
    in_df = input_df
    selected_lat = lat_column_name
    selected_long = long_column_name
    if in_df is not None:
        if selected_lat is None:
            messages.append("Please select latitude column")
        else:
            if pd.api.types.is_numeric_dtype(in_df[selected_lat]):
                if pd.Series(in_df[selected_lat] < -90).sum() > 0:
                    messages.append("Values in latitude column below -90")
                if pd.Series(in_df[selected_lat] > 90).sum() > 0:
                    messages.append("Values in latitude column above -90")
            else:
                messages.append("Latitude column is not numeric")

        if selected_long is None:
            messages.append("Please select longitude column")
        else:
            if pd.api.types.is_numeric_dtype(in_df[selected_lat]):
                if pd.Series(in_df[selected_long] < -360).sum() > 0:
                    messages.append("Values in longitude column below -360")
                if pd.Series(in_df[selected_long] > 360).sum() > 0:
                    messages.append("Values in longitude column above 360")
            else:
                messages.append("Longitude column is not numeric")
