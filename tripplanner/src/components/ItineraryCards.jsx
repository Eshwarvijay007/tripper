import React, { useState, useRef } from "react";

// MapPin icon component
const MapPin = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
  </svg>
);

// Format price in INR
const formatINR = (amount) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0
  }).format(amount);
};

const ItineraryCards = ({ tripPlan, onLocationClick }) => {
  const [showAllHotels, setShowAllHotels] = useState(false);
  
  const [selectedDayIndex, setSelectedDayIndex] = useState(0);
  const scrollContainerRef = useRef(null);
  const [showLeftArrow, setShowLeftArrow] = useState(false);
  const [showRightArrow, setShowRightArrow] = useState(false);

  // Check scroll position and update arrow visibility
  const checkScrollButtons = () => {
    if (scrollContainerRef.current) {
      const { scrollLeft, scrollWidth, clientWidth } =
        scrollContainerRef.current;
      setShowLeftArrow(scrollLeft > 0);
      setShowRightArrow(scrollLeft < scrollWidth - clientWidth - 1);
    }
  };

  // Scroll left/right functions
  const scrollLeft = () => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollBy({ left: -200, behavior: "smooth" });
    }
  };

  const scrollRight = () => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollBy({ left: 200, behavior: "smooth" });
    }
  };

  // Initialize scroll buttons on mount and when days change
  React.useEffect(() => {
    checkScrollButtons();
    const handleResize = () => checkScrollButtons();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, [tripPlan]);

  if (!tripPlan || !tripPlan.trip_plan) {
    return null;
  }

  const { trip_plan: days, stay_plan: hotels } = tripPlan;
  const selectedDay = days[selectedDayIndex];
  
  // Generate realistic pricing for hotels and sort by price
  const generateRealisticPricing = (hotel, index) => {
    // Generate varied prices based on hotel name hash and index
    const hash = hotel.name.split('').reduce((a, b) => {
      a = ((a << 5) - a) + b.charCodeAt(0);
      return a & a;
    }, 0);
    
    // Hotel name-based pricing logic for more realism
    const hotelName = hotel.name.toLowerCase();
    let baseTier = 1; // Default to mid-range
    
    // Budget indicators
    if (hotelName.includes('inn') || hotelName.includes('lodge') || hotelName.includes('hostel')) {
      baseTier = 0;
    }
    // Luxury indicators  
    else if (hotelName.includes('luxury') || hotelName.includes('grand') || hotelName.includes('palace') || 
             hotelName.includes('resort') || hotelName.includes('oberoi') || hotelName.includes('taj') ||
             hotelName.includes('five star') || hotelName.includes('presidential')) {
      baseTier = 3;
    }
    // Premium indicators
    else if (hotelName.includes('premium') || hotelName.includes('deluxe') || hotelName.includes('suites') ||
             hotelName.includes('boutique') || hotelName.includes('executive')) {
      baseTier = 2;
    }
    // Rating-based adjustment
    if (hotel.rating >= 4.5) baseTier = Math.max(baseTier, 2); // Min premium for high ratings
    else if (hotel.rating >= 4.0) baseTier = Math.max(baseTier, 1); // Min mid-range
    
    // Create different price tiers
    const priceTiers = [
      { min: 85, max: 160, label: 'Budget' },      // Budget hotels
      { min: 160, max: 290, label: 'Mid-range' },  // Mid-range hotels  
      { min: 290, max: 480, label: 'Premium' },    // Premium hotels
      { min: 480, max: 750, label: 'Luxury' }     // Luxury hotels
    ];
    
    // Apply some randomness but keep it reasonable
    const finalTier = (baseTier + Math.abs(hash) % 2) % priceTiers.length;
    const tier = priceTiers[finalTier];
    
    // Add variance within the tier for each hotel
    const variance = (Math.abs(hash + index) % 60) - 30; // -30 to +30
    const minPrice = Math.max(tier.min + variance, tier.min - 20);
    const maxPrice = Math.max(minPrice + 50, tier.max + variance);
    
    return {
      range_min: Math.round(minPrice),
      range_max: Math.round(maxPrice),
      tier: tier.label
    };
  };
  
  // Add realistic pricing to hotels if not already present
  const hotelsWithPricing = hotels?.map((hotel, index) => ({
    ...hotel,
    pricing: hotel.pricing || generateRealisticPricing(hotel, index)
  })) || [];
  
  // Sort hotels by price (low to high)
  const sortedHotels = [...hotelsWithPricing].sort((a, b) => {
    const priceA = a.pricing?.range_min || 0;
    const priceB = b.pricing?.range_min || 0;
    return priceA - priceB;
  });
  
  // Determine how many hotels to show
  const hotelsToShow = showAllHotels ? sortedHotels : sortedHotels.slice(0, 3);

  return (
    <div className="space-y-6">
      {/* Horizontal scrollable day tabs */}
      <div className="bg-white border border-gray-200 rounded-2xl shadow-sm overflow-hidden">
        {/* Day tabs header */}
        <div className="border-b border-gray-100 relative">
          {/* Left scroll arrow */}
          {showLeftArrow && (
            <button
              onClick={scrollLeft}
              className="absolute left-2 top-1/2 -translate-y-1/2 z-10 w-8 h-8 bg-white shadow-md rounded-full flex items-center justify-center hover:bg-gray-50 transition-colors"
            >
              <svg
                className="w-4 h-4 text-gray-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M15 19l-7-7 7-7"
                />
              </svg>
            </button>
          )}

          {/* Right scroll arrow */}
          {showRightArrow && (
            <button
              onClick={scrollRight}
              className="absolute right-2 top-1/2 -translate-y-1/2 z-10 w-8 h-8 bg-white shadow-md rounded-full flex items-center justify-center hover:bg-gray-50 transition-colors"
            >
              <svg
                className="w-4 h-4 text-gray-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 5l7 7-7 7"
                />
              </svg>
            </button>
          )}

          <div
            ref={scrollContainerRef}
            className="flex overflow-x-auto scrollbar-hide"
            onScroll={checkScrollButtons}
            style={{ scrollbarWidth: "none", msOverflowStyle: "none" }}
          >
            {days.map((day, index) => (
              <button
                key={day.day || index}
                onClick={() => setSelectedDayIndex(index)}
                className={`flex-shrink-0 px-4 py-3 border-b-2 transition-all duration-200 ${
                  selectedDayIndex === index
                    ? "border-black"
                    : "border-transparent hover:bg-gray-50"
                }`}
              >
                <div className="flex items-center gap-2">
                  <div
                    className={`w-6 h-6 rounded-full flex items-center justify-center font-medium text-xs transition-colors ${
                      selectedDayIndex === index
                        ? "bg-black text-white"
                        : "bg-gray-200 text-gray-700"
                    }`}
                  >
                    {day.day}
                  </div>
                  <span
                    className={`font-medium whitespace-nowrap text-sm ${
                      selectedDayIndex === index
                        ? "text-gray-900"
                        : "text-gray-600"
                    }`}
                  >
                    Day {day.day}
                  </span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Selected day content */}
        {selectedDay && (
          <div className="p-6">
            <div className="space-y-4">
              {selectedDay.locations?.map((location, locIndex) => (
                <div
                  key={locIndex}
                  className="flex gap-4 p-4 rounded-xl transition-all duration-200 cursor-pointer location-card hover:shadow-sm"
                  onClick={() => onLocationClick && onLocationClick(location)}
                >
                  {/* Location image */}
                  <div className="flex-shrink-0">
                    {location.photo_url ? (
                      <img
                        src={location.photo_url}
                        alt={location.name}
                        className="w-20 h-20 rounded-lg object-cover"
                        onError={(e) => {
                          e.target.style.display = "none";
                        }}
                      />
                    ) : (
                      <div className="w-20 h-20 rounded-lg bg-gradient-to-br from-gray-200 to-gray-300 flex items-center justify-center">
                        <svg
                          className="w-8 h-8 text-gray-400"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                          />
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
                          />
                        </svg>
                      </div>
                    )}
                  </div>

                  {/* Location details */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between">
                      <h4 className="font-semibold text-gray-900 text-sm leading-tight">
                        {location.name}
                      </h4>
                      {location.rating && (
                        <div className="flex items-center gap-1 ml-2 flex-shrink-0">
                          <svg
                            className="w-4 h-4 text-yellow-400 fill-current"
                            viewBox="0 0 20 20"
                          >
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                          </svg>
                          <span className="text-sm font-medium text-gray-700">
                            {location.rating}
                          </span>
                        </div>
                      )}
                    </div>

                    {location.description && (
                      <p
                        className="text-sm text-gray-600 mt-1 overflow-hidden"
                        style={{
                          display: "-webkit-box",
                          WebkitLineClamp: 2,
                          WebkitBoxOrient: "vertical",
                        }}
                      >
                        {location.description}
                      </p>
                    )}

                    <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
                      {location.estimated_visit_duration && (
                        <span className="flex items-center gap-1">
                          <svg
                            className="w-3 h-3"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                            />
                          </svg>
                          {location.estimated_visit_duration}
                        </span>
                      )}
                      {/* Distance and duration - show "Starting Point" for first location */}
                      {location.distance_from_previous && location.distance_from_previous !== "0.0 km" ? (
                        <span className="flex items-center gap-1">
                          <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                          </svg>
                          {location.distance_from_previous}
                        </span>
                      ) : locIndex === 0 ? (
                        <span className="flex items-center gap-1 text-green-600">
                          <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                          </svg>
                          Starting Point
                        </span>
                      ) : null}
                      {location.travel_duration && location.travel_duration !== "0 min" ? (
                        <span className="flex items-center gap-1">
                          <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2 2v12a2 2 0 002 2z" />
                          </svg>
                          {location.travel_duration}
                        </span>
                      ) : locIndex === 0 ? (
                        <span className="flex items-center gap-1 text-green-600">
                          <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          Begin Journey
                        </span>
                      ) : null}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Hotels section */}
      {hotels && hotels.length > 0 && (
        <div className="bg-white border border-gray-200 rounded-2xl shadow-sm overflow-hidden">
          <div className="bg-gradient-to-r from-green-50 to-emerald-50 px-6 py-4 border-b border-gray-100">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center">
                <svg
                  className="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
                  />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900">
                Recommended Stays
              </h3>
            </div>
          </div>

          <div className="p-6">
            <div className="grid gap-4">
              {hotelsToShow.map((hotel, index) => (
                <div 
                  key={index} 
                  className="flex gap-4 p-4 rounded-xl bg-gray-50 hover:bg-gray-100 transition-all duration-200 cursor-pointer hover:shadow-sm"
                  onClick={() => {
                    if (onLocationClick) {
                      // Handle different coordinate formats
                      const lat = hotel.coordinates?.lat || hotel.lat;
                      const lng = hotel.coordinates?.lng || hotel.lng || hotel.coordinates?.lon || hotel.lon;
                      
                      if (lat && lng) {
                        onLocationClick({
                          name: hotel.name,
                          lat: parseFloat(lat),
                          lng: parseFloat(lng)
                        });
                      }
                    }
                  }}
                >
                  {/* Hotel image */}
                  <div className="flex-shrink-0">
                    {hotel.photos && hotel.photos[0] ? (
                      <img
                        src={hotel.photos[0]}
                        alt={hotel.name}
                        className="w-24 h-20 rounded-lg object-cover"
                        onError={(e) => {
                          e.target.style.display = "none";
                        }}
                      />
                    ) : (
                      <div className="w-24 h-20 rounded-lg bg-gradient-to-br from-gray-200 to-gray-300 flex items-center justify-center">
                        <svg
                          className="w-6 h-6 text-gray-400"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
                          />
                        </svg>
                      </div>
                    )}
                  </div>

                  {/* Hotel details */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between">
                      <h4 className="font-semibold text-gray-900 text-sm leading-tight">
                        {hotel.name}
                      </h4>
                      {hotel.rating && (
                        <div className="flex items-center gap-1 ml-2 flex-shrink-0">
                          <svg
                            className="w-4 h-4 text-yellow-400 fill-current"
                            viewBox="0 0 20 20"
                          >
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                          </svg>
                          <span className="text-sm font-medium text-gray-700">
                            {hotel.rating}
                          </span>
                        </div>
                      )}
                    </div>

                    {hotel.description && (
                      <p
                        className="text-sm text-gray-600 mt-1 overflow-hidden"
                        style={{
                          display: "-webkit-box",
                          WebkitLineClamp: 2,
                          WebkitBoxOrient: "vertical",
                        }}
                      >
                        {hotel.description}
                      </p>
                    )}

                    <div className="flex items-center justify-between mt-2">
                      <div className="flex items-center gap-2">
                        {/* Hotel Category Tag */}
                        {hotel.category && (
                          <span className="text-xs bg-gray-200 px-2 py-1 rounded-full">{hotel.category}</span>
                        )}
                        {/* Pricing Tier Tag */}
                        {hotel.pricing?.tier && (
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                            hotel.pricing.tier === 'Budget' ? 'bg-green-100 text-green-700' :
                            hotel.pricing.tier === 'Mid-range' ? 'bg-blue-100 text-blue-700' :
                            hotel.pricing.tier === 'Premium' ? 'bg-purple-100 text-purple-700' :
                            hotel.pricing.tier === 'Luxury' ? 'bg-amber-100 text-amber-700' :
                            'bg-gray-100 text-gray-700'
                          }`}>
                            {hotel.pricing.tier}
                          </span>
                        )}
                      </div>
                      {hotel.pricing && (
                        <div className="text-right">
                          <div className="text-sm font-semibold text-gray-900">
                            {formatINR(hotel.pricing.range_min)} - {formatINR(hotel.pricing.range_max)}
                          </div>
                          <div className="text-xs text-gray-500">per night</div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
            
            {sortedHotels.length > 3 && (
              <div className="mt-4 text-center">
                <button 
                  onClick={() => setShowAllHotels(!showAllHotels)}
                  className="text-sm text-blue-600 hover:text-blue-700 font-medium transition-colors flex items-center justify-center gap-1 mx-auto"
                >
                  {showAllHotels ? (
                    <>
                      Show fewer hotels
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
                      </svg>
                    </>
                  ) : (
                    <>
                      View {sortedHotels.length - 3} more hotels
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                      </svg>
                    </>
                  )}
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default ItineraryCards;
