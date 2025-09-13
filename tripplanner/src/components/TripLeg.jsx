import React from 'react';

const TripLeg = ({ leg, index }) => {
  const city = leg.city || leg.name || 'City';
  const days = leg.days || '';
  return (
    <button className="px-3 py-2 rounded-md border bg-white hover:bg-gray-50 text-left">
      <div className="flex items-center gap-2 text-sm">
        <span className="inline-flex items-center justify-center w-5 h-5 text-xs rounded-full bg-gray-200">{(index ?? 0) + 1}</span>
        <span className="font-medium">{city}</span>
      </div>
      <div className="text-xs text-gray-600 mt-1">{days}</div>
    </button>
  );
};

export default TripLeg;
