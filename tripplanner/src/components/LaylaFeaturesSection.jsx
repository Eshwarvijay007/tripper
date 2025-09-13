import React from 'react';
import { motion } from 'framer-motion';

const features = [
  {
    icon: 'rocket',
    title: 'Tailor-made',
    description: 'Ask Layla to create a personalized itinerary tailored to your preferences and travel style. Discover the ultimate travel experience with customized plans that cater to your unique interests, ensuring every moment of your journey is memorable and perfectly aligned with your desires.',
  },
  {
    icon: 'rocket',
    title: 'Cheaper',
    description: "Layla makes you find the best deals and offers, saving you money on your travel plans. With Layla's expert guidance, you can explore a wide range of budget-friendly options, from affordable flights to discounted accommodations, ensuring your travel experience is both enjoyable and economical.",
  },
  {
    icon: 'rocket',
    title: 'Hidden Gems',
    description: "Layla uncovers hidden gems and off-the-beaten-path destinations, ensuring you experience the best of your destination. Discover unique attractions and local secrets that are often overlooked by mainstream tourists. With Layla's expert guidance, you'll explore charming villages and breathtaking landscapes.",
  },
  {
    icon: 'rocket',
    title: 'No Surprises',
    description: "Layla ensures everything runs smoothly, from flights to accommodations, with no unpleasant surprises. Whether you're booking flights, securing accommodations, or arranging activities, Layla's expert planning guarantees a stress-free experience. Enjoy your trip without the worry of unexpected issues, knowing that Layla has everything under control, allowing you to focus on creating unforgettable memories.",
  },
];

const LaylaFeaturesSection = () => {
  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 1.6 }}
      className="bg-layla-background py-16 md:!py-24 px-4 md:px-6"
    >
      <div className="container mx-auto flex flex-col gap-10 md:gap-12">
        <div className="section-title-gap-lg mx-auto flex max-w-xl flex-col items-center text-center">
          <h2 className="heading-lg text-layla-foreground">I will be there for you in every step</h2>
          <p className="text-layla-muted-foreground text-base">Curate, save and get notified about your trips on the go.</p>
        </div>
        <div className="grid grid-cols-1 gap-8 md:grid-cols-2 md:gap-6 lg:grid-cols-4">
          {features.map((feature, index) => (
            <div key={index} className="flex flex-col items-center gap-5 text-center">
              <div className="bg-layla-background flex h-10 w-10 shrink-0 items-center justify-center rounded-md border shadow-xs">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={`lucide lucide-${feature.icon} text-primary-green h-5 w-5`} aria-hidden="true"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"></path><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"></path><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"></path><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"></path></svg>
              </div>
              <div className="flex flex-col gap-2">
                <h3 className="text-layla-foreground font-semibold">{feature.title}</h3>
                <p className="text-layla-muted-foreground">{feature.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </motion.section>
  );
};

export default LaylaFeaturesSection;