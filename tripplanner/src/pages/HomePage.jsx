import React from 'react';
import TripPlannerHeroSection from '../components/TripPlannerHeroSection';
import TripPlannerFeaturesSection from '../components/TripPlannerFeaturesSection';
import TripPlannerPartnersSection from '../components/TripPlannerPartnersSection';
import TripPlannerTripTypesSection from '../components/TripPlannerTripTypesSection';
import TripPlannerInspirationsSection from '../components/TripPlannerInspirationsSection';
import TripPlannerFaqsSection from '../components/TripPlannerFaqsSection';
import './tripplanner.css';

const HomePage = () => {
  return (
    <div>
      <TripPlannerHeroSection />
      <TripPlannerFeaturesSection />
      <TripPlannerPartnersSection />
      <TripPlannerTripTypesSection />
      <TripPlannerInspirationsSection />
      <TripPlannerFaqsSection />
    </div>
  );
};

export default HomePage;