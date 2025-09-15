
import React from 'react';
import surfImg from '../assets/images/surf.png';
import yogaImg from '../assets/images/yoga1.png';
import boatImg from '../assets/images/boat.png';
import uncle from '../assets/images/Poster.jpeg';
import dinein from '../assets/images/dinein.jpeg';
import lady from '../assets/images/lady.jpeg';
import drinks from '../assets/images/drinks.jpeg';

const TripPlannerFeaturesSection = ({ transparent = false }) => {
  return (
    <div className="lazy-div" style={{opacity: 1, transform: "none"}}>
      <section className={`${transparent ? 'bg-transparent' : 'bg-background'} mb-12 mt-5 py-8 md:mt-10`} id="product">
        <div className="container m-8 mx-auto max-w-5xl rounded-3xl bg-white/70 backdrop-blur-sm border border-black/5 shadow-sm px-6 md:px-10 py-8 md:py-12">
          <h2 className="px-0 text-center text-3xl md:text-4xl xl:text-5xl font-semibold leading-tight tracking-tight">
            <span className="text-gray-900">every journey has a storyteller.</span>
            <br className="hidden md:block" />
            <span className="script-accent">yours is Naomi</span>
          </h2>
          <p className="mt-6 md:mt-8 text-center text-gray-700">Planning a trip can feel overwhelming. <strong className="text-gray-900">Too many tabs, hours of research, no clear starting point.</strong> Our AI understands your travel needs, using live data and smart itineraries to match your style, budget, and timing. From flights to hotels to activities, we handle the whole process so you can focus on the journey.</p>
          <div className="mb-6 md:mb-8 w-full">
            <div className="mx-auto h-0.5 bg-black/10 w-40 md:w-56 rounded-full"></div>
          </div>
          <div className="flex flex-wrap">
            <div className="w-full p-6 sm:w-1/2 md:mt-8">
              <h3 className="mb-3 text-2xl md:text-3xl font-semibold text-gray-900">Instant itineraries</h3>
              <p className="text-gray-700">Enter your travel dates and destinations, and get a full plan while saving you hours, complete with flights, hotels, and activities. <br /> <strong className="italic text-gray-900">Example:</strong><span className="italic"> Planning a week in <a href="http://layla.ai/chat/?ask=help-me-plan-a-7-day-trip-to-Rome?utm_medium=tripplanner" className="text-blue-600 underline">Rome</a>? Trip Planner AI suggests a 7-day itinerary that balances classics like the Colosseum and Vatican with hidden gems like Trastevere and local trattorias. You’ll see timing, routes, and budget estimates all in one view.</span></p>
            </div>
            <div className="w-full p-6 sm:w-1/2 self-center">
              <img alt="Instant itineraries" loading="lazy" decoding="async" className="mx-auto rounded-2xl border border-black/5 shadow-sm w-48 h-48 md:w-64 md:h-64" src={surfImg} />
            </div>
          </div>
          <div className="flex flex-col-reverse flex-wrap sm:flex-row">
            <div className="w-full p-6 sm:w-1/2 self-center">
              <img alt="Trips for everyone" loading="lazy"  decoding="async" className="mx-auto rounded-2xl border border-black/5 shadow-sm w-48 h-48 md:w-64 md:h-64" src={yogaImg} />
            </div>
            <div className="mt-8 w-full p-6 sm:w-1/2">
              <div className="align-middle">
                <h3 className="mb-3 text-2xl md:text-3xl font-semibold text-gray-900">Trips for everyone</h3>
                <p className="text-gray-700">Every traveler is different, and your trip should reflect that. We adapts to your style, whether you’re planning a <a href="https://layla.ai/plan/family-vacation-trip-planner?utm_medium=tripplanner" className="text-blue-600 underline">family vacation</a> with downtime built in, a <a href="https://layla.ai/plan/couple-trip-planner?utm_medium=tripplanner" className="text-blue-600 underline">couples getaway</a> filled with romantic moments or a <a href="/layla" className="text-blue-600 underline">Pacific Coast Highway road trip</a> our AI designs journeys that match your pace and preferences.</p>
              </div>
            </div>
          </div>
          <div className="flex flex-wrap">
            <div className="w-full p-6 sm:w-1/2 md:mt-8">
              <h3 className="mb-3 text-2xl md:text-3xl font-semibold text-gray-900">Live Prices &amp; Easy Booking</h3>
              <p className="text-gray-700">Compare real-time prices for flights and hotels, then book directly with trusted platforms like <a href="https://tripplanner.ai/www.skyscanner.com" className="text-blue-600 underline">Skyscanner</a>, <a href="https://www.booking.com/index.en-gb.html?label=CsscVZ7NSQPldPwV4ONiNutClDH2-ItineraryHotelSearch&amp;aid=2233658&amp;sid=667843cdc053d5906844fac0285f64ec?utm_medium=tripplanner" className="text-blue-600 underline">Booking.com</a>, and <a href="https://www.getyourguide.com/s/?q=tokyo+food+tours&amp;searchSource=3?utm_medium=tripplanner" className="text-blue-600 underline">GetYourGuide</a>. Whether you’re searching for a boutique hotel in Rome or the cheapest flight to Paris, our AI finds the best options so you save money, time, and stress.<br /> <strong className="italic text-gray-900">Example:</strong> <span className="italic"> “Help me find the best flights from Paris to Rome on October 19, 2025, and a hotel with a view of the Colosseum.” and watch the magic happen on Layla.ai</span></p>
            </div>
            <div className="w-full p-6 sm:w-1/2 self-center">
              <img alt="Live Prices & Easy Booking"  loading="lazy" decoding="async" className="mx-auto rounded-2xl border border-black/5 shadow-sm w-48 h-48 md:w-64 md:h-64" src={boatImg} />
            </div>
          </div>
          <div className="flex flex-col-reverse flex-wrap sm:flex-row">
            <div className="w-full p-6 sm:w-1/2 self-center">
              <img alt="Flexible editing" loading="lazy" width="200" height="200" decoding="async" className="mx-auto rounded-2xl border border-black/5 shadow-sm" src={uncle} />
            </div>
            <div className="mt-8 w-full p-6 sm:w-1/2">
              <div className="align-middle">
                <h3 className="mb-3 text-2xl md:text-3xl font-semibold text-gray-900">Flexible editing</h3>
                <p className="mb-8 text-gray-700">Swap activities, adjust transport, or upgrade your hotel with one click; your itinerary updates instantly.<br /><strong className="italic text-gray-900">Example:</strong> <span className="italic"> If you decide to skip a museum visit for a food tour in Tokyo, your plan automatically recalculates travel times, new costs, and nearby suggestions so nothing feels broken.</span></p>
              </div>
            </div>
          </div>
          <div className="flex flex-wrap">
            <div className="w-full p-6 sm:w-1/2 md:mt-8">
              <h3 className="mb-3 text-2xl md:text-3xl font-semibold text-gray-900">Live Prices &amp; Easy Booking</h3>
              <p className="text-gray-700">Compare real-time prices for flights and hotels, then book directly with trusted platforms like <a href="https://tripplanner.ai/www.skyscanner.com" className="text-blue-600 underline">Skyscanner</a>, <a href="https://www.booking.com/index.en-gb.html?label=CsscVZ7NSQPldPwV4ONiNutClDH2-ItineraryHotelSearch&amp;aid=2233658&amp;sid=667843cdc053d5906844fac0285f64ec?utm_medium=tripplanner" className="text-blue-600 underline">Booking.com</a>, and <a href="https://www.getyourguide.com/s/?q=tokyo+food+tours&amp;searchSource=3?utm_medium=tripplanner" className="text-blue-600 underline">GetYourGuide</a>. Whether you’re searching for a boutique hotel in Rome or the cheapest flight to Paris, our AI finds the best options so you save money, time, and stress.<br /> <strong className="italic text-gray-900">Example:</strong> <span className="italic"> “Help me find the best flights from Paris to Rome on October 19, 2025, and a hotel with a view of the Colosseum.” and watch the magic happen on Layla.ai</span></p>
            </div>
            <div className="w-full p-6 sm:w-1/2 self-center">
              <img alt="Live Prices & Easy Booking"  loading="lazy" width="330" height="330" decoding="async" className="mx-auto rounded-2xl border border-black/5 shadow-sm" src={dinein} />
            </div>
          </div>
          <div className="flex flex-col-reverse flex-wrap sm:flex-row">
            <div className="w-full p-6 sm:w-1/2 self-center">
              <img alt="Flexible editing" loading="lazy" width="230" height="200" decoding="async" className="mx-auto rounded-2xl border border-black/5 shadow-sm" src={drinks} />
            </div>
            <div className="mt-8 w-full p-6 sm:w-1/2">
              <div className="align-middle">
                <h3 className="mb-3 text-2xl md:text-3xl font-semibold text-gray-900">Flexible editing</h3>
                <p className="mb-8 text-gray-700">Swap activities, adjust transport, or upgrade your hotel with one click; your itinerary updates instantly.<br /><strong className="italic text-gray-900">Example:</strong> <span className="italic"> If you decide to skip a museum visit for a food tour in Tokyo, your plan automatically recalculates travel times, new costs, and nearby suggestions so nothing feels broken.</span></p>
              </div>
            </div>
          </div>
          <article className="">
            <address className="author">Written by <a rel="author" className="pointer-events-none" href="https://tripplanner.ai/">Ana Rodriguez</a></address>Family &amp; Group Travel Blogger
          </article>
        </div>
      </section>
    </div>
  );
};

export default TripPlannerFeaturesSection;
