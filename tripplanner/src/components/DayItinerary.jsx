import React, { useState } from 'react';

const DayItinerary = ({ itinerary }) => {
  const [expanded, setExpanded] = useState(false);
  return (
    <div className="border rounded-md bg-white">
      <div className="p-4 space-y-2">
        <div className="flex items-baseline justify-between gap-3">
          <div className="font-medium">Day {itinerary.day}: {itinerary.title}</div>
          <div className="text-xs text-gray-500 whitespace-nowrap">{itinerary.date}</div>
        </div>
        <div className="text-sm text-gray-800 leading-6">
          <div style={!expanded ? { maxHeight: '72px', overflow: 'hidden' } : undefined}>
            {itinerary.description}
          </div>
          <button className="text-blue-600 text-sm mt-1" onClick={() => setExpanded(v => !v)}>
            {expanded ? 'Show less' : '... Read more'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default DayItinerary;
