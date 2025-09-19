
import React from 'react';

const TripPlannerHeroSection = () => {
  return (
    <div className="relative z-[30] mt-24 h-auto min-h-0 w-full">
      <main className="relative h-full w-full rounded-3xl bg-white pb-72 pt-10  md:mx-auto md:pt-28">
        <div className="flex flex-col gap-5">
          <div className="px-4 md:px-6 flex flex-col gap-2 md:gap-4">
            <div className="sr-only text-4xl font-medium tracking-tight text-gray-900 xl:inline xl:text-4xl">
              Trip Planner AI
            </div>
            <h1 className="text-center text-4xl font-bold !leading-[1.2] tracking-tight text-gray-900 md:text-6xl xl:text-7xl">
              AI Trip Planner for <br /> Flights, Hotels &amp; Experience
            </h1>
            <p className="mx-auto my-3 max-w-2xl text-center text-gray-700 sm:mx-auto sm:mt-5 sm:text-base md:mt-5 md:text-lg xl:text-xl">
              Smarter than endless tabs, a personalized trip builder and
              itinerary generator that saves you hours planning flights, hotels,
              and activities.
            </p>
            <a
              className="mx-auto flex items-center gap-2 rounded-full bg-accent-green px-8 py-4 text-lg text-white ring-2 ring-accent-green ring-offset-2 transition-colors hover:bg-accent-green-2"
              href="/naomi"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                xmlnsXlink="http://www.w3.org/1999/xlink"
                aria-hidden="true"
                role="img"
                className="mb-1 text-xl iconify iconify--bx"
                width="1em"
                height="1em"
                viewBox="0 0 24 24"
              >
                <path
                  fill="currentColor"
                  d="M14.844 20H6.5C5.121 20 4 18.879 4 17.5S5.121 15 6.5 15h7c1.93 0 3.5-1.57 3.5-3.5S15.43 8 13.5 8H8.639a9.8 9.8 0 0 1-1.354 2H13.5c.827 0 1.5.673 1.5 1.5s-.673 1.5-1.5 1.5h-7C4.019 13 2 15.019 2 17.5S4.019 22 6.5 22h9.593a10.4 10.4 0 0 1-1.249-2M5 2C3.346 2 2 3.346 2 5c0 3.188 3 5 3 5s3-1.813 3-5c0-1.654-1.346-3-3-3m0 4.5a1.5 1.5 0 1 1 .001-3.001A1.5 1.5 0 0 1 5 6.5"
                ></path>
                <path
                  fill="currentColor"
                  d="M19 14c-1.654 0-3 1.346-3 3c0 3.188 3 5 3 5s3-1.813 3-5c0-1.654-1.346-3-3-3m0 4.5a1.5 1.5 0 1 1 .001-3.001A1.5 1.5 0 0 1 19 18.5"
                ></path>
              </svg>
              Create a New Trip
            </a>
          </div>
        </div>
      </main>
    </div>
  );
};

export default TripPlannerHeroSection;
