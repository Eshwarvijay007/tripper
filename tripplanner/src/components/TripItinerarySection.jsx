
import React from 'react';
import TripLegsBar from './TripLegsBar';
import DayItinerary from './DayItinerary';

const TripItinerarySection = ({ tripData }) => {
  return (
    <div className="space-y-3">
      <h2 className="text-lg font-semibold">Itinerary</h2>
      <TripLegsBar legs={tripData.legs} />
      <div className="space-y-4">
        {tripData.itinerary.map((itinerary, index) => (
          <DayItinerary key={index} itinerary={itinerary} />
        ))}
      </div>
    </div>
  );
};

export default TripItinerarySection;
