
import React, { useState, useEffect, useRef } from 'react';
import goaImg from '../assets/images/Goa.jpeg';
import keralaImg from '../assets/images/kerala.jpeg';
import kedarnathImg from '../assets/images/kedarnath.jpeg';
import charminarImg from '../assets/images/charminar.jpeg';
import hawamahalImg from '../assets/images/hawamahal.jpeg';
import { motion } from 'framer-motion';

const whyNaomi = [
  {
    image: goaImg,
    text: "Celebrating the big 3-0 with my best friends! We're dreaming of a four-day Goa getaway—beach vibes, cozy homestays, and a magical sunset cruise.",
  },
  {
    image: keralaImg,
    text: "Just married! We’re looking for a romantic four-day Kerala backwater escape with a private houseboat, luxury stays, and unforgettable moments to start our journey together.",
  },
  {
    image: kedarnathImg,
    text: "Our family has always wished for a spiritual retreat. Plan an eight-day Kedarnath pilgrimage with temple visits, peaceful ashrams, and budget-friendly stays surrounded by serenity.",
  },
  {
    image: charminarImg,
    text: "Exploring the heart of Hyderabad! Give us a two-day cultural trip around Charminar with heritage walks, bustling bazaars, and mouthwatering street food.",
  },
  {
    image: hawamahalImg,
    text: "A royal escape to Jaipur! Plan a three-day trip with a visit to Hawa Mahal, colorful markets, Rajasthani cuisine, and majestic forts.",
  }
];

