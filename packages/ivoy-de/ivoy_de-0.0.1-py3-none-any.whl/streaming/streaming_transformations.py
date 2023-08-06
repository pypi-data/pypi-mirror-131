from datetime import datetime
import pytz


class Transformations:
    def date_to_utc(self, epoch=None, date_local=None) -> str:
        """Function to convert date epoch and local time to UTC.

        Args:
            epoch (int, optional): Epoch timestamp. Defaults to None.
            date_local (datetime, optional): Local datetime. Defaults to None.

        Returns:
            str: Datetime in UTC format parsed to string.
        """
        if epoch is not None:
            local = pytz.timezone("America/Mexico_City")
            local_time = datetime.utcfromtimestamp(epoch / 1000)
            local_dt = local.localize(local_time, is_dst=None)
            utc_dt = local_dt.astimezone(pytz.utc)
            return utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        if date_local is not None:
            return date_local.strftime("%Y-%m-%dT%H:%M:%SZ")

        if epoch is None and date_local is None:
            return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
