import React from 'react';

const TripPageHeader = () => {
  return (
    <div className="w-full h-12 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <a href="/" className="flex items-center gap-2">
          <img alt="Layla avatar" width="32" height="32" className="rounded-full" src="https://layla.ai/theme/layla/new-character-small.webp" />
          <span className="font-medium hidden sm:inline">Layla</span>
        </a>
        <div className="text-sm text-gray-800 truncate max-w-[50vw]">---</div>
      </div>
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 border rounded-md bg-gray-50">
          <button className="px-2 py-1 text-xs">USD</button>
          <div className="w-px h-4 bg-gray-300" />
          <button className="px-2 py-1 text-xs">EN</button>
        </div>
        <button className="px-2 py-1 text-xs border rounded-md">Menu</button>
      </div>
    </div>
  );
};

export default TripPageHeader;
