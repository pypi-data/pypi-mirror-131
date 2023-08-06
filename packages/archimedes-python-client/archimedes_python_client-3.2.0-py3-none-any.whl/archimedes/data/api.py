import json
from http import HTTPStatus
from typing import List, Dict

import pandas as pd
import numpy as np
import requests
from requests.exceptions import HTTPError

# TODO when requests v2.27.0+ is released, we can use JSONDecodeError directly from requests.exceptions
# TODO See https://github.com/psf/requests/pull/5856 for more details
from simplejson import JSONDecodeError

import archimedes
from archimedes.configuration import api_config
from archimedes.auth import archimedes_auth

API_URL = api_config.url
API_VERSION = 2


def get(
    series_ids: List[str],
    price_areas: List[str] = None,
    start: str = None,
    end: str = None,
):
    """Get any number of time series.

    This function can be used to fetch time series from the Archimedes Database.
    To see which series are available, use `list_ids()`.

    Example:
        >>> archimedes.get(
        >>>     series_ids=["NP/AreaPrices"],
        >>>     price_areas=["NO1", "NO2"],
        >>>     start="2020-06-20T04:00:00+00:00",
        >>>     end="2020-06-28T04:00:00+00:00",
        >>> )
        series_id                 NP/AreaPrices
        price_area                          NO1   NO2
        from_dt
        2020-06-20T04:00:00+00:00          1.30  1.30
        2020-06-20T05:00:00+00:00          1.35  1.35
        ...                                 ...   ...
        2020-06-28T03:00:00+00:00          0.53  0.53
        2020-06-28T04:00:00+00:00          0.55  0.55

    Args:
        series_ids (List[str]): The series ids to get.
        price_areas (List[str], optional): The price areas to pick, all price areas if None. Defaults to None.
        start (str, optional): The first datetime to fetch (inclusive). Returns all if None. Defaults to None.
        end (str, optional): The last datetime to fetch (exclusive). Returns all if None. Defaults to None.

    Returns:
        DataFrame with all the time series data

    Raises:
        HTTPError: If an http error occurs when requesting the API.
        NoneAuth: If the user is unauthorized or if the authorization has expired.
    """

    if isinstance(series_ids, str):
        series_ids = [series_ids]

    if isinstance(price_areas, str):
        price_areas = [price_areas]

    if start is None:
        start = archimedes.constants.DATE_LOW
    else:
        start = pd.to_datetime(start)

    if end is None:
        end = archimedes.constants.DATE_HIGH
    else:
        end = pd.to_datetime(end)

    query = {
        "series_ids": series_ids,
        "price_areas": price_areas,
        "start": start,
        "end": end,
        "flatten_columns": True,
    }

    data = _make_api_request(
        f"{API_URL}/v{API_VERSION}/data/get",
        params=query,
    )

    df = pd.DataFrame.from_dict(data)

    row_count = df.shape[0]
    if row_count == 0:
        return df

    df = df.sort_values(by=["from_dt", "version"])

    df = df.pivot_table(
        values="value",
        columns=["series_id", "price_area"],
        index="from_dt",
        aggfunc="last",
    )

    df.index = pd.to_datetime(df.index)

    return df


def get_latest(
    series_ids: List[str],
    price_areas: List[str] = None,
):
    """Get the most recent data for any number of time series.

    This function is similar to `get()`, but only fetches data from the past 48 hours,
    potentially including future hours as well (as in the case of Spot price data).

    @TODO: Add an argument `hours` that allows the 'lookback' period to be extended
    to an arbitrary number of hours.

    Example:
        >>> # Calling this function at 2020-03-15T10:15:00
        >>> archimedes.get_latest(
        >>>     series_ids=["NP/AreaPrices", "NP/ConsumptionImbalancePrices"],
        >>>     price_areas=["NO1"],
        >>> )
        series_id                 NP/AreaPrices  NP/ConsumptionImbalancePrices
        price_area                          NO1                            NO1
        from_dt
        2020-03-14T04:11:00+00:00          1.30                           1.30
        2020-03-14T05:12:00+00:00          1.35                           1.35
        ...                                 ...                            ...
        2020-03-15T22:00:00+00:00          0.53                            NaN
        2020-03-15T23:00:00+00:00          0.55                            NaN

    Args:
        series_ids (List[str]): The series ids to get.
        price_areas (List[str], optional): The price areas to pick, all price areas if None. Defaults to None.

    Returns:
        DataFrame with the latest time series data

    Raises:
        HTTPError: If an http error occurs when requesting the API.
        NoneAuth: If the user is unauthorized or if the authorization has expired.
    """
    now_dt = pd.Timestamp.now(tz="utc")
    start_dt = now_dt - pd.Timedelta(days=2)
    # +14 days should be enough in all cases now:
    end_dt = now_dt + pd.Timedelta(days=14)

    df = get(
        series_ids=series_ids,
        price_areas=price_areas,
        start=start_dt.isoformat(),
        end=end_dt.isoformat(),
    )

    return df


