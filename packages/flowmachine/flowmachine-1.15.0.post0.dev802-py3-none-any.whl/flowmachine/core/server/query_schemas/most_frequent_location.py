# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marshmallow import fields
from marshmallow.validate import OneOf

from flowmachine.features.subscriber.most_frequent_location import MostFrequentLocation
from .aggregation_unit import AggregationUnitMixin
from .base_query_with_sampling import (
    BaseQueryWithSamplingSchema,
    BaseExposedQueryWithSampling,
)
from .field_mixins import (
    HoursField,
    StartAndEndField,
    EventTypesField,
    SubscriberSubsetField,
)

__all__ = ["MostFrequentLocationSchema", "MostFrequentLocationExposed"]


class MostFrequentLocationExposed(BaseExposedQueryWithSampling):
    def __init__(
        self,
        start_date,
        end_date,
        *,
        aggregation_unit,
        event_types,
        subscriber_subset=None,
        sampling=None,
        hours=None,
    ):
        # Note: all input parameters need to be defined as attributes on `self`
        # so that marshmallow can serialise the object correctly.
        self.start = start_date
        self.stop = end_date
        self.hours = hours
        self.aggregation_unit = aggregation_unit
        self.event_types = event_types
        self.subscriber_subset = subscriber_subset
        self.sampling = sampling

    @property
    def _unsampled_query_obj(self):
        """
        Return the underlying flowmachine daily_location object.

        Returns
        -------
        Query
        """
        return MostFrequentLocation(
            start=self.start,
            stop=self.stop,
            hours=self.hours,
            spatial_unit=self.aggregation_unit,
            table=self.event_types,
            subscriber_subset=self.subscriber_subset,
        )


class MostFrequentLocationSchema(
    StartAndEndField,
    EventTypesField,
    SubscriberSubsetField,
    HoursField,
    AggregationUnitMixin,
    BaseQueryWithSamplingSchema,
):
    # query_kind parameter is required here for claims validation
    query_kind = fields.String(validate=OneOf(["most_frequent_location"]))

    __model__ = MostFrequentLocationExposed
