import React from 'react';
import LaylaHeroSection from '../components/LaylaHeroSection';
import LaylaPromptSection from '../components/LaylaPromptSection';
import LaylaHowItWorksSection from '../components/LaylaHowItWorksSection';
import LaylaWhySection from '../components/LaylaWhySection';
import LaylaCtaSection from '../components/LaylaCtaSection';
import LaylaTopTripsSection from '../components/LaylaTopTripsSection';
import LaylaFeaturesSection from '../components/LaylaFeaturesSection';
import TripPlannerFeaturesSection from '../components/TripPlannerFeaturesSection';
import LaylaFooter from '../components/LaylaFooter';
import './layla.css';

const LaylaPage = () => {
  return (
    <div className="layla-page min-h-screen flex flex-col">
      <LaylaHeroSection />
      <LaylaPromptSection />
      <LaylaHowItWorksSection />
      <LaylaWhySection />
      <TripPlannerFeaturesSection transparent />
      <LaylaCtaSection />
      <LaylaTopTripsSection />
      <LaylaFeaturesSection />
      <LaylaFooter />
    </div>
  );
};

export default LaylaPage;
