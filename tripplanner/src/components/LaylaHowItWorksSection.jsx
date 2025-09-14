
import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Luggage, Plane, Hotel, Globe } from 'lucide-react';

const steps = [
  {
    title: 'Inspiration',
    description: 'Show me cultural spots to explore in Italy',
    icon: <Luggage />,
    image: 'https://layla.ai/Homepage/images/how-it-works/en/inspire.png',
  },
  {
    title: 'Flights',
    description: 'Find me cheap flights under $300 to Rome',
    icon: <Plane />,
    image: 'https://layla.ai/_next/static/media/progressive_image_placeholder.28d15427.webp',
  },
  {
    title: 'Hotels',
    description: 'Show me family friendly hotels in Rome',
    icon: <Hotel />,
    image: 'https://layla.ai/_next/static/media/progressive_image_placeholder.28d15427.webp',
  },
  {
    title: 'Trips',
    description: 'Build me a 7-day family vacation to Rome, including a guided tour of the Colosseum',
    icon: <Globe />,
    image: 'https://layla.ai/_next/static/media/progressive_image_placeholder.28d15427.webp',
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