const NaomiWhySection = () => {
  const [activeIndex, setActiveIndex] = useState(0);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const carouselRef = useRef(null);
  const autoScrollRef = useRef(null);

  // Create infinite loop by duplicating items
  const infiniteItems = [...whyNaomi, ...whyNaomi, ...whyNaomi];
  const startIndex = whyNaomi.length; // Start from the middle set

  const handleNext = () => {
    if (isTransitioning) return;
    setIsTransitioning(true);
    setActiveIndex((prevIndex) => prevIndex + 1);
  };

  const handlePrev = () => {
    if (isTransitioning) return;
    setIsTransitioning(true);
    setActiveIndex((prevIndex) => prevIndex - 1);
  };

  // Handle infinite loop reset
  useEffect(() => {
    if (isTransitioning) {
      const timer = setTimeout(() => {
        setIsTransitioning(false);
        // Reset to middle set when reaching boundaries
        if (activeIndex >= whyNaomi.length * 2) {
          setActiveIndex(whyNaomi.length);
        } else if (activeIndex < 0) {
          setActiveIndex(whyNaomi.length - 1);
        }
      }, 300);
      return () => clearTimeout(timer);
    }
  }, [activeIndex, isTransitioning]);

  // Auto-scroll functionality
  useEffect(() => {
    const startAutoScroll = () => {
      autoScrollRef.current = setInterval(() => {
        handleNext();
      }, 6000);
    };

    startAutoScroll();
    return () => {
      if (autoScrollRef.current) {
        clearInterval(autoScrollRef.current);
      }
    };
  }, []);

  // Pause auto-scroll on hover
  const handleMouseEnter = () => {
    if (autoScrollRef.current) {
      clearInterval(autoScrollRef.current);
    }
  };

  const handleMouseLeave = () => {
    autoScrollRef.current = setInterval(() => {
      handleNext();
    }, 6000);
  };

  // Handle mouse wheel scrolling
  const handleWheel = (e) => {
    e.preventDefault();
    if (e.deltaY > 0) {
      handleNext();
    } else {
      handlePrev();
    }
  };

  // Initialize with middle set
  useEffect(() => {
    setActiveIndex(startIndex);
  }, []);

  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 1.0 }}
      className="w-full py-16 md:!py-24 px-4 md:px-6 bg-transparent overflow-hidden"
    >
      <div className="container mx-auto flex flex-col items-start justify-center gap-8">
        <div className="w-full flex flex-col items-center gap-12">
          <div className="w-full inline-flex items-center gap-2">
            <div className="flex-1 inline-flex flex-col items-center gap-5">
              <h2 className="text-naomi-foreground text-3xl font-bold leading-9">
                Tell me the why - I’ll nail the when, where & what
              </h2>
              <p className="text-naomi-muted-foreground text-base leading-normal">
                What makes me stand out
              </p>
            </div>
          </div>
        </div>
        <div 
          className="relative w-full" 
          onMouseEnter={handleMouseEnter}
          onMouseLeave={handleMouseLeave}
          onWheel={handleWheel}
        >
          <div className="overflow-hidden rounded-2xl">
            <motion.div
              ref={carouselRef}
              className="flex -ml-4"
              animate={{ x: `-${(activeIndex * 100) / 3}%` }}
              transition={isTransitioning ? { type: "spring", stiffness: 300, damping: 30 } : { duration: 0 }}
            >
              {infiniteItems.map((item, index) => (
                <div
                  key={`${index}-${Math.floor(index / whyNaomi.length)}`}
                  className="min-w-0 shrink-0 grow-0 pl-4 basis-full sm:basis-1/2 lg:basis-1/3"
                >
                  <div className="flex flex-col gap-3">
                    <div className="overflow-hidden border rounded-2xl bg-naomi-background">
                      <div
                        style={{
                          position: "relative",
                          width: "100%",
                          paddingBottom: "125%",
                        }}
                      >
                        <div
                          style={{
                            position: "absolute",
                            top: 0,
                            right: 0,
                            bottom: 0,
                            left: 0,
                          }}
                        >
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
                                <svg
                                  xmlns="http://www.w3.org/2000/svg"
                                  width="24"
                                  height="24"
                                  viewBox="0 0 24 24"
                                  fill="none"
                                  stroke="currentColor"
                                  strokeWidth="2"
                                  strokeLinecap="round"
                                  strokeLinejoin="round"
                                  className="lucide lucide-send size-4"
                                >
                                  <path d="M14.536 21.686a.5.5 0 0 0 .937-.024l6.5-19a.496.496 0 0 0-.635-.635l-19 6.5a.5.5 0 0 0-.024.937l7.93 3.18a2 2 0 0 1 1.112 1.11z"></path>
                                  <path d="m21.854 2.147-10.94 10.939"></path>
                                </svg>
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <p className="text-naomi-foreground text-lg leading-7 font-normal">
                      {item.text}
                    </p>
                  </div>
                </div>
              ))}
            </motion.div>
          </div>
          {/* Left Arrow - Improved styling */}
          <button
            onClick={handlePrev}
            className="absolute left-4 top-1/2 -translate-y-1/2 z-10 w-12 h-12 bg-white/90 backdrop-blur-sm border border-gray-200 rounded-full shadow-lg hover:shadow-xl hover:bg-white transition-all duration-200 flex items-center justify-center group"
          >
            <svg
              className="w-5 h-5 text-gray-700 group-hover:text-gray-900 transition-colors"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            <span className="sr-only">Previous slide</span>
          </button>
          
          {/* Right Arrow - Improved styling */}
          <button
            onClick={handleNext}
            className="absolute right-4 top-1/2 -translate-y-1/2 z-10 w-12 h-12 bg-white/90 backdrop-blur-sm border border-gray-200 rounded-full shadow-lg hover:shadow-xl hover:bg-white transition-all duration-200 flex items-center justify-center group"
          >
            <svg
              className="w-5 h-5 text-gray-700 group-hover:text-gray-900 transition-colors"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
            <span className="sr-only">Next slide</span>
          </button>
          
          {/* Dots indicator */}
          <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2">
            {whyNaomi.map((_, index) => {
              const currentIndex = ((activeIndex % whyNaomi.length) + whyNaomi.length) % whyNaomi.length;
              return (
                <button
                  key={index}
                  onClick={() => {
                    setIsTransitioning(true);
                    setActiveIndex(startIndex + index);
                  }}
                  className={`w-2 h-2 rounded-full transition-all duration-200 ${
                    currentIndex === index 
                      ? 'bg-white shadow-md scale-110' 
                      : 'bg-white/60 hover:bg-white/80'
                  }`}
                />
              );
            })}
          </div>
        </div>
      </div>
    </motion.section>
  );
};

export default NaomiWhySection;
