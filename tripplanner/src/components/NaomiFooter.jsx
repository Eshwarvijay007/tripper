import React from 'react';
import elephant from '../assets/images/elephant.png';

const NaomiFooter = () => {
  return (
    <footer className="w-full mt-auto">
      <div className="w-full border-t border-black/10 bg-transparent">
        <div className="w-full px-6 md:px-10 pt-6 md:pt-8">
          <div className="flex flex-col gap-1 pb-4">
            <span className="text-base md:text-lg text-gray-900 font-semibold">
              Plan smarter, travel better.
            </span>
            <span className="text-xs md:text-sm text-gray-700">
              Powered by Naomi — your personal travel agent
            </span>
          </div>
          <img
            src={elephant}
            alt="Elephant"
            className="block w-full h-auto select-none rounded-none"
          />
        </div>
      </div>
    </footer>
  );
};

export default NaomiFooter;
