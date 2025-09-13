import React, { useEffect, useRef, useState } from 'react';
import { loadGoogleMaps } from '../lib/maps';

const Map = ({ fullHeight = false, markers = [] }) => {
  const ref = useRef(null);
  const [mapsLoaded, setMapsLoaded] = useState(false);
  const [mapsError, setMapsError] = useState(null);
  const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;
  const style = `border rounded-md bg-white ${fullHeight ? 'h-full' : 'h-64'}`;

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
    const center = markers?.length
      ? { lat: markers[0].lat, lng: markers[0].lon }
      : { lat: 20.5937, lng: 78.9629 }; // India default
    const map = new g.maps.Map(ref.current, {
      center,
      zoom: markers?.length ? 10 : 4,
      mapTypeControl: false,
      streetViewControl: false,
    });

    const bounds = new g.maps.LatLngBounds();
    (markers || []).forEach((m) => {
      if (typeof m.lat !== 'number' || typeof m.lon !== 'number') return;
      const pos = { lat: m.lat, lng: m.lon };
      new g.maps.Marker({ position: pos, map, title: m.title || m.name || '' });
      bounds.extend(pos);
    });
    if (markers?.length > 1) {
      map.fitBounds(bounds);
    }
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
