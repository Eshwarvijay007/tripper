import React from 'react';

const TripTitleSection = ({ title, onShowHotels }) => {
  return (
    <div className="space-y-3">
      <div className="flex items-start justify-between">
        <h1 className="text-xl font-semibold leading-tight">{title}</h1>
        <div className="flex items-center gap-2">
          {onShowHotels && (
            <button className="px-3 py-1.5 text-sm border rounded-md" onClick={onShowHotels}>Show Hotels</button>
          )}
          <button className="px-3 py-1.5 text-sm border rounded-md">Download</button>
          <button className="px-3 py-1.5 text-sm border rounded-md">Share</button>
          <button className="px-3 py-1.5 text-sm bg-primary-green text-white rounded-md">Trip Cart</button>
        </div>
      </div>
      <div className="flex items-center gap-2 text-sm text-gray-600">
        <span>May 22 – 27</span>
        <span className="w-px h-4 bg-gray-300" />
        <span>1 traveller</span>
      </div>
    </div>
  );
};

export default TripTitleSection;
