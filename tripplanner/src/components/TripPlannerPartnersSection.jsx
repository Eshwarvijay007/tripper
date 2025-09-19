import React from 'react';
import { motion } from 'framer-motion';

const partners = [
  { alt: 'Booking', src: 'https://tripplanner.ai/_next/image?url=%2Fshared%2Fplatforms%2Fbooking-logo.webp&w=640&q=75&dpl=dpl_BVqXPdBxWjNVA6pzJR2huFbe68ST' },
  { alt: 'Viator', src: 'https://tripplanner.ai/landing/images/affiliates/viator.svg' },
  { alt: 'Get Your Guide', src: 'https://tripplanner.ai/landing/images/affiliates/getyourguide.svg' },
  { alt: 'Skyscanner', src: 'https://tripplanner.ai/landing/images/affiliates/skyscanner.svg' },
];

const TripPlannerPartnersSection = () => {
  const duplicatedPartners = [...partners, ...partners];

  return (
    <div className="py-12 bg-white">
      <div className="container mx-auto">
        <h4 className="px-6 text-center lg:px-12 mb-8">
          8M+ trips planned <br /> 4.9{" "}
          <span className="text-yellow-800">★</span> average
        </h4>
        <div className="relative w-full overflow-hidden">
          <motion.div
            className="flex"
            animate={{
              x: ["0%", "-100%"],
              transition: {
                ease: "linear",
                duration: 20,
                repeat: Infinity,
              },
            }}
          >
            {duplicatedPartners.map((partner, index) => (
              <div
                key={index}
                className="flex-shrink-0"
                style={{ width: `${100 / partners.length}%` }}
              >
                <div className="relative grid h-[8rem] w-full place-items-center">
                  <img
                    alt={partner.alt}
                    src={partner.src}
                    className="h-[2rem] w-auto object-contain"
                  />
                </div>
              </div>
            ))}
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default TripPlannerPartnersSection;