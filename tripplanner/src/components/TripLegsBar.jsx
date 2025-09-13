
import React from 'react';
import TripLeg from './TripLeg';

const TripLegsBar = ({ legs }) => {
  return (
    <div className="sticky top-0 z-10 bg-gray-50/80 backdrop-blur border-y">
      <div className="overflow-x-auto">
        <div className="flex gap-2 p-2">
          {legs.map((leg, index) => (
            <TripLeg key={index} leg={leg} index={index} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default TripLegsBar;
