import React from 'react';

const AttractionsList = ({ items = [], onShowOnMap }) => {
  if (!items.length) return <div className="text-sm text-gray-600">No attractions.</div>;
  return (
    <div className="space-y-3">
      {items.map((a) => (
        <div key={a.id || a.place_id} className="bg-white border rounded-md p-3 flex gap-3 items-start">
          {a.photo && (
            <img src={a.photo} alt={a.name} className="w-12 h-12 object-cover rounded" />
          )}
          <div className="flex-1 min-w-0">
            <div className="font-medium truncate">{a.name}</div>
            <div className="text-xs text-gray-600">{a.score ? `${a.score}★` : ''} {a.user_ratings ? `• ${a.user_ratings} reviews` : ''}</div>
          </div>
          {typeof a.lat === 'number' && typeof a.lon === 'number' && (
            <button className="text-xs text-blue-600" onClick={() => onShowOnMap && onShowOnMap([a])}>Show on map</button>
          )}
        </div>
      ))}
      {onShowOnMap && items.some(x => typeof x.lat === 'number' && typeof x.lon === 'number') && (
        <div className="text-right">
          <button className="text-xs text-blue-600" onClick={() => onShowOnMap(items)}>Show all on map</button>
        </div>
      )}
    </div>
  );
};

export default AttractionsList;

