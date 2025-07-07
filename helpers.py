import io
import pandas as pd
import geopandas as gpd
from shapely import wkb
from elasticsearch.exceptions import BadRequestError

# Allow wide columns
pd.set_option('display.max_colwidth', None)

# Convert Well-known Binary to Text
def wkb_to_wkt(wkb_bytes):
    if wkb_bytes is None:
        return None
    try:
        return wkb.loads(wkb_bytes).wkt
    except Exception as e:
        print(f"Error converting WKB: {wkb_bytes} - {e}")
        return None

# Generate a Pandas Dataframe or a Geopandas Dataframe from a ES|QL query
def esql(query, client, geometry_col:str = "geometry", use_arrow:bool = True):
    try:
        # Query ES and create a Pandas Dataframe
        if use_arrow:
            es_response = client.esql.query(query=query.strip(), format="arrow", columnar=True)
            df = es_response.to_pandas()
        else:
            es_response = client.esql.query(query=query.strip(), format="csv")
            df = pd.read_csv(io.StringIO(str(es_response)))
    
        # Promote to a Geopandas Dataframe if a "geometry" column
        if geometry_col in df.columns:
            if use_arrow:
                # Arrow geometries are transferred as WKB
                df[geometry_col] = df[geometry_col].apply(wkb_to_wkt)
            gs = gpd.GeoSeries.from_wkt(df[geometry_col])
            gdf = gpd.GeoDataFrame(df, geometry=gs, crs="EPSG:4326")
            if geometry_col != "geometry":
                gdf.drop(columns="geometry")
            return gdf
        else:
            return df
    except BadRequestError as e:
        print("Something went wrong!")
        print(e.message)
        print("\r\n".join([c['reason'] for c in e.info['error']['root_cause']]))
