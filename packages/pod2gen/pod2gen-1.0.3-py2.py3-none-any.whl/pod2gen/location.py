# -*- coding: utf-8 -*-
"""
    pod2gen.location
    ~~~~~~~~~~~~~~~

    This module contains Location, which represents a channel or an episode location.

    :copyright: 2021, Slim Beji <mslimbeji@gmail.com>
    :license: FreeBSD and LGPL, see license.* for more details.
"""
import re
import warnings

from lxml import etree


class Location(object):
    """Class representing a Location object.

    By using this class, you can be sure that the location object is formatted correctly.
    and will be correctly used by the associated :class:`~.pod2gen.Podcast` or
    :class:`~.pod2gen.Episode` object.

    Coordinates parsing is in accordance with
    `RFC 5870 <https://datatracker.ietf.org/doc/html/rfc5870>`_
    and basic regular expression are used to parse the :attr:`~.Location.geo` atrribute

    See `podcast-namespace Location
    <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#location>`_
    for an overview of the Location tag.

    Although `RFC 5870 <https://datatracker.ietf.org/doc/html/rfc5870>`_ accepts unknow fields
    like the ``"bar"`` attribute in the geo uri ``"geo:70,20;foo=1.00;bar=white"``,
    pod2gen will not accept it and will raise an error.

    Example::

        >>> from pod2gen import Location
        >>> l = Location("My location", osm="W5013364", geo="geo:37.786971,-122.399677,300;u=100")
        >>> l.text
        'My location'
        >>> l.osm
        'W5013364'
        >>> l.geo
        'geo:37.786971,-122.399677,300;u=100'
        >>> l.latitude
        37.786971
        >>> l.longitude
        -122.399677
        >>> l.altitude
        300
        >>> l.uncertainty
        100
        >>> # Updating geo URI by changing one coordinate
        >>> l.altitude = 400
        >>> l.geo
        'geo:37.786971,-122.399677,400;u=100'
        >>> # Creating a location with coordinate
        >>> l = Location("A second location", latitude=37.786971, longitude=-122.399677)
        >>> l.geo
        'geo:37.786971,-122.399677'
        >>> l.uncertainty = 50
        >>> l.geo
        'geo:37.786971,-122.399677;u=50'
    """

    _accepted_osm_regex = r"^[NRW]\d+(\#\d+)?$"
    _accepted_geo_regex = r"^geo:-?\d+(\.\d*)?,-?\d+(\.\d*)?(,-?\d+(\.\d*)?)?(;crs=[\w\d]+)?(;u=\d+(\.\d*)?)?$"
    _know_crs = ["wgs84"]

    _redundant_parameter_warning = (
        "latitude or longitude or altitude or crs or uncertainty "
        "parameters will be ignored when specifying a geo parameter"
    )

    def __init__(
        self,
        text,
        osm=None,
        geo=None,
        latitude=None,
        longitude=None,
        altitude=None,
        crs=None,
        uncertainty=None,
    ):
        """Create new Location object. See the class description of
        :class:´~pod2gen.transcript.Location`.

        :param text: The tag node value. This is the location to display.
        :type text: str
        :param osm: (Optional) The OpenStreetMap reference of the location.
        :type osm: str or None
        :param geo: (Optional) A geo URI, conformant to RFC 5870.
        :type geo: str or None
        :param latitude: (Optional) The location latitude.
        :type latitude: float or int
        :param longitude: (Optional) The location longitude.
        :type longitude: float or int
        :param altitude: (Optional) The location altitude.
        :type altitude: float or int
        :param crs: (Optional) The Coordinate Reference System Identification (wgs84).
        :type crs: str or None
        :param uncertainty: (Optional) the amount of uncertainty in the location (in meters).
        :type uncertainty: float or int
        """

        self._text = None
        self._osm = None
        self._geo = None
        self._latitude = None
        self._longitude = None
        self._altitude = None
        self._crs = None
        self._uncertainty = None

        self.text = text
        self.osm = osm

        if geo:
            if latitude or longitude or altitude or crs or uncertainty:
                warnings.warn(self._redundant_parameter_warning, stacklevel=2)
        else:
            if latitude and longitude:
                geo = self.build_geo_uri(
                    latitude, longitude, altitude, crs, uncertainty
                )
            elif bool(latitude) ^ bool(longitude):
                raise ValueError(
                    "Either specify a geo uri or both latitude and longitude"
                )

        self.geo = geo

    def build_geo_uri(
        self, latitude, longitude, altitude=None, crs=None, uncertainty=None
    ):
        """Create a geo URI from coordinates inputs.

        :param latitude: The location latitude.
        :type latitude: float or int
        :param longitude: The location longitude.
        :type longitude: float or int
        :param altitude: (Optional) The location altitude.
        :type altitude: float or int
        :param crs: (Optional) The Coordinate Reference System Identification
            (default is ``"wgs84"``).
        :type crs: str
        :param uncertainty: (Optional) the amount of uncertainty in the location (in meters).
        :type uncertainty: float or int

        :returns: :obj:`str`
        """

        if not latitude or not longitude:
            return None

        geo = "geo:%s,%s" % (latitude, longitude)
        if altitude:
            geo = "%s,%s" % (geo, altitude)
        if crs:
            geo = "%s;crs=%s" % (geo, crs)
        if uncertainty:
            geo = "%s;u=%s" % (geo, uncertainty)

        return geo

    def _update_from_geo_uri(self, reset_if_empty=True):
        geo = self.geo
        if geo:
            elements = re.split("[;,:]", geo)
            self.latitude = elements[1]
            self.longitude = elements[2]

            for i in range(3, len(elements)):
                item = elements[i]
                if item.startswith("crs="):
                    self.crs = item[4:]
                elif item.startswith("u="):
                    self.uncertainty = item[2:]
                else:
                    self.altitude = item
        elif reset_if_empty:
            self._latitude = None
            self._longitude = None
            self._altitude = None
            self._crs = None
            self._uncertainty = None

    def _update_from_parameters(
        self, latitude=None, longitude=None, altitude=None, crs=None, uncertainty=None
    ):
        if not latitude:
            latitude = self.latitude
        if not longitude:
            longitude = self.longitude
        if not altitude:
            altitude = self.altitude
        if not crs:
            crs = self.crs
        if not uncertainty:
            uncertainty = self.uncertainty

        geo = self.build_geo_uri(latitude, longitude, altitude, crs, uncertainty)
        self._geo = geo

    def rss_entry(self):
        """Create an RSS ``<podcast:location>`` tag using lxml's etree and return it.

        This is primarily used by both :class:`~.pod2gen.Podcast` and
        :class:`~.pod2gen.Episode` as the location tag parent is either
        the channel (podcast) or item (episode)

        :RSS: ``<podcast:location>``

        :returns: :class:`lxml.etree.Element`
        """

        PODCAST_NS = "https://podcastindex.org/namespace/1.0"

        entry = etree.Element("{%s}location" % PODCAST_NS)
        entry.text = etree.CDATA(self.text)

        if self.geo:
            entry.attrib["geo"] = self.geo
        if self.osm:
            entry.attrib["osm"] = self.osm

        return entry

    @property
    def text(self):
        """The tag ``<podcast:transcript>`` node value. It is meant for podcast
        apps to display the name of the location that the podcast or episode is about.
        It is for display purposes only.

        Check `podcast-namespace Location node value
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#node-value-4>`_
        for more details.

        :type: :obj:`str`
        """
        return self._text

    @text.setter
    def text(self, text):
        if not text:
            raise ValueError("text field of location objects cannot be None or empty")

        if len(text) > 128:
            raise ValueError("Location display text should not exceed 128 characters")

        self._text = text

    @property
    def osm(self):
        """The `Open Street Map <https://en.wikipedia.org/wiki/OpenStreetMap>`_
        identifier of the place.

        Check `podcast-namespace Location osm attribute
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#attributes-6>`_
        for more details.

        :type: :obj:`str` or :obj:`None`
        """
        return self._osm

    @osm.setter
    def osm(self, osm):
        if osm is None:
            self._osm = None
        else:
            if not re.match(self._accepted_osm_regex, osm):
                raise ValueError("%s is not a valid osm reference" % osm)

            self._osm = osm

    @property
    def geo(self):
        """A geo URI, conformant to `RFC 5870 <https://datatracker.ietf.org/doc/html/rfc5870>`_.

        The geo URI indicates all of latitude, longitude, altitude and precision uncertainty of
        the place.

        Check `podcast-namespace Location geo attribute
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#attributes-6>`_
        for more details.

        :type: :obj:`str`
        """
        return self._geo

    @geo.setter
    def geo(self, geo):
        if geo:
            if not re.match(self._accepted_geo_regex, geo):
                raise ValueError("%s is not a valid geo uri" % geo)

            self._geo = geo
            self._update_from_geo_uri()

        else:
            self._geo = None
            self._update_from_geo_uri(reset_if_empty=True)

    @property
    def latitude(self):
        """The latitude in the geo URI, conformant to
        `RFC 5870 <https://datatracker.ietf.org/doc/html/rfc5870>`_.

        :type: :obj:`float`
        """
        return self._latitude

    @latitude.setter
    def latitude(self, latitude):
        if latitude:
            if not isinstance(latitude, int) and not isinstance(latitude, float):
                try:
                    latitude = float(latitude)
                except:
                    raise ValueError(
                        "Latitude value %r could not be converted into a numeric value"
                        % latitude
                    )

            if latitude - int(latitude) == 0:
                latitude = int(latitude)

            self._latitude = latitude
        else:
            self._latitude = None

        self._update_from_parameters()

    @property
    def longitude(self):
        """The longitude in the geo URI, conformant to
        `RFC 5870 <https://datatracker.ietf.org/doc/html/rfc5870>`_.

        :type: :obj:`float`
        """
        return self._longitude

    @longitude.setter
    def longitude(self, longitude):
        if longitude:
            if not isinstance(longitude, int) and not isinstance(longitude, float):
                try:
                    longitude = float(longitude)
                except:
                    raise ValueError(
                        "Longitude value %r could not be converted into a numeric value"
                        % longitude
                    )

            if longitude - int(longitude) == 0:
                longitude = int(longitude)

            self._longitude = longitude
        else:
            self._longitude = None

        self._update_from_parameters()

    @property
    def altitude(self):
        """The altitude in the geo URI, conformant to
        `RFC 5870 <https://datatracker.ietf.org/doc/html/rfc5870>`_

        :type: :obj:`float` or :obj:`None`
        """
        return self._altitude

    @altitude.setter
    def altitude(self, altitude):
        if altitude:
            if not isinstance(altitude, int) and not isinstance(altitude, float):
                try:
                    altitude = float(altitude)
                except:
                    raise ValueError(
                        "Altitude value %r could not be converted into a numeric value"
                        % altitude
                    )

            if altitude - int(altitude) == 0:
                altitude = int(altitude)

            self._altitude = altitude
        else:
            self._altitude = None

        self._update_from_parameters()

    @property
    def crs(self):
        """The coordinate reference system in the geo URI, conformant to
        `RFC 5870 <https://datatracker.ietf.org/doc/html/rfc5870>`_
        The default coordinate reference system used is the
        `World Geodetic System 1984 (WGS-84) <https://en.wikipedia.org/wiki/World_Geodetic_System>`_.

        :type: :obj:`str` or :obj:`None`
        """
        return self._crs

    @crs.setter
    def crs(self, crs):
        if crs:
            crs = crs.lower()
            if crs not in self._know_crs:
                warnings.warn(
                    "The %s coordinate system is unknown or not conformant to RFC 5870 yet"
                    % crs,
                    stacklevel=2,
                )
            self._crs = crs
        else:
            self._crs = None

        self._update_from_parameters()

    @property
    def uncertainty(self):
        """The uncertainty in the geo URI, conformant to
        `RFC 5870 <https://datatracker.ietf.org/doc/html/rfc5870>`_

        :type: :obj:`float` or obj:`None`
        """
        return self._uncertainty

    @uncertainty.setter
    def uncertainty(self, uncertainty):
        if uncertainty:
            if not isinstance(uncertainty, int) and not isinstance(uncertainty, float):
                try:
                    uncertainty = float(uncertainty)
                except:
                    raise ValueError(
                        "Uncertainty value %r could not be converted into a numeric value"
                        % uncertainty
                    )

            if uncertainty < 0:
                raise ValueError(
                    "Uncertainty cannot be negative. Received %r." % uncertainty
                )

            if uncertainty - int(uncertainty) == 0:
                uncertainty = int(uncertainty)

            self._uncertainty = uncertainty
        else:
            self._uncertainty = None

        self._update_from_parameters()

    def __repr__(self):
        return "Location(text=%s, osm=%s, geo=%s)" % (self.text, self.osm, self.geo)
