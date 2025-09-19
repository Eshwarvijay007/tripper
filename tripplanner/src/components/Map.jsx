import React, { useEffect, useRef, useState } from 'react';
import { loadGoogleMaps } from '../lib/maps';

const Map = ({ fullHeight = false, markers = [] }) => {
  const ref = useRef(null);
  const [mapsLoaded, setMapsLoaded] = useState(false);
  const [mapsError, setMapsError] = useState(null);
  const previousMarkersRef = useRef([]);
  const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;
  const style = `border rounded-2xl overflow-hidden bg-white ${fullHeight ? 'h-full' : 'h-64'}`;

  useEffect(() => {
    let canceled = false;
    loadGoogleMaps(apiKey)
      .then(() => !canceled && setMapsLoaded(true))
      .catch((err) => {
        if (!canceled) setMapsError(err?.message || 'Failed to load Google Maps');
      });
    return () => {
      canceled = true;
    };
  }, [apiKey]);

  useEffect(() => {
    if (!mapsLoaded || !ref.current) return;
    const g = window.google;
    
    // Check if this is an update to existing map
    const existingMap = ref.current.mapInstance;
    const hasMarkersChanged = JSON.stringify(markers) !== JSON.stringify(previousMarkersRef.current);
    
    if (existingMap && hasMarkersChanged && markers?.length > 0) {
      // Smooth transition for marker changes
      const newCenter = { lat: markers[0].lat, lng: markers[0].lon };
      const newZoom = markers.length === 1 ? 15 : 10;
      
      // Smooth pan and zoom transition
      existingMap.panTo(newCenter);
      if (existingMap.getZoom() !== newZoom) {
        existingMap.setZoom(newZoom);
      }
      
      // Clear existing markers and add new ones
      if (ref.current.markers) {
        ref.current.markers.forEach(marker => marker.setMap(null));
      }
      
      ref.current.markers = [];
      markers.forEach((m) => {
        if (typeof m.lat !== 'number' || typeof m.lon !== 'number') return;
        const pos = { lat: m.lat, lng: m.lon };
        const marker = new g.maps.Marker({ 
          position: pos, 
          map: existingMap, 
          title: m.title || m.name || '',
          animation: g.maps.Animation.DROP
        });
        ref.current.markers.push(marker);
      });
      
      previousMarkersRef.current = markers;
      return;
    }
    
    // Initial map creation
    const center = markers?.length
      ? { lat: markers[0].lat, lng: markers[0].lon }
      : { lat: 20.5937, lng: 78.9629 }; // India default
    
    let zoom = 4; // Default for no markers
    if (markers?.length === 1) {
      zoom = 15; // Close zoom for single hotel/location
    } else if (markers?.length > 1) {
      zoom = 10; // Medium zoom for multiple locations
    }
    
    const map = new g.maps.Map(ref.current, {
      center,
      zoom,
      mapTypeControl: false,
      streetViewControl: false,
    });

    // Store map instance for smooth transitions
    ref.current.mapInstance = map;
    ref.current.markers = [];

    const bounds = new g.maps.LatLngBounds();
    (markers || []).forEach((m) => {
      if (typeof m.lat !== 'number' || typeof m.lon !== 'number') return;
      const pos = { lat: m.lat, lng: m.lon };
      const marker = new g.maps.Marker({ 
        position: pos, 
        map, 
        title: m.title || m.name || '',
        animation: g.maps.Animation.DROP
      });
      ref.current.markers.push(marker);
      bounds.extend(pos);
    });
    
    if (markers?.length > 1) {
      map.fitBounds(bounds);
    }
    
    previousMarkersRef.current = markers;
  }, [mapsLoaded, markers]);

  return (
    <div className={`relative ${style}`}>
      <div ref={ref} className="w-full h-full" />
      {!mapsLoaded && !mapsError && (
        <div className="absolute inset-0 flex items-center justify-center text-sm text-gray-600">Loading map…</div>
      )}
      {mapsError && (
        <div className="absolute inset-0 flex items-center justify-center text-center p-4 text-sm text-red-600">
          {mapsError}. Set VITE_GOOGLE_MAPS_API_KEY in tripplanner/.env and restart dev server.
        </div>
      )}
    </div>
  );
};

export default Map;
