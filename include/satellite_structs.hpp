#ifndef SATELLITE_STRUCTS_HPP
#define SATELLITE_STRUCTS_HPP

namespace Terminal {

struct Info {
    int satid;                     // NORAD ID used in input
    std::string satname;           // Satellite name
    int transactionscount;         // Count of transactions performed with this API key in last 60 minutes

    // Additional fields specific to certain responses
    std::string category;          // Category name (ANY if category id requested was 0)
    int passescount;               // Count of passes returned
    int satcount;                  // Count of satellites returned
};    

struct TLEResponse {
    Info info;                     // Common info section
    std::string tle;              // Two Line Elements on a single line string. Split by \r\n to get original two lines
};

// Structure representing a single satellite position at a specific timestamp
struct SatellitePosition {
    float satlatitude;            // Satellite footprint latitude (decimal degrees format)
    float satlongitude;           // Satellite footprint longitude (decimal degrees format)
    float sataltitude;            // Satellite altitude in meters
    float azimuth;                // Satellite azimuth with respect to observer's location (degrees)
    float elevation;              // Satellite elevation with respect to observer's location (degrees)
    float ra;                     // Satellite right ascension (degrees)
    float dec;                    // Satellite declination (degrees)
    int timestamp;                // Unix time for this position (seconds). Convert to observer's time zone
};

// Response structure for the Get Satellite Positions API endpoint
struct SatellitePositionsResponse {
    Info info;                                     // Common info section
    std::vector<SatellitePosition> positions;      // Array of satellite positions, each representing one second of calculation
};

// Structure representing a single visual pass of a satellite
struct VisualPass {
    float startAz;                 // Satellite azimuth for the start of this pass (degrees)
    std::string startAzCompass;    // Satellite azimuth compass direction for the start of this pass (N, NE, E, SE, S, SW, W, NW)
    float startEl;                 // Satellite elevation for the start of this pass (degrees)
    int startUTC;                  // Unix time for the start of this pass. Convert to observer's time zone

    float maxAz;                   // Satellite azimuth for the max elevation of this pass (degrees)
    std::string maxAzCompass;      // Satellite azimuth compass direction for the max elevation of this pass (N, NE, E, SE, S, SW, W, NW)
    float maxEl;                   // Satellite max elevation for this pass (degrees)
    int maxUTC;                    // Unix time for the max elevation of this pass. Convert to observer's time zone

    float endAz;                   // Satellite azimuth for the end of this pass (degrees)
    std::string endAzCompass;      // Satellite azimuth compass direction for the end of this pass (N, NE, E, SE, S, SW, W, NW)
    float endEl;                   // Satellite elevation for the end of this pass (degrees)
    int endUTC;                    // Unix time for the end of this pass. Convert to observer's time zone

    float mag;                     // Max visual magnitude of the pass, same scale as star brightness. If undetermined, value is 100000
    int duration;                  // Total visible duration of this pass (seconds)
};

// Response structure for the Get Visual Passes API endpoint
struct VisualPassesResponse {
    Info info;                         // Common info section
    std::vector<VisualPass> passes;    // Array of visual passes returned
};

// Structure representing a single radio pass of a satellite
struct RadioPass {
    float startAz;                 // Satellite azimuth for the start of this pass (degrees)
    std::string startAzCompass;    // Satellite azimuth compass direction for the start of this pass (N, NE, E, SE, S, SW, W, NW)
    int startUTC;                  // Unix time for the start of this pass. Convert to observer's time zone

    float maxAz;                   // Satellite azimuth for the max elevation of this pass (degrees)
    std::string maxAzCompass;      // Satellite azimuth compass direction for the max elevation of this pass (N, NE, E, SE, S, SW, W, NW)
    float maxEl;                   // Satellite max elevation for this pass (degrees)
    int maxUTC;                    // Unix time for the max elevation of this pass. Convert to observer's time zone

    float endAz;                   // Satellite azimuth for the end of this pass (degrees)
    std::string endAzCompass;      // Satellite azimuth compass direction for the end of this pass (N, NE, E, SE, S, SW, W, NW)
    int endUTC;                    // Unix time for the end of this pass. Convert to observer's time zone
};

// Response structure for the Get Radio Passes API endpoint
struct RadioPassesResponse {
    Info info;                         // Common info section
    std::vector<RadioPass> passes;     // Array of radio passes returned
};

// Structure representing a single satellite above the observer's location
struct SatelliteAbove {
    int satid;                     // Satellite NORAD ID
    std::string satname;           // Satellite name
    std::string intDesignator;     // Satellite international designator
    std::string launchDate;        // Satellite launch date (YYYY-MM-DD)
    float satlat;                  // Satellite footprint latitude (decimal degrees format)
    float satlng;                  // Satellite footprint longitude (decimal degrees format)
    float satalt;                  // Satellite altitude (km)
};

// Response structure for the What's Up? (above) API endpoint
struct SatelliteAboveResponse {
    Info info;                             // Common info section
    std::vector<SatelliteAbove> above;     // Array of satellites above the observer's location
};

}

#endif 