
import React, { useState } from 'react';
import { motion } from 'framer-motion';

const whyLayla = [
  {
    image: 'https://firebasestorage.googleapis.com/v0/b/bd-app-dev-375714.appspot.com/o/homepage_configs%2FHome%20Page%2FJapan%20Couple%20Trip%20.jpg?alt=media&token=a5a44574-b1b3-444e-90b7-a815921035d6',
    text: 'We just got engaged and crave six days of pure zen - think autumn-coloured gardens, private hot-spring soaks and a hands-on sushi lesson this October',
  },
  {
    image: 'https://layla.ai/_next/static/media/progressive_image_placeholder.28d15427.webp',
    text: 'It’s my 30th with five besties, give us four sun-drenched days of turquoise swims, villa pool parties and sunset boat cruises in July',
  },
  {
    image: 'https://layla.ai/_next/static/media/progressive_image_placeholder.28d15427.webp',
    text: 'Dad and I have always dreamed of spotting the Big Five. Plan an eight-day road-trip next month with whale watching, self-drive safaris and cosy budget lodges.',
  },
];

const LaylaWhySection = () => {
  const [activeIndex, setActiveIndex] = useState(0);

  const handleNext = () => {
    setActiveIndex((prevIndex) => (prevIndex + 1) % whyLayla.length);
  };

  const handlePrev = () => {
    setActiveIndex((prevIndex) => (prevIndex - 1 + whyLayla.length) % whyLayla.length);
  };

  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 1.0 }}
      className="w-full py-16 md:!py-24 px-4 md:px-6 bg-layla-background overflow-hidden"
    >
      <div className="container mx-auto flex flex-col items-start justify-center gap-8">
        <div className="w-full flex flex-col items-center gap-12">
          <div className="w-full inline-flex items-center gap-2">
            <div className="flex-1 inline-flex flex-col items-center gap-5">
              <h2 className="text-layla-foreground text-3xl font-bold leading-9">Tell me the why - I’ll nail the when, where & what</h2>
              <p className="text-layla-muted-foreground text-base leading-normal">What makes me stand out</p>
            </div>
          </div>
        </div>
        <div className="relative w-full">
          <div className="overflow-hidden">
            <motion.div
              className="flex -ml-4"
              animate={{ x: `-${activeIndex * 100 / 3}%` }}
              transition={{ type: 'spring', stiffness: 300, damping: 30 }}
            >
              {whyLayla.map((item, index) => (
                <div
                  key={index}
                  className="min-w-0 shrink-0 grow-0 pl-4 basis-full sm:basis-1/2 lg:basis-1/3"
                >
                  <div className="flex flex-col gap-3">
                    <div className="overflow-hidden border rounded-2xl bg-layla-background">
                      <div style={{ position: "relative", width: "100%", paddingBottom: "125%" }}>
                        <div style={{ position: "absolute", top: 0, right: 0, bottom: 0, left: 0 }}>
                          <div className="relative h-full w-full">
                            <img
                              alt="Prompt Example"
                              loading="lazy"
                              decoding="async"
                              src={item.image}
                              className="h-full w-full object-cover"
                            />
                            <div className="absolute left-4 bottom-4">
                              <button className="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-all cursor-pointer bg-secondary text-secondary-foreground shadow-xs hover:bg-secondary/80 h-9 px-4 py-2">
                                Ask
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-send size-4"><path d="M14.536 21.686a.5.5 0 0 0 .937-.024l6.5-19a.496.496 0 0 0-.635-.635l-19 6.5a.5.5 0 0 0-.024.937l7.93 3.18a2 2 0 0 1 1.112 1.11z"></path><path d="m21.854 2.147-10.94 10.939"></path></svg>
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <p className="text-layla-foreground text-lg leading-7 font-normal">{item.text}</p>
                  </div>
                </div>
              ))}
            </motion.div>
          </div>
          <button onClick={handlePrev} className="inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-medium transition-all cursor-pointer border bg-layla-background shadow-xs hover:bg-accent hover:text-accent-foreground absolute size-8 rounded-full top-1/2 -translate-y-1/2 left-1">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-arrow-left"><path d="m12 19-7-7 7-7"></path><path d="M19 12H5"></path></svg>
            <span className="sr-only">Previous slide</span>
          </button>
          <button onClick={handleNext} className="inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-medium transition-all cursor-pointer border bg-layla-background shadow-xs hover:bg-accent hover:text-accent-foreground absolute size-8 rounded-full top-1/2 -translate-y-1/2 right-1">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-arrow-right"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>
            <span className="sr-only">Next slide</span>
          </button>
        </div>
      </div>
    </motion.section>
  );
};

export default LaylaWhySection;
