import React from 'react';

const HotelsList = ({ items = [], loading = false, error = null }) => {
  if (loading) return <div className="text-sm text-gray-600">Loading hotels…</div>;
  if (error) return <div className="text-sm text-red-600">{error}</div>;
  if (!items.length) return <div className="text-sm text-gray-600">No hotels found.</div>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {items.map((h) => {
        const img = h.image_url || h.photo;
        const price = h.price_per_night;
        return (
          <div key={h.id} className="overflow-hidden rounded-xl border bg-white shadow-sm flex flex-col">
            {img && (
              <div className="h-48 w-full overflow-hidden bg-gray-100">
                <img src={img} alt={h.name} className="h-full w-full object-cover" />
              </div>
            )}
            <div className="p-4 flex-1 flex flex-col">
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                  <h4 className="font-semibold text-base truncate">{h.name}</h4>
                  <div className="text-xs text-gray-600 truncate">
                    {h.neighborhood ? h.neighborhood + ' • ' : ''}
                    {h.stars ? `${h.stars}★` : ''}
                  </div>
                </div>
                {price && (
                  <div className="text-sm text-right whitespace-nowrap">
                    <div className="font-medium">{price.currency} {price.amount}</div>
                    <div className="text-gray-600 text-xs">per night (approx)</div>
                  </div>
                )}
              </div>

              {h.description && (
                <p className="text-sm text-gray-700 mt-3 max-h-16 overflow-hidden">{h.description}</p>
              )}

              {h.deeplink && (
                <div className="mt-4">
                  <a href={h.deeplink} target="_blank" rel="noreferrer" className="inline-block text-sm text-white bg-blue-600 hover:bg-blue-700 px-3 py-1.5 rounded">
                    View Details
                  </a>
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default HotelsList;
