import React from 'react';
import { motion } from 'framer-motion';

const LaylaCtaSection = () => {
  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 1.2 }}
      className="px-4 md:px-6 py-16 md:!py-24 bg-layla-background"
      aria-labelledby="cta-heading"
    >
      <div className="container-padding-x bg-primary-green container mx-auto py-16 md:!rounded-xl md:!p-16">
        <div className="mx-auto flex max-w-xl flex-col items-center gap-8 md:!max-w-full md:!flex-row md:!gap-16">
          <div className="w-full flex-1">
            <div style={{ position: "relative", width: "100%", paddingBottom: "100%" }}>
              <div style={{ position: "absolute", top: 0, right: 0, bottom: 0, left: 0 }}>
                <img
                  alt="CTA section image"
                  loading="lazy"
                  decoding="async"
                  src="https://layla.ai/Homepage/images/layla-banner-image-desktop.webp"
                  className="rounded-xl object-cover h-full w-full"
                />
              </div>
            </div>
          </div>
          <div className="flex flex-1 flex-col items-center gap-8 md:!gap-10 md:!items-start">
            <div className="section-title-gap-lg mx-auto flex flex-col items-center text-center md:!items-start md:!text-left">
              <h2 id="cta-heading" className="heading-lg text-white">Your ultimate travel sidekick</h2>
              <p className="text-white/80">
                Looking for the perfect travel agent for your next family vacation, romantic getaway, anniversary escape, or birthday trip? You're in the right place. Ask me anything about planning your vacation — from dreamy destinations and cozy stays to flights, road trips, and more. Whether you're traveling with kids, your partner, or solo, I’ll help you build the perfect itinerary. No more juggling tabs and apps — I’m the only AI travel agent you need. Get inspired with personalized destination ideas and stunning video content from creators you’ll love. Then, customize every detail to make the most of your precious vacation days.
              </p>
            </div>
            <button className="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-all cursor-pointer shadow-xs h-9 px-4 py-2 bg-white text-primary-green hover:bg-gray-200">
              Create a new trip
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-arrow-right"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>
            </button>
          </div>
        </div>
      </div>
    </motion.section>
  );
};

export default LaylaCtaSection;