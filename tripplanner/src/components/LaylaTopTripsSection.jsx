import React from 'react';
import { motion } from 'framer-motion';

const trips = [
  {
    href: "https://layla.ai/trip/01JSF7A39YF67T1X0WA9P1MFAE",
    image: "https://firebasestorage.googleapis.com/v0/b/bd-app-dev-375714.appspot.com/o/homepage_configs%2FHome%20Page%2FRoad%20Trip%20Through%20the%20South%20of%20Spain.png?alt=media&token=3b358693-34b8-4348-b393-32a57d8c8468",
    title: "Road Trip Through the South of Spain",
  },
  {
    href: "https://layla.ai/trip/01K1G20TTDATS9SG8DHX7KS2HZ",
    image: "https://firebasestorage.googleapis.com/v0/b/bd-app-dev-375714.appspot.com/o/homepage_configs%2FHome%20Page%2F10%20Days%20in%20Vietnam_%20Culture%20&%20Adventure.png?alt=media&token=22359125-9331-433a-91a0-2459a2b853f5",
    title: "10 Days in Vietnam: Culture & Adventure",
  },
  {
    href: "https://layla.ai/trip/01JRTCP5YY15APNNVVG25PC04Z",
    image: "https://firebasestorage.googleapis.com/v0/b/bd-app-dev-375714.appspot.com/o/homepage_configs%2FHome%20Page%2FRomantic%20Getaway%20in%20the%20Amalfi%20Coast.png?alt=media&token=8286c683-1093-475e-9363-28bbc6259a99",
    title: "Romantic Getaway in the Amalfi Coast",
  },
  {
    href: "https://layla.ai/trip/01JRTCTG7Z947ZZZ0H6NARSM0R",
    image: "https://firebasestorage.googleapis.com/v0/b/bd-app-dev-375714.appspot.com/o/homepage_configs%2FHome%20Page%2FUltimate%20Summer%20Escape%20to%20Croatia.png?alt=media&token=a78a3970-9354-484c-a9fb-c17b6333c27c",
    title: "Ultimate Summer Escape to Croatia",
  },
];

const LaylaTopTripsSection = () => {
  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 1.4 }}
      className="bg-transparent py-16 md:!py-24 px-4 md:px-6"
      aria-labelledby="blog-section-heading"
    >
      <div className="container mx-auto gap-10 md:gap-12">
        <div className="flex flex-col items-center gap-10 md:gap-12">
          <div className="section-title-gap-lg mx-auto flex max-w-xl flex-col items-center text-center">
            <h2 id="blog-section-heading" className="heading-lg text-layla-foreground">Top Trips to Level Up Your Vacation Game</h2>
          </div>
          <div className="grid grid-cols-1 gap-8 md:grid-cols-2 md:gap-6 lg:grid-cols-4" role="list">
            {trips.map((trip, index) => (
              <a key={index} className="group block" target="_blank" href={trip.href}>
                <div className="flex flex-col gap-4 rounded-xl transition-all duration-200">
                  <div style={{ position: "relative", width: "100%", paddingBottom: "75%" }}>
                    <div className="overflow-hidden rounded-xl" style={{ position: "absolute", top: 0, right: 0, bottom: 0, left: 0 }}>
                      <img
                        alt={`${trip.title} thumbnail`}
                        loading="lazy"
                        decoding="async"
                        src={trip.image}
                        className="h-full w-full object-cover transition-transform duration-200 group-hover:scale-105"
                      />
                    </div>
                  </div>
                  <div className="flex flex-col gap-3">
                    <h3 className="text-base leading-normal font-semibold group-hover:underline text-layla-foreground">{trip.title}</h3>
                  </div>
                </div>
              </a>
            ))}
          </div>
        </div>
      </div>
    </motion.section>
  );
};

export default LaylaTopTripsSection;
