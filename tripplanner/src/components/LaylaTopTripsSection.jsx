import React from 'react';
import { motion } from 'framer-motion';
import mysoreImg from '../assets/images/MYSORE.jpeg';
import indiaImg from '../assets/images/india.jpeg';
import blrImg from '../assets/images/bengaluru.jpeg';
import mumbai from '../assets/images/mumbai.jpeg';
import chennai from '../assets/images/chennai.jpeg';
import up from '../assets/images/up.jpeg';
const SimpleCard = ({ image, title, text }) => (
  <div className="group w-full max-w-sm md:max-w-md mx-auto rounded-2xl border border-black/5 shadow-sm overflow-hidden bg-white">
    <div className="relative w-full h-[28rem] md:h-[32rem] p-2 flex items-center justify-center bg-white">
      <img src={image} alt={title} className="h-full w-auto max-w-full object-contain rounded-2xl" />
      <div className="absolute inset-0 rounded-xl bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-200" />
      <div className="pointer-events-none absolute inset-x-0 bottom-0 p-4 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
        <div className="text-white font-semibold drop-shadow-sm">{title}</div>
        {text && <p className="text-white/90 text-sm mt-1 leading-relaxed">{text}</p>}
      </div>
    </div>
  </div>
);

const LaylaTopTripsSection = () => {
  const cards = [
    { image: mysoreImg, title: 'Mysuru Majesty', text: 'Palaces, silk markets, and dusky lamps — soak in royal grandeur with a relaxed city rhythm.' },
    { image: indiaImg, title: 'Incredible India Mix', text: 'A sampler of heritage, cuisine, and culture — perfect for first-timers looking to feel the vibe.' },
    { image: blrImg, title: 'Bengaluru City Vibes', text: 'Cafés, gardens, and creative corners — an easy-going urban escape with local flavors.' },
    { image: mumbai, title: 'Mumbai City Vibes', text: 'Cafés, gardens, and creative corners — an easy-going urban escape with local flavors.' },
    { image: chennai, title: 'Chennai City Vibes', text: 'Cafés, gardens, and creative corners — an easy-going urban escape with local flavors.' },
    { image: up, title: 'Uttar Pradesh City Vibes', text: 'Cafés, gardens, and creative corners — an easy-going urban escape with local flavors.' },
  ];

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
          <div className="grid grid-cols-1 gap-12 sm:grid-cols-2 lg:grid-cols-3">
            {cards.map((c, i) => (
              <SimpleCard key={i} image={c.image} title={c.title} text={c.text} />
            ))}
          </div>
        </div>
      </div>
    </motion.section>
  );
};

export default LaylaTopTripsSection;
