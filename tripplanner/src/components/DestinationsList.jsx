import React from 'react';

const DestinationsList = ({ items = [], onShowOnMap, onShowAttractions }) => {
  if (!items.length) return <div className="text-sm text-gray-600">No results.</div>;
  return (
    <div className="space-y-3">
      {items.map((d, idx) => (
        <div key={`${d.dest_id}-${idx}`} className="bg-white border rounded-md p-3 flex gap-3 items-start">
          {d.image_url && (
            <img src={d.image_url} alt={d.name} className="w-12 h-12 object-cover rounded" />
          )}
          <div className="flex-1 min-w-0">
            <div className="font-medium truncate">{d.name}</div>
            <div className="text-xs text-gray-600">{d.city_name || ''} {d.region ? `• ${d.region}` : ''} {d.country ? `• ${d.country}` : ''}</div>
          </div>
          <div className="flex gap-2">
            {typeof d.lat === 'number' && typeof d.lon === 'number' && (
              <button className="text-xs text-blue-600" onClick={() => onShowOnMap && onShowOnMap([d])}>Show on map</button>
            )}
            {typeof d.lat === 'number' && typeof d.lon === 'number' && (
              <button className="text-xs text-blue-600" onClick={() => onShowAttractions && onShowAttractions(d)}>Nearby attractions</button>
            )}
          </div>
        </div>
      ))}
      {onShowOnMap && items.some(d => typeof d.lat === 'number' && typeof d.lon === 'number') && (
        <div className="text-right">
          <button className="text-xs text-blue-600" onClick={() => onShowOnMap(items)}>Show all on map</button>
        </div>
      )}
    </div>
  );
};

export default DestinationsList;
