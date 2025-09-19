
import React from 'react';

const TripPlannerFaqsSection = () => {
  return (
    <div className="border-t border-solid border-gray-300">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6">
        <div className="flex w-full flex-col justify-center gap-2">
          <h2 className="text-center text-3xl font-medium">
            Customized <span className="font-semibold">Itineraries</span> for
            Every Travel Dream
          </h2>
          <p className="mx-auto mt-6 max-w-2xl text-center">
            Trip Planner AI is your ultimate companion for any travel scenario.
            Whether it's a solo adventure, a family vacation, or a group
            expedition, our app tailors every aspect of your journey. Experience
            the convenience of:
          </p>
        </div>
        <div className="mt-20 grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          <div className="flex flex-col gap-5 text-center">
            <h2 className="text-center text-xl font-medium">
              <span className="font-semibold text-primary-purple-2">
                AI-Powered
              </span>{" "}
              Route Optimization
            </h2>
            <p className="text-gray-600">
              Utilize AI for{" "}
              <strong className="font-medium text-gray-900">
                optimal travel routes.
              </strong>{" "}
              Our app ensures a seamless journey, calculating the best paths,
              travel times, and distances for city tours or cross-country road
              trips.
            </p>
          </div>
          <div className="flex flex-col gap-5 text-center">
            <h3 className="text-center text-xl font-medium">
              All-in-One{" "}
              <span className="font-semibold text-primary-purple-2">
                Travel Organizer
              </span>
            </h3>
            <p className="text-gray-600">
              Simplify travel planning with our all-in-one platform. Trip
              Planner AI consolidates hotel and flight details, manages
              bookings, and imports tips and guides. Organize{" "}
              <strong className="font-medium text-gray-900">
                all trip details in one place.
              </strong>
            </p>
          </div>
          <div className="flex flex-col gap-5 text-center md:col-span-2 lg:col-span-1">
            <h3 className="text-center text-xl font-medium">
              Collaborative{" "}
              <span className="font-semibold text-primary-purple-2">
                Group Planning
              </span>{" "}
              Made Easy
            </h3>
            <p className="text-gray-600">
              Collaborate on itineraries with companions. Our real-time feature
              makes group travel planning effortless, ensuring everyone stays
              informed and involved in the process.
            </p>
          </div>
        </div>
      </div>
      <div className="mx-auto flex max-w-7xl flex-col gap-2 px-4 py-12 text-center sm:px-6">
        <div className="mb-8 flex w-full flex-col justify-center gap-2">
          <h2 className="text-center text-3xl font-medium">FAQs</h2>
          <p className="mx-auto mt-6 max-w-2xl text-center">
            Updated by Trip Planner AI &amp; Naomi.ai Research Team on September
            1, 2025
          </p>
        </div>
        <p className="mt-2 text-base text-gray-500 md:text-lg">
          <strong>
            {" "}
            Q1: What’s the best way to plan a vacation itinerary?
          </strong>
          <br />
          The best way is to use an AI trip planner that balances activities,
          rest, and meals for your style of travel. Start with 1–2 highlights
          per day, then build flexibility around them.
          <br />
          <span className="italic">
            Example: In Rome, you might visit the Colosseum in the morning, then
            enjoy a leisurely evening in Trastevere.
          </span>
        </p>
        <p className="mt-2 text-base text-gray-500 md:text-lg">
          <strong> Q2: How far in advance should you book a trip?</strong>
          <br />
          For the best flight and hotel prices, book 6–9 months in advance. For
          peak holiday seasons, aim for a year ahead. Last-minute deals exist
          but are less reliable for families or couples.
        </p>
        <p className="mt-2 text-base text-gray-500 md:text-lg">
          <strong> Q3: What are affordable vacation ideas? </strong>
          <br />
          Affordable trips include national parks, road trips, and secondary
          cities with free attractions. All-inclusive packages can also save on
          meals and activities.
          <br />
          <span className="italic">
            Example: Lisbon, Valencia, or Mexico City deliver rich culture at
            lower costs.
          </span>
          <br />
          Browse{" "}
          <a
            className=" text-blue-600 underline"
            href="https://tripplanner.ai/public-trips?utm_medium=tripplanner"
          >
            Ready Trips
          </a>
        </p>
        <p className="mt-2 text-base text-gray-500 md:text-lg">
          <strong>Q4: What should be included in a road trip planner?</strong>
          <br />A good road trip planner includes routes, rest stops, overnight
          stays, and flexible timing.
          <br />
          <span className="italic">
            Example: The Pacific Coast Highway can be optimized with stopovers
            in Santa Barbara, Big Sur, and Monterey.
          </span>
          <br />
          Build your route with the{" "}
          <a className=" text-blue-600 underline" href="/naomi">
            California Road Trip.
          </a>
        </p>
        <p className="mt-2 text-base text-gray-500 md:text-lg">
          <strong>Q5: What makes a couples trip planner different?</strong>
          <br />
          Couples planners focus on romantic experiences and flexible pacing.
          Expect scenic walks, boutique hotels, and curated dining.
          <br />
          <span className="italic">
            Example: A weekend in Paris might combine a Seine dinner cruise with
            time to explore hidden cafes.
          </span>
          <br />
        </p>
        <p className="mt-2 text-base text-gray-500 md:text-lg">
          <strong>Q6: Do travelers need visas for Europe in 2025? </strong>
          <br />
          Yes. From 2025, U.S. citizens need ETIAS authorization to visit most
          European countries. Some destinations also require six months’
          passport validity.
          <br />
          <span className="italic">
            Example: A weekend in Paris might combine a Seine dinner cruise with
            time to explore hidden cafes.
          </span>
          <br />
          Check requirements:{" "}
          <a
            className=" text-blue-600 underline"
            href="https://travel-europe.europa.eu/en/etias"
          >
            https://travel-europe.europa.eu/en/etias
          </a>
        </p>
        <p className="mt-2 text-base text-gray-500 md:text-lg">
          <strong>
            Q7: What are the best destinations for multigenerational trips?
          </strong>
          <br />
          Destinations with a mix of activities and accessibility work best:
          cruises, resorts, and cultural cities.
          <br />
          <span className="italic">
            Examples: Italy, Spain, Portugal, or Caribbean resorts with
            childcare and easy day tours.
          </span>
        </p>
        <p className="mt-2 text-base text-gray-500 md:text-lg">
          <strong>Q8: What’s the cheapest time to travel?</strong>
          <br />
          Shoulder months like September and October are often the most
          affordable, with lower flight prices, fewer crowds, and better
          availability.
          <br />
        </p>
        <p className="mt-2 text-base text-gray-500 md:text-lg">
          <strong>Q9: How do you keep kids entertained on a long trip?</strong>
          <br />
          Pack games, audiobooks, tablets, and plan regular stops. Classic games
          like I Spy or surprise snacks keep trips fun.
          <br />
        </p>
        <div>
          <p className="mt-2 text-base text-gray-500 md:text-lg">
            <strong>
              Q10: What are the best road trips in the U.S. and Europe?
            </strong>
          </p>
          <ul className="mt-2 text-base text-gray-500 md:text-lg">
            <li>
              <strong>US:</strong> Pacific Coast Highway, Blue Ridge Parkway,
              Yellowstone loop
            </li>
            <li>
              <strong>Europe:</strong> Germany’s Romantic Road, Ireland’s Ring
              of Kerry, Italy’s Amalfi Coast.
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default TripPlannerFaqsSection;
