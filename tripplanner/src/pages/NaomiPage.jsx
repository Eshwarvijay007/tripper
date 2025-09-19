import NaomiHeroSection from "../components/NaomiHeroSection";
import NaomiPromptSection from "../components/NaomiPromptSection";
import NaomiHowItWorksSection from "../components/NaomiHowItWorksSection";
import NaomiWhySection from "../components/NaomiWhySection";

import NaomiTopTripsSection from "../components/NaomiTopTripsSection";
import NaomiFeaturesSection from "../components/NaomiFeaturesSection";
import TripPlannerFeaturesSection from "../components/TripPlannerFeaturesSection";
import NaomiFooter from "../components/NaomiFooter";
import "./naomi.css";

const NaomiPage = () => {
  return (
    <div className="naomi-page min-h-screen flex flex-col">
      <NaomiHeroSection />
      <NaomiPromptSection />
      <NaomiHowItWorksSection />
      <NaomiWhySection />
      <TripPlannerFeaturesSection transparent />

      <NaomiTopTripsSection />
      <NaomiFeaturesSection />
      <NaomiFooter />
    </div>
  );
};

export default NaomiPage;
