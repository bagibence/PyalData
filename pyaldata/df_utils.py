import pandas as pd

@property
def index_field_names(df):
    """
    Get what time points are indicated in the trials

    Parameters
    ----------
    df : pd.DataFrame
        data in TrialData format

    Returns
    -------
    list of index names
    """
    return [c for c in df.columns if c.startswith('idx')]

pd.DataFrame.index_field_names = index_field_names


@property
def index_fields(df):
    """
    Return only the index fields of a dataframe

    Parameters
    ----------
    df : pd.DataFrame
        data in TrialData format

    Returns
    -------
    dataframe with only the fields that start with idx
    """
    idx_names = [c for c in df.columns if c.startswith('idx')]

    return df[idx_names]

pd.DataFrame.index_fields = index_fields
