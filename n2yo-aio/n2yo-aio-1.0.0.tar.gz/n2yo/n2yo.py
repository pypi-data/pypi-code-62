import aiohttp

from .satellite_categories import N2YOSatelliteCategory

API_URL = 'https://www.n2yo.com/rest/v1/satellite/'


class N2YO:
    def __init__(self, api_key, latitude=None, longitude=None, altitude=None):
        self.api_key = api_key
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.transactions_count = 0
        self.params = {'apiKey': self.api_key}

        # Initialize aiohttp session
        self.session = aiohttp.ClientSession()

    async def get_tle(self, id):
        '''
        Retrieve the Two Line Elements (TLE) for a satellite identified by NORAD id.

        Request: /tle/{id}

        Parameter	Type	Required	Comments
        id	integer	Yes	NORAD id

        Response:

        Parameter	        Type	Comments
        satid	            integer	NORAD id used in input
        satname	            string	Satellite name
        transactionscount	integer	Count of transactions performed with this API key in last 60 minutes
        tle	                string	TLE on single line string. Split the line in two by \r\n to get original two lines
        '''
        async with self.session.get(
            f'{API_URL}tle/{id}',
            params=self.params
        ) as r:
            response = await r.json()

        self.transactions_count = response['info']['transactionscount']

        return response['info'], response['tle']

    async def get_satellite_positions(
        self, id, seconds,
        latitude=None, longitude=None, altitude=None
    ):
        '''
        Retrieve the future positions of any satellite as footprints (latitude, longitude) to display orbits on maps. Also return the satellite's azimuth and elevation with respect to the observer location. Each element in the response array is one second of calculation. First element is calculated for current UTC time.

        Request: /positions/{id}/{observer_lat}/{observer_lng}/{observer_alt}/{seconds}

        Parameter	    Type	Required	Comments
        id	            integer	Yes	        NORAD id
        observer_lat	float	Yes	        Observer's latitide (decimal degrees format)
        observer_lng	float	Yes	        Observer's longitude (decimal degrees format)
        observer_alt	float	Yes	        Observer's altitude above sea level in meters
        seconds	        integer	Yes	        Number of future positions to return. Each second is a position. Limit 300 seconds

        Response:

        Parameter	        Type	Comments
        satid	            integer	NORAD id used in input
        satname	            string	Satellite name
        transactionscount	integer	Count of transactions performed with this API key in last 60 minutes
        satlatitude	        float	Satellite footprint latitude (decimal degrees format)
        satlongitude	    float	Satellite footprint longitude (decimal degrees format)
        azimuth	            float	Satellite azimuth with respect to observer's location (degrees)
        elevation	        float	Satellite elevation with respect to observer's location (degrees)
        ra	                float	Satellite right angle (degrees)
        dec	                float	Satellite declination (degrees)
        timestamp	        integer	Unix time for this position (seconds). You should convert this UTC value to observer's time zone
        '''
        if latitude is None:
            latitude = self.latitude
        if longitude is None:
            longitude = self.longitude
        if altitude is None:
            altitude = self.altitude

        async with self.session.get(
            f'{API_URL}positions/{id}/{latitude}/{longitude}/{altitude}/{seconds}',
            params=self.params
        ) as r:
            response = await r.json()

        self.transactions_count = response['info']['transactionscount']

        positions = []
        azels = []
        radecs = []
        timestamps = []
        for ii, pos in enumerate(response['positions']):
            positions.append([
                pos['satlatitude'],
                pos['satlongitude'],
                pos['sataltitude']
            ])
            azels.append([pos['azimuth'], pos['elevation']])
            radecs.append([pos['ra'], pos['dec']])
            timestamps.append(pos['timestamp'])

        ans = {
            'timestamps': timestamps,
            'positions': positions,
            'azels': azels,
            'radecs': radecs
        }

        return response['info'], ans

    async def get_visual_passes(
        self, id, days, min_visibility,
        latitude=None, longitude=None, altitude=None
    ):
        '''
        Get predicted visual passes for any satellite relative to a location on Earth. A 'visual pass' is a pass that should be optically visible on the entire (or partial) duration of crossing the sky. For that to happen, the satellite must be above the horizon, illumintaed by Sun (not in Earth shadow), and the sky dark enough to allow visual satellite observation.

        Request: /visualpasses/{id}/{observer_lat}/{observer_lng}/{observer_alt}/{days}/{min_visibility}

        Parameter	    Type	Required	Comments
        id	            integer	Yes	        NORAD id
        observer_lat	float	Yes	        Observer's latitide (decimal degrees format)
        observer_lng	float	Yes	        Observer's longitude (decimal degrees format)
        observer_alt	float	Yes	        Observer's altitude above sea level in meters
        days	        integer	Yes	        Number of days of prediction (max 10)
        min_visibility	integer	Yes	        Minimum number of seconds the satellite should be considered optically visible during the pass to be returned as result

        Response:

        Parameter	        Type	Comments
        satid	            integer	NORAD id used in input
        satname	            string	Satellite name
        transactionscount	integer	Count of transactions performed with this API key in last 60 minutes
        passescount	        integer	Count of passes returned
        startAz	            float	Satellite azimuth for the start of this pass (relative to the observer, in degrees)
        startAzCompass	    string	Satellite azimuth for the start of this pass (relative to the observer). Possible values: N, NE, E, SE, S, SW, W, NW
        startEl	            float	Satellite elevation for the start of this pass (relative to the observer, in degrees)
        startUTC	        integer	Unix time for the start of this pass. You should convert this UTC value to observer's time zone
        maxAz	            float	Satellite azimuth for the max elevation of this pass (relative to the observer, in degrees)
        maxAzCompass	    string	Satellite azimuth for the max elevation of this pass (relative to the observer). Possible values: N, NE, E, SE, S, SW, W, NW
        maxEl	            float	Satellite max elevation for this pass (relative to the observer, in degrees)
        maxUTC	            integer	Unix time for the max elevation of this pass. You should convert this UTC value to observer's time zone
        endAz	            float	Satellite azimuth for the end of this pass (relative to the observer, in degrees)
        endAzCompass	    string	Satellite azimuth for the end of this pass (relative to the observer). Possible values: N, NE, E, SE, S, SW, W, NW
        endEl	            float	Satellite elevation for the end of this pass (relative to the observer, in degrees)
        endUTC	            integer	Unix time for the end of this pass. You should convert this UTC value to observer's time zone
        mag	                float	Max visual magnitude of the pass, same scale as star brightness. If magnitude cannot be determined, the value is 100000
        duration	        integer	Total visible duration of this pass (in seconds)
        '''
        if latitude is None:
            latitude = self.latitude
        if longitude is None:
            longitude = self.longitude
        if altitude is None:
            altitude = self.altitude

        async with self.session.get(
            f'{API_URL}visualpasses/{id}/{latitude}/{longitude}/{altitude}/{days}/{min_visibility}',
            params=self.params
        ) as r:
            response = await r.json()

        self.transactions_count = response['info']['transactionscount']

        if 'passes' in response.keys():
            passes = response['passes']
        else:
            passes = []

        return response['info'], passes

    async def get_radio_passes(
        self, id, days, min_elevation,
        latitude=None, longitude=None, altitude=None
    ):
        '''
        The 'radio passes' are similar to 'visual passes', the only difference being the requirement for the objects to be optically visible for observers. This function is useful mainly for predicting satellite passes to be used for radio communications. The quality of the pass depends essentially on the highest elevation value during the pass, which is one of the input parameters.

        Request: /radiopasses/{id}/{observer_lat}/{observer_lng}/{observer_alt}/{days}/{min_elevation}

        Parameter	    Type	Required	Comments
        id	            integer	Yes	        NORAD id
        observer_lat	float	Yes	        Observer's latitide (decimal degrees format)
        observer_lng	float	Yes	        Observer's longitude (decimal degrees format)
        observer_alt	float	Yes	        Observer's altitude above sea level in meters
        days	        integer	Yes	        Number of days of prediction (max 10)
        min_elevation	integer	Yes	        The minimum elevation acceptable for the highest altitude point of the pass (degrees)

        Response:

        Parameter	        Type	Comments
        satid	            integer	NORAD id used in input
        satname	            string	Satellite name
        transactionscount	integer	Count of transactions performed with this API key in last 60 minutes
        passescount	        integer	Count of passes returned
        startAz	            float	Satellite azimuth for the start of this pass (relative to the observer, in degrees)
        startAzCompass	    string	Satellite azimuth for the start of this pass (relative to the observer). Possible values: N, NE, E, SE, S, SW, W, NW
        startUTC	        integer	Unix time for the start of this pass. You should convert this UTC value to observer's time zone
        maxAz	            float	Satellite azimuth for the max elevation of this pass (relative to the observer, in degrees)
        maxAzCompass	    string	Satellite azimuth for the max elevation of this pass (relative to the observer). Possible values: N, NE, E, SE, S, SW, W, NW
        maxEl	            float	Satellite max elevation for this pass (relative to the observer, in degrees)
        maxUTC	            integer	Unix time for the max elevation of this pass. You should convert this UTC value to observer's time zone
        endAz	            float	Satellite azimuth for the end of this pass (relative to the observer, in degrees)
        endAzCompass	    string	Satellite azimuth for the end of this pass (relative to the observer). Possible values: N, NE, E, SE, S, SW, W, NW
        endUTC	            integer	Unix time for the end of this pass. You should convert this UTC value to observer's time zone
        '''
        if latitude is None:
            latitude = self.latitude
        if longitude is None:
            longitude = self.longitude
        if altitude is None:
            altitude = self.altitude

        async with self.session.get(
            f'{API_URL}radiopasses/{id}/{latitude}/{longitude}/{altitude}/{days}/{min_elevation}',
            params=self.params
        ) as r:
            response = await r.json()

        self.transactions_count = response['info']['transactionscount']

        if 'passes' in response.keys():
            passes = response['passes']
        else:
            passes = []

        return response['info'], passes

    async def get_above(
        self,
        search_radius=90,
        category_id=N2YOSatelliteCategory.All,
        latitude=None,
        longitude=None,
        altitude=None
    ):
        '''
        The 'above' function will return all objects within a given search radius above observer's location. The radius (θ), expressed in degrees, is measured relative to the point in the sky directly above an observer (azimuth).

        Request: /above/{observer_lat}/{observer_lng}/{observer_alt}/{search_radius}/{category_id}

        Parameter	    Type	Required	Comments
        observer_lat	float	Yes	        Observer's latitide (decimal degrees format)
        observer_lng	float	Yes	        Observer's longitude (decimal degrees format)
        observer_alt	float	Yes	        Observer's altitude above sea level in meters
        search_radius	integer	Yes	        Search radius (0-90)
        category_id	    integer	Yes	        Category id (see table). Use 0 for all categories

        Response:

        Parameter	        Type	Comments
        category	        string	Category name (ANY if category id requested was 0)
        transactionscount	integer	Count of transactions performed with this API key in last 60 minutes
        satcount	        integer	Count of satellites returned
        startAz	            float	Satellite azimuth for the start of this pass (relative to the observer, in degrees)
        satid	            integer	Satellite NORAD id
        intDesignator	    string	Satellite international designator
        satname	            string	Satellite name
        launchDate	        string	Satellite launch date (YYYY-MM-DD)
        satlat	            float	Satellite footprint latitude (decimal degrees format)
        satlat	            float	Satellite footprint longitude (decimal degrees format)
        satlat	            float	Satellite altitude (km)

        '''
        if latitude is None:
            latitude = self.latitude
        if longitude is None:
            longitude = self.longitude
        if altitude is None:
            altitude = self.altitude

        async with self.session.get(
            f'{API_URL}above/{latitude}/{longitude}/{altitude}/{search_radius}/{category_id}',
            params=self.params
        ) as r:
            response = await r.json()

        self.transactions_count = response['info']['transactionscount']

        if 'above' in response.keys():
            above = response['above']
        else:
            above = []

        return response['info'], above
