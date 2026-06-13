package infra

import (
	"encoding/json"
	"fmt"
	"io"
	"math"
	"net/http"
	"net/url"
)

type OSRMClient struct {
	baseURL string
	client  *http.Client
}

type RouteResult struct {
	DistanceKm      float64
	DurationSeconds int
	Polyline        string
}

func NewOSRM(baseURL string) *OSRMClient {
	return &OSRMClient{baseURL: baseURL, client: &http.Client{}}
}

func (o *OSRMClient) Route(srcLat, srcLon, dstLat, dstLon float64) (*RouteResult, error) {
	u := fmt.Sprintf("%s/route/v1/driving/%f,%f;%f,%f?overview=simplified&geometries=geojson",
		o.baseURL, srcLon, srcLat, dstLon, dstLat)
	resp, err := o.client.Get(u)
	if err != nil {
		return nil, fmt.Errorf("osrm request: %w", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("osrm read: %w", err)
	}

	var result struct {
		Code   string `json:"code"`
		Routes []struct {
			Distance float64 `json:"distance"`
			Duration float64 `json:"duration"`
			Geometry struct {
				Coordinates [][2]float64 `json:"coordinates"`
			} `json:"geometry"`
		} `json:"routes"`
	}
	if err := json.Unmarshal(body, &result); err != nil {
		return nil, fmt.Errorf("osrm decode: %w", err)
	}
	if result.Code != "Ok" || len(result.Routes) == 0 {
		return nil, fmt.Errorf("osrm error: %s", result.Code)
	}

	route := result.Routes[0]
	// Encode polyline from coordinates
	coords := make([][2]float64, len(route.Geometry.Coordinates))
	for i, c := range route.Geometry.Coordinates {
		coords[i] = [2]float64{c[1], c[0]} // lat, lon
	}
	polyline := encodePolyline(coords)

	return &RouteResult{
		DistanceKm:      math.Round(route.Distance/1000*100) / 100,
		DurationSeconds: int(math.Round(route.Duration)),
		Polyline:        polyline,
	}, nil
}

func (o *OSRMClient) Nearest(lat, lon float64) (*[2]float64, error) {
	u := fmt.Sprintf("%s/nearest/v1/driving/%f,%f?number=1", o.baseURL, lon, lat)
	resp, err := o.client.Get(u)
	if err != nil {
		return nil, fmt.Errorf("osrm nearest request: %w", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("osrm nearest read: %w", err)
	}

	var result struct {
		Code       string `json:"code"`
		Waypoints []struct {
			Location [2]float64 `json:"location"`
		} `json:"waypoints"`
	}
	if err := json.Unmarshal(body, &result); err != nil {
		return nil, fmt.Errorf("osrm nearest decode: %w", err)
	}
	if result.Code != "Ok" || len(result.Waypoints) == 0 {
		return nil, fmt.Errorf("osrm nearest: no waypoints")
	}
	loc := result.Waypoints[0].Location
	return &[2]float64{loc[1], loc[0]}, nil // return [lat, lon]
}

func encodePolyline(points [][2]float64) string {
	var result []byte
	prevLat, prevLon := int64(0), int64(0)
	for _, p := range points {
		lat := int64(math.Round(p[0] * 1e5))
		lon := int64(math.Round(p[1] * 1e5))
		result = append(result, encodeSignedInt(lat-prevLat)...)
		result = append(result, encodeSignedInt(lon-prevLon)...)
		prevLat, prevLon = lat, lon
	}
	return string(result)
}

func encodeSignedInt(v int64) []byte {
	v = v << 1
	if v < 0 {
		v = ^v
	}
	return encodeUnsignedInt(v)
}

func encodeUnsignedInt(v int64) []byte {
	var b []byte
	for v >= 32 {
		b = append(b, byte((v&31)+63))
		v >>= 5
	}
	b = append(b, byte(v+63))
	return b
}

// Haversine fallback
func HaversineKm(lat1, lon1, lat2, lon2 float64) float64 {
	const R = 6371
	dLat := (lat2 - lat1) * math.Pi / 180
	dLon := (lon2 - lon1) * math.Pi / 180
	a := math.Sin(dLat/2)*math.Sin(dLat/2) +
		math.Cos(lat1*math.Pi/180)*math.Cos(lat2*math.Pi/180)*
			math.Sin(dLon/2)*math.Sin(dLon/2)
	return R * 2 * math.Atan2(math.Sqrt(a), math.Sqrt(1-a))
}

// Google polyline encoding
func polylineEncode(coords [][2]float64) string {
	// simple wrapper
	return (&polylineEncoder{}).encode(coords)
}

type polylineEncoder struct {
	result []byte
	prevLat, prevLon int64
}

func (pe *polylineEncoder) encode(coords [][2]float64) string {
	pe.result = pe.result[:0]
	pe.prevLat, pe.prevLon = 0, 0
	for _, p := range coords {
		lat := int64(math.Round(p[0] * 1e5))
		lon := int64(math.Round(p[1] * 1e5))
		pe.writeSigned(lat - pe.prevLat)
		pe.writeSigned(lon - pe.prevLon)
		pe.prevLat, pe.prevLon = lat, lon
	}
	return string(pe.result)
}

func (pe *polylineEncoder) writeSigned(v int64) {
	v = v << 1
	if v < 0 {
		v = ^v
	}
	for v >= 32 {
		pe.result = append(pe.result, byte((v&31)+63))
		v >>= 5
	}
	pe.result = append(pe.result, byte(v+63))
}
