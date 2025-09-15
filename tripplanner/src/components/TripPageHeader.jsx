import React from 'react';

const TripPageHeader = () => {
  // Eager-import the first logo found in src/assets/logos for a clean minimalist header
  const logos = import.meta.glob('../assets/logos/*', { eager: true, as: 'url' });
  const logoUrl = Object.values(logos)[0];

  return (
    <div className="w-full h-14 flex items-center justify-between">
      <div className="flex items-center">
        <a href="/" className="inline-flex items-center" aria-label="Home">
          {logoUrl ? (
            <img src={logoUrl} alt="Logo" className="h-10 md:h-12 w-auto" />
          ) : (
            <span className="font-semibold">Trip</span>
          )}
        </a>
      </div>
      <div className="flex items-center gap-3 text-gray-900">
        <div className="flex items-center gap-2 border border-gray-300 rounded-md bg-white/60 backdrop-blur px-1 py-0.5">
          <button className="px-2 py-1 text-xs text-gray-900 hover:bg-black/5 rounded">INR</button>
          <div className="w-px h-4 bg-gray-300" />
          <button className="px-2 py-1 text-xs text-gray-900 hover:bg-black/5 rounded">EN</button>
        </div>
        <button className="px-2 py-1 text-xs border border-gray-300 rounded-md text-gray-900 bg-white/60 hover:bg-black/5">Menu</button>
      </div>
    </div>
  );
};

export default TripPageHeader;
