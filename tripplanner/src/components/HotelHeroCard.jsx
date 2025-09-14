import React from 'react';

const HotelHeroCard = ({ hotel }) => {
  if (!hotel) return null;
  const {
    name,
    image_url,
    photo, // alternate field name if coming from hotels search
    city_name,
    region,
    country,
    price_per_night,
    stars,
    neighborhood,
  } = hotel;

  const img = image_url || photo;
  return (
    <div className="overflow-hidden rounded-xl border bg-white shadow-sm">
      {img && (
        <div className="h-40 w-full overflow-hidden bg-gray-100">
          <img src={img} alt={name} className="h-full w-full object-cover" />
        </div>
      )}
      <div className="p-4">
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0">
            <h4 className="font-semibold truncate">{name}</h4>
            <div className="text-xs text-gray-600 truncate">
              {neighborhood ? neighborhood + ' • ' : ''}
              {city_name || ''} {region ? `• ${region}` : ''} {country ? `• ${country}` : ''}
            </div>
          </div>
          {stars && (
            <div className="text-xs px-2 py-1 rounded bg-yellow-100 text-yellow-800 whitespace-nowrap">{stars}★</div>
          )}
        </div>
        {price_per_night && (
          <div className="mt-2 text-sm">
            <span className="font-medium">{price_per_night.currency} {price_per_night.amount}</span>
            <span className="text-gray-600"> / night</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default HotelHeroCard;

