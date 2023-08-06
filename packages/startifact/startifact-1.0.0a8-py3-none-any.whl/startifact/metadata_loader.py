from json import load
from logging import getLogger
from typing import Dict, List, Optional, cast

from boto3.session import Session

from startifact.bucket_names import BucketNames
from startifact.exceptions import NoRegionsAvailable


class MetadataLoader:
    """
    Loads an artifact's metadata from any available region.
    """

    def __init__(
        self,
        bucket_names: BucketNames,
        key: str,
        regions: List[str],
        metadata: Optional[Dict[str, str]] = None,
    ) -> None:

        self._any_regions_claim_no_metadata = False
        self._bucket_names = bucket_names
        self._cached_metadata = metadata
        self._key = key
        self._logger = getLogger("startifact")
        self._regions = regions

    @property
    def any_regions_claim_no_metadata(self) -> bool:
        return self._any_regions_claim_no_metadata

    def operate(self, session: Session) -> Optional[Dict[str, str]]:
        try:
            bucket = self._bucket_names.get(session)

            self._logger.debug(
                "Downloading metadata from %s/%s in %s.",
                bucket,
                self.key,
                session.region_name,
            )

            s3 = session.client("s3")  # pyright: reportUnknownMemberType=false

            try:
                response = s3.get_object(Bucket=bucket, Key=self.key)
                return cast(Dict[str, str], load(response["Body"]))

            except s3.exceptions.NoSuchKey:
                self._logger.debug("%s claims no metadata.", session.region_name)
                self._any_regions_claim_no_metadata = True
                return None

        except Exception as ex:
            msg = f"Failed to get metadata from {session.region_name}: {ex}"
            self._logger.warning(msg)
            return None

    @property
    def loaded(self) -> Dict[str, str]:
        if self._cached_metadata is not None:
            return self._cached_metadata

        for region in self._regions:
            self._logger.debug("Attempting download from %s…", region)
            session = Session(region_name=region)
            self._cached_metadata = self.operate(session)
            if self._cached_metadata is not None:
                return self._cached_metadata

        if not self._any_regions_claim_no_metadata:
            raise NoRegionsAvailable(self._regions)

        self._logger.debug(
            "No metadata was found. One or more regions explicitly claimed "
            + "that this artifact has no metadata.",
        )

        empty: Dict[str, str] = {}
        self._cached_metadata = empty
        return self._cached_metadata

    @property
    def key(self) -> str:
        return self._key
