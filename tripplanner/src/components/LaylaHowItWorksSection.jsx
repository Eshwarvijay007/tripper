
import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Luggage, Plane, Hotel, Globe } from 'lucide-react';

const steps = [
  {
    title: 'Inspiration',
    description: 'Show me cultural spots to explore in Tamil Nadu',
    longDescription: "Explore the diverse cultural and historical landscapes of Tamil Nadu. Instead of a rigid itinerary, focus on a journey of discovery, highlighting the region's rich heritage. Describe the cultural significance of key locations, from the ancient Pallava monuments of Mahabalipuram and the living Chola temples of Thanjavur and Gangaikonda Cholapuram, to the vibrant spiritual center of Madurai.\n\nInclude lesser-known cultural gems like the Danish-era town of Tharangambadi or the unique Chettinad mansions. Mention specific cultural experiences beyond sightseeing, such as observing temple rituals, learning about traditional crafts like Kanchipuram silk weaving, or savoring the distinct local cuisine. The goal is to capture the essence of a cultural immersion rather than a simple tourist checklist.",
    icon: <Luggage />,
  },
  {
    title: 'Flights',
    description: 'Find me cheap flights under 5000 to Pune',
    longDescription: 'Search for the best flight deals to your desired destination. Filter by price, airline, and layovers to find the perfect option for your trip.',
    icon: <Plane />,
  },
  {
    title: 'Hotels',
    description: 'Show me family friendly hotels in Coorg',
    longDescription: 'Discover and book hotels that fit your needs. Explore options from luxury resorts to budget-friendly stays, with amenities and locations tailored to your preferences.',
    icon: <Hotel />,
  },
  {
    title: 'Trips',
    description: 'Build me a 7-day family vacation to Dubai, including a guided tour of the Burj Khalifa',
    longDescription: 'Plan your entire trip with a detailed itinerary. Get suggestions for activities, tours, and dining, all customized to your travel style and interests.In addition to tours and activities, the plan should offer a variety of dining options, from luxury fine dining to casual, family-friendly restaurants with designated kids play areas. Provide practical travel advice on local transportation (e.g., Metro vs. taxis), visa information, and tips for navigating the city with children. The goal is to create a full, customizable travel guide that balances adventure, relaxation, and cultural experiences, tailored to different family travel styles and budgets.',
    icon: <Globe />,
  },
];

const LaylaHowItWorksSection = () => {
  const [activeIndex, setActiveIndex] = useState(0);

  const handleStepClick = (index) => {
    setActiveIndex(index);
  };

  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.8 }}
      className="bg-transparent py-16 md:!py-24 px-4 md:px-6"
      id="how-it-works-section"
    >
      <div className="container mx-auto">
        <div className="mb-8 text-center md:mb-12">
          <h2 className="text-3xl font-bold leading-tight md:text-4xl lg:text-5xl text-layla-foreground">What you can ask me</h2>
          <p className="text-layla-muted-foreground mx-auto mt-3 max-w-2xl text-sm md:mt-4 md:text-base">Try one of these asks and let the vacation inspo roll in.</p>
        </div>
        <div>
          <div className="mx-auto flex max-w-6xl flex-col-reverse gap-6 md:flex-row md:gap-8 lg:gap-16">
            <div className="md:w-1/2 lg:w-2/5">
              <ul className="grid grid-cols-1 gap-3 md:flex md:flex-col md:gap-2">
                {steps.map((step, index) => (
                  <li
                    key={index}
                    className={`group relative flex cursor-pointer rounded-xl border px-4 py-3 transition-all duration-300 md:px-5 md:py-4 ${
                      activeIndex === index ? 'border-border bg-accent shadow-sm' : 'hover:border-border hover:bg-accent/30 border-transparent'
                    }`}
                    onClick={() => handleStepClick(index)}
                  >
                    <div className="flex w-full items-start gap-3 md:gap-4">
                      <div className={`flex aspect-square w-9 shrink-0 items-center justify-center rounded-lg transition-colors md:w-10 ${
                        activeIndex === index ? 'bg-primary-green text-white' : 'bg-muted text-layla-muted-foreground'
                      }`}>
                        {step.icon}
                      </div>
                      <div className="min-w-0 flex-1">
                        <h3 className={`mb-1 text-sm font-semibold transition-colors md:text-base lg:text-lg ${
                          activeIndex === index ? 'text-layla-foreground' : 'text-layla-muted-foreground'
                        }`}>{step.title}</h3>
                        <p className="text-layla-muted-foreground md:group-data-open:opacity-100 line-clamp-2 text-xs transition-all md:text-sm lg:text-sm">{step.description}</p>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
            <div className="relative md:w-1/2 lg:w-3/5">
              <div className="border border-black/10 rounded-xl shadow-sm bg-white p-5 md:p-6">
                <div className="flex items-start gap-4">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-primary-green text-white">
                    {steps[activeIndex].icon}
                  </div>
                  <div className="min-w-0 flex-1">
                    <h3 className="text-lg md:text-xl font-semibold text-gray-900 leading-tight">
                      {steps[activeIndex].title}
                    </h3>
                    <p className="mt-2 text-sm md:text-base text-gray-600 leading-relaxed">
                      {steps[activeIndex].description}
                    </p>
                    <p className="mt-2 text-sm md:text-base text-gray-600 leading-relaxed">
                      {steps[activeIndex].longDescription}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </motion.section>
  );
};

export default LaylaHowItWorksSection;
