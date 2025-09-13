import React from 'react';

const HotelsList = ({ items = [], loading = false, error = null }) => {
  if (loading) return <div className="text-sm text-gray-600">Loading hotels…</div>;
  if (error) return <div className="text-sm text-red-600">{error}</div>;
  if (!items.length) return <div className="text-sm text-gray-600">No hotels found.</div>;

  return (
    <div className="space-y-3">
      {items.map((h) => (
        <div key={h.id} className="bg-white border rounded-md p-3 flex gap-3 items-start">
          {h.photo && (
            <img src={h.photo} alt={h.name} className="w-16 h-16 object-cover rounded" />
          )}
          <div className="flex-1 min-w-0">
            <div className="font-medium truncate">{h.name}</div>
            <div className="text-xs text-gray-600">{h.neighborhood || ''} {h.stars ? `• ${h.stars}★` : ''}</div>
            <div className="text-sm mt-1">{h.price_per_night?.currency} {h.price_per_night?.amount}</div>
          </div>
          {h.deeplink && (
            <a href={h.deeplink} target="_blank" rel="noreferrer" className="text-blue-600 text-sm">View</a>
          )}
        </div>
      ))}
    </div>
  );
};

export default HotelsList;

