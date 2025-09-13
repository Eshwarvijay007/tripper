import React from 'react';
import { motion } from 'framer-motion';

const LaylaHeroSection = () => {
  return (
    <motion.section 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="bg-background pt-40 pb-6 md:pb-12 flex flex-col items-center gap-6"
    >
      <div className="container mx-auto max-w-2xl md:!max-w-4xl px-6 md:px-4 flex flex-col items-center gap-12 md:gap-16">
        <div className="flex flex-col items-center gap-6 md:max-w-xl w-full">
          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="text-layla-foreground text-3xl md:!text-4xl lg:!text-5xl font-bold text-center leading-9 md:!leading-tight"
          >
            Hey, I’m Layla, your personal travel agent
          </motion.h1>
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="text-muted-foreground text-lg text-center leading-7 md:!text-base"
          >
            Tell me what you want, and I’ll handle the rest: flights, hotels, itineraries, in seconds.
          </motion.p>
        </div>
      </div>
    </motion.section>
  );
};

export default LaylaHeroSection;