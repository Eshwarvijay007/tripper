import { Link } from 'react-router-dom'
import { MapPin } from 'lucide-react'

const HeroSection = () => {
  return (
    <div className="relative z-[30] mt-24 h-auto min-h-0 w-full">
      <main className="relative h-full w-full rounded-3xl bg-white pb-72 pt-10 md:mx-auto md:pt-28">
        <div className="flex flex-col gap-5">
          <div className="px-4 md:px-6 flex flex-col gap-2 md:gap-4">
            <div className="sr-only text-4xl font-medium tracking-tight text-gray-900 xl:inline xl:text-4xl">
              Trip Planner AI
            </div>
            <div className="flex items-center justify-center gap-2 pb-4">
              <img
                alt="Trip Planner AI Character"
                loading="lazy"
                width="180"
                height="130"
                className="w-75 h-20 rounded-full"
                src="https://tripplanner.ai/logo/logo.svg"
              />
            </div>
            <h1 className="text-center text-4xl font-bold !leading-[1.2] tracking-tight text-gray-900 md:text-6xl xl:text-7xl animate-fade-in-up">
              AI Trip Planner for <br /> Flights, Hotels & Experience
            </h1>
            <p className="mx-auto my-3 max-w-2xl text-center text-gray-700 sm:mx-auto sm:mt-5 sm:text-base md:mt-5 md:text-lg xl:text-xl animate-fade-in-up">
              Smarter than endless tabs, a personalized trip builder and
              itinerary generator that saves you hours planning flights, hotels,
              and activities.
            </p>
            <Link
              className="mx-auto flex items-center gap-2 rounded-full bg-accent-green px-8 py-4 text-lg text-white ring-2 ring-accent-green ring-offset-2 transition-colors hover:bg-accent-green-2 btn-hover animate-fade-in-up"
              to="/naomi"
            >
              <MapPin className="mb-1 text-xl" size={20} />
              Create a New Trip
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
}

export default HeroSection