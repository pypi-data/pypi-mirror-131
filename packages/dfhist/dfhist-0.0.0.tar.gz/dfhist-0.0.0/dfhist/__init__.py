from datetime import datetime as dt
from functools import wraps
from glob import glob
from os import getcwd
from os.path import getctime, join
from typing import Optional, Callable, List, Any

import pandas as pd


class DFHist:
    def __init__(
        self,
        *,
        directory: str = None,
        expire: Optional[int] = None,
        format: str = "{timestamp}.csv",
        tsformatter: Optional[Callable[[], str]] = None,
        method="csv",
        marshal_params=None,
        unmarshal_params=None,
    ):
        self.directory = directory if directory is not None else getcwd()
        if expire is not None and expire < 0:
            raise ValueError("expire must be nonnegative")

        self.expiry = expire
        self.format = format
        if tsformatter is not None:
            self.tsformatter = tsformatter
        else:
            self.tsformatter = lambda: dt.strftime(
                dt.now(), "%Y-%m-%d-%H:%M:%S"
            )

        self.method = method

        if marshal_params is not None:
            self.marshal_params = marshal_params
        else:
            if self.method == "csv":
                self.marshal_params = {"index": False}
            else:
                raise NotImplementedError

        if unmarshal_params is not None:
            self.unmarshal_params = unmarshal_params
        else:
            if self.method == "csv":
                self.unmarshal_params = {}
            else:
                raise NotImplementedError

    def marshal(self, df: pd.DataFrame) -> str:
        path = join(
            self.directory,
            self.format.format(timestamp=self.tsformatter()),
        )
        if self.method == "csv":
            df.to_csv(path, **self.marshal_params)
            return path
        else:
            raise NotImplementedError

    def unmarshal(self, path) -> pd.DataFrame:
        if self.method == "csv":
            return pd.read_csv(path, **self.unmarshal_params)
        else:
            raise NotImplementedError

    def paths_to_versions(self) -> List[str]:
        return sorted(
            glob(join(self.directory, self.format.format(timestamp="*"))),
            key=getctime,
        )

    def __call__(self, f):
        return wraps(f)(VersionedFunc(f, self))


class VersionedFunc:
    """Given a function f that produces a pandas dataframe, this is a
    'versioned' form of f that might instead use a cached result, and is able
    to save to the version history. If desired, a refresh can be demanded by
    invoking .force(*args, **kwargs).
    """

    def __init__(self, f: Callable[[Any], pd.DataFrame], dfhist: DFHist):
        self.f = f
        self.dfhist = dfhist

    def __call__(self, *args, **kwargs):
        refresh = True

        versions = self.dfhist.paths_to_versions()
        if versions:
            elapsed = dt.now() - dt.utcfromtimestamp(getctime(versions[-1]))
            if (
                self.dfhist.expiry is None
                or elapsed.seconds < self.dfhist.expiry
            ):
                refresh = False

        if refresh:
            df = self.f(*args, **kwargs)
            self.dfhist.marshal(df)
            return df
        else:
            return self.retrieve()

    def retrieve(self):
        """Retrieve the most recent version of f, without reloading."""
        versions = self.dfhist.paths_to_versions()
        most_recent_version = versions[-1]
        return self.dfhist.unmarshal(most_recent_version)

    def force(self, *args, **kwargs):
        """Force an update and save the result."""
        df = self.f(*args, **kwargs)
        self.dfhist.marshal(df)
        return df
