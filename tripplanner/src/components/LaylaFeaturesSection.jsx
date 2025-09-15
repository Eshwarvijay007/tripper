import React from 'react';
import dodo1 from '../assets/images/dodo1.jpeg';
import dodo2 from '../assets/images/dodo2.jpeg';
import dodo3 from '../assets/images/dodo3.jpeg';
import dodo4 from '../assets/images/dodo4.jpeg';
import { motion } from 'framer-motion';

const features = [
  {
    icon: 'rocket',
    title: 'Tailor-made',
    description: 'Ask Naomi to create a personalized itinerary tailored to your preferences and travel style. Discover the ultimate travel experience with customized plans that cater to your unique interests, ensuring every moment of your journey is memorable and perfectly aligned with your desires.',
  },
  {
    icon: 'rocket',
    title: 'Cheaper',
    description: "Naomi makes you find the best deals and offers, saving you money on your travel plans. With Layla's expert guidance, you can explore a wide range of budget-friendly options, from affordable flights to discounted accommodations, ensuring your travel experience is both enjoyable and economical.",
  },
  {
    icon: 'rocket',
    title: 'Hidden Gems',
    description: "Naomi uncovers hidden gems and off-the-beaten-path destinations, ensuring you experience the best of your destination. Discover unique attractions and local secrets that are often overlooked by mainstream tourists. With Layla's expert guidance, you'll explore charming villages and breathtaking landscapes.",
  },
  {
    icon: 'rocket',
    title: 'No Surprises',
    description: "Naomi ensures everything runs smoothly, from flights to accommodations, with no unpleasant surprises. Whether you're booking flights, securing accommodations, or arranging activities, Layla's expert planning guarantees a stress-free experience. Enjoy your trip without the worry of unexpected issues..",
  },
];

const LaylaFeaturesSection = () => {
  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 1.6 }}
      className="bg-transparent py-16 md:!py-24 px-4 md:px-6"
    >
      <div className="container mx-auto flex flex-col gap-10 md:gap-12">
        <div className="mx-auto flex max-w-3xl flex-col items-center text-center">
          <div className="text-[11px] md:text-xs uppercase tracking-[0.14em] text-gray-500">Always‑on support</div>
          <h2 className="mt-1 text-[22px] md:text-[26px] font-semibold leading-tight text-gray-900">I will be there for you in every step</h2>
          <div className="mt-2 h-px w-14 md:w-16 bg-black/10" />
          <p className="mt-2 text-sm md:text-[15px] text-gray-600">Curate, save and get notified about your trips on the go.</p>
        </div>
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
          {features.map((feature, index) => {
            const imgs = [dodo1, dodo2, dodo3, dodo4];
            const img = imgs[index % imgs.length];
            return (
              <div key={index} className="flex flex-col items-center gap-4 text-center px-2">
                <div className="flex h-32 w-30 md:h-30 md:w-44 items-center justify-center rounded-md border border-black/10 bg-white shadow-sm overflow-hidden">
                  <img src={img} alt="" className="h-full w-full object-cover" />
                </div>
                <div className="flex flex-col gap-1 items-center">
                  <h3 className="text-gray-900 text-sm md:text-base font-semibold">{feature.title}</h3>
                  <p className="text-gray-600 text-xs md:text-sm leading-relaxed max-w-xs md:max-w-sm">{feature.description}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </motion.section>
  );
};

export default LaylaFeaturesSection;