def get_predictions(
    series_ids: List[str] = None, price_areas: List[str] = None, start: str = None, end: str = None
) -> List:
    """Get any number of predictions

    This function can be used to fetch predictions from the Archimedes Database.

    Unlike `archimedes.get`, this will return a list, not a dataframe.

    Example:
        >>> archimedes.get_predictions(
            series_ids=["PX/rk-naive"],
            price_areas=["NO1"],
            start="2020"
        )
        >>> [...]

    Args:
        series_ids (List[str], optional): The series ids to get.
        price_areas (List[str], optional): The price areas to get the data for.
        start (str, optional):
            The first datetime to fetch (inclusive). Returns all if None. Defaults to None.
        end (str, optional):
            The last datetime to fetch (exclusive). Returns all if None. Defaults to None.

    Returns:
        DataFrame with all the prediction data
    """
    if isinstance(series_ids, str):
        series_ids = [series_ids]

    if isinstance(price_areas, str):
        price_areas = [price_areas]

    if start is None:
        start = archimedes.constants.DATE_LOW
    else:
        start = pd.to_datetime(start)

    if end is None:
        end = archimedes.constants.DATE_HIGH
    else:
        end = pd.to_datetime(end)

    query = {"start": start, "end": end}

    if series_ids is not None:
        query["series_ids"] = series_ids

    if price_areas is not None:
        query["price_areas"] = price_areas

    data = _make_api_request(
        f"{API_URL}/v{API_VERSION}/data/get_predictions",
        params=query,
    )

    for item in data:
        json_data = item.get("json_data")
        item.update(json_data)
        del item["json_data"]

    return pd.DataFrame.from_dict(data)


def list_ids(sort: bool = False):
    """List all the series ids available.

    Example:
        >>> archimedes.list_ids()
                                    series_id
        0   NP/NegativeProductionImbalancePrices
        1                    NP/ProductionTotals
        ..                                   ...
        38                 NP/OrdinaryDownVolume
        39                    NP/SpecialUpVolume
    
    Args:
        sort (bool): False - return all series in one dataframe column, True - order dataframe by data-origin
    
    Returns:
        DataFrame with all available list_ids
    """
    data = _make_api_request(
        f"{API_URL}/v{API_VERSION}/data/list_ids",
    )

    series_df = pd.DataFrame.from_dict(data)

    if not sort:
        return series_df

    # get list of data-sources and sort alphabetically
    data_sources = np.unique([ids.split("/")[0] for ids in series_df.values.flatten()])
    data_sources = np.sort(data_sources)

    sorted_df = pd.DataFrame()
    for source in data_sources:
        source_ids = series_df[pd.Series(series_df.values.flatten()).str.startswith(source)]
        # sort series_ids alphabetically and reset dataframe index
        source_ids = source_ids.sort_values(by="series_id")
        source_ids = source_ids.reset_index(drop=True)
        # append column of series_ids to frame
        sorted_df = pd.concat([sorted_df, source_ids], axis=1)

    # set name of columns and replace nans with empty strings
    sorted_df.columns = data_sources
    sorted_df = sorted_df.fillna("")
    return sorted_df.copy()


def list_prediction_ids():
    """List all the prediction series ids available.

    Example:
        >>> archimedes.list_prediction_ids()
                                     series_id
        0               PX/rk-nn-probabilities
        1   PX/rk-nn-direction-probabilities/U
        ..                                ...
        22                           PX/rk-901
        23                         PX/rk-naive
    """

    data = _make_api_request(
        f"{API_URL}/v{API_VERSION}/data/list_prediction_ids"
    )

    return pd.DataFrame.from_dict(data)


def get_predictions_ref_dts(prediction_id: str = None):
    """Get which ref_dts are available.

    ref_dt == prediction_build_dt
    Users views in the database.

    Args:
        prediction_id (str): The series id to get the reference dts for. If None, get ref_dts for all prediction_ids.

    Returns:
        DataFrame with all ref_dts
    """
    query = {}

    if prediction_id:
        query["prediction_id"] = prediction_id

    data = _make_api_request(
        f"{API_URL}/v{API_VERSION}/data/get_predictions_ref_dts",
        params=query,
    )

    return pd.DataFrame.from_dict(data)


def _make_api_request(url, method="GET", *args, **kwargs):
    access_token = archimedes_auth.get_access_token_silent()

    headers = kwargs.pop("headers", None)
    if headers is None:
        headers = {}

    headers.update({"Authorization": f"Bearer {access_token}"})

    r = requests.request(method, url, headers=headers, *args, **kwargs)

    if r.status_code not in [HTTPStatus.OK, HTTPStatus.CREATED]:
        try:
            error_message = r.json().get("detail")
        except JSONDecodeError:
            error_message = r.content
        raise HTTPError(f"API Error: {error_message}")

    return r.json()


def store_prediction(
    prediction_id: str,
    from_dt: pd.Timestamp,
    ref_dt: pd.Timestamp,
    run_dt: pd.Timestamp,
    data: Dict,
):
    """Store a prediction

    Example:
        >>> import archimedes
        >>> import pandas as pd
        >>> from dateutil.tz import gettz
        >>> tz_oslo = gettz("Europe/Oslo")
        >>> prediction_id = "test-prediction-id"
        >>> from_dt = pd.Timestamp("2021-04-11 23:47:16.854775807", tz=tz_oslo)
        >>> ref_dt = pd.Timestamp("2021-04-10 23:00:00.000000000", tz=tz_oslo)
        >>> run_dt = pd.Timestamp.now(tz=tz_oslo)
        >>> data = {"direction": "D", "probability": 0.8632089971077396, "hours_ahead": 1, "price_area": "NO1"}
        >>> archimedes.store_prediction(
        >>>     prediction_id=prediction_id,
        >>>     from_dt=from_dt,
        >>>     ref_dt=ref_dt,
        >>>     run_dt=run_dt,
        >>>     data=data
        >>> )
        True
    """
    payload = {
        "prediction_id": prediction_id,
        "from_dt": from_dt.isoformat(),
        "ref_dt": ref_dt.isoformat(),
        "run_dt": run_dt.isoformat(),
        "data": data,
    }

    ret = _make_api_request(
        f"{API_URL}/v{API_VERSION}/data/store_prediction",
        method="POST",
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"}
    )

    return ret.get("success", False)
