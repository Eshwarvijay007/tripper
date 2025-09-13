import React from 'react';

const AirportsList = ({ items = [], loading = false, error = null }) => {
  if (loading) return <div className="text-sm text-gray-600">Loading airports…</div>;
  if (error) return <div className="text-sm text-red-600">{error}</div>;
  if (!items.length) return <div className="text-sm text-gray-600">No results.</div>;

  return (
    <div className="space-y-3">
      {items.map((a, idx) => (
        <div key={`${a.code}-${idx}`} className="bg-white border rounded-md p-3 flex gap-3 items-start">
          {a.photoUri && (
            <img src={a.photoUri} alt={a.name} className="w-12 h-12 object-cover rounded" />
          )}
          <div className="flex-1 min-w-0">
            <div className="font-medium truncate">{a.name} ({a.code})</div>
            <div className="text-xs text-gray-600">
              {a.cityName || ''} {a.regionName ? `• ${a.regionName}` : ''} {a.country ? `• ${a.country}` : ''}
            </div>
            {a.distanceKm && (
              <div className="text-xs text-gray-500">{a.distanceKm.toFixed ? a.distanceKm.toFixed(1) : a.distanceKm} km from city</div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

export default AirportsList;

