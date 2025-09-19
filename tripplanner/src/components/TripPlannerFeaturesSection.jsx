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
    <div className="lazy-div" style={{ opacity: 1, transform: "none" }}>
      <section
        className={`${
          transparent ? "bg-transparent" : "bg-background"
        } mb-12 mt-5 py-8 md:mt-10`}
        id="product"
      >
        <div className="container m-8 mx-auto max-w-5xl rounded-3xl bg-white/70 backdrop-blur-sm border border-black/5 shadow-sm px-6 md:px-10 py-8 md:py-12">
          <h2 className="px-0 text-center text-3xl md:text-4xl xl:text-5xl font-semibold leading-tight tracking-tight">
            <span className="text-gray-900">
              every journey has a storyteller.
            </span>
            <br className="hidden md:block" />
            <span className="script-accent">yours is Naomi</span>
          </h2>
          <p className="mt-6 md:mt-8 text-center text-gray-700">
            Planning a trip can feel overwhelming.{" "}
            <strong className="text-gray-900">
              Too many tabs, hours of research, no clear starting point.
            </strong>{" "}
            Our AI understands your travel needs, using live data and smart
            itineraries to match your style, budget, and timing. From flights to
            hotels to activities, we handle the whole process so you can focus
            on the journey.
          </p>

          <div className="mb-6 md:mb-8 w-full">
            <div className="mx-auto h-0.5 bg-black/10 w-40 md:w-56 rounded-full"></div>
          </div>

          {/* Feature 1 */}
          <div className="flex flex-wrap">
            <div className="w-full p-6 sm:w-1/2 md:mt-8">
              <h3 className="mb-3 text-2xl md:text-3xl font-semibold text-gray-900">
                Instant itineraries
              </h3>
              <p className="text-gray-700">
                Enter your travel dates and destinations, and get a full plan
                while saving you hours, complete with trains, hotels, and
                activities.
                <br />
                <strong className="italic text-gray-900">Example: </strong>
                <span>
                  Planning a week in Jaipur? Naomi suggests a 7-day itinerary
                  that balances classics like Amer Fort and City Palace with
                  hidden gems like Chand Baori and local bazaars. You’ll see
                  timing, routes, and budget estimates all in one view.
                </span>
              </p>
            </div>
            <div className="w-full p-6 sm:w-1/2 self-center">
              <img
                alt="Instant itineraries"
                loading="lazy"
                decoding="async"
                className="mx-auto rounded-2xl border border-black/5 shadow-sm w-48 h-48 md:w-64 md:h-64"
                src={surfImg}
              />
            </div>
          </div>

          {/* Feature 2 */}
          <div className="flex flex-col-reverse flex-wrap sm:flex-row">
            <div className="w-full p-6 sm:w-1/2 self-center">
              <img
                alt="Trips for everyone"
                loading="lazy"
                decoding="async"
                className="mx-auto rounded-2xl border border-black/5 shadow-sm w-48 h-48 md:w-64 md:h-64"
                src={yogaImg}
              />
            </div>
            <div className="mt-8 w-full p-6 sm:w-1/2">
              <h3 className="mb-3 text-2xl md:text-3xl font-semibold text-gray-900">
                Trips for everyone
              </h3>
              <p className="text-gray-700">
                Every traveler is different, and your trip should reflect that.
                We adapt to your style, whether you’re planning a family
                vacation with downtime built in, a couples’ getaway filled with
                romantic moments or a Golden Triangle road trip our AI designs
                journeys that match your pace and preferences.
              </p>
            </div>
          </div>

          {/* Feature 3 */}
          <div className="flex flex-wrap">
            <div className="w-full p-6 sm:w-1/2 md:mt-8">
              <h3 className="mb-3 text-2xl md:text-3xl font-semibold text-gray-900">
                Live prices & easy booking
              </h3>
              <p className="text-gray-700">
                Compare real-time prices for trains and hotels, then book
                directly with trusted platforms like IRCTC,
                <a href="easemytrip.com" className="text-blue-600">
                  {" "}
                  EaseMyTrip.
                </a>{" "}
                Whether you’re searching for a boutique hotel in Jaipur or the
                cheapest flight to Goa, our AI finds the best options so you
                save money, time, and stress.
                <br />
                <strong className="italic text-gray-900">Example: </strong>
                <span>
                  {" "}
                  Help me find the best flights from Delhi to Goa on October 19,
                  2025, and a hotel near Baga Beach.” and watch the magic happen
                  on Naomi.ai
                </span>
              </p>
            </div>
            <div className="w-full p-6 sm:w-1/2 self-center">
              <img
                alt="Live Prices & Easy Booking"
                loading="lazy"
                decoding="async"
                className="mx-auto rounded-2xl border border-black/5 shadow-sm w-48 h-48 md:w-64 md:h-64"
                src={boatImg}
              />
            </div>
          </div>

          {/* Feature 4 */}
          <div className="flex flex-col-reverse flex-wrap sm:flex-row">
            <div className="w-full p-6 sm:w-1/2 self-center">
              <img
                alt="Flexible editing"
                loading="lazy"
                width="200"
                height="200"
                decoding="async"
                className="mx-auto rounded-2xl border border-black/5 shadow-sm"
                src={uncle}
              />
            </div>
            <div className="mt-8 w-full p-6 sm:w-1/2">
              <h3 className="mb-3 text-2xl md:text-3xl font-semibold text-gray-900">
                Flexible editing
              </h3>
              <p className="text-gray-700">
                Swap activities, adjust transport, or upgrade your hotel with
                one click, your itinerary updates instantly.
                <br />
                <strong className="italic text-gray-900">Example: </strong>
                <span>
                  {" "}
                  If you decide to skip a temple visit for a backwater cruise in
                  Kochi, your plan automatically recalculates travel times, new
                  costs, and nearby suggestions so nothing feels broken.
                </span>
              </p>
            </div>
          </div>

          {/* Feature 5 */}
          <div className="flex flex-wrap">
            <div className="w-full p-6 sm:w-1/2 md:mt-8">
              <h3 className="mb-3 text-2xl md:text-3xl font-semibold text-gray-900">
                Smart food & culture picks
              </h3>
              <p className="text-gray-700">
                Beyond tourist traps, discover authentic places to eat, drink,
                and unwind. Our AI learns what you love be it rooftop cocktails,
                cozy cafes, or night markets and finds cultural hotspots that
                match. Each suggestion adds flavor to your journey, both
                literally and figuratively.
              </p>
            </div>
            <div className="w-full p-6 sm:w-1/2 self-center">
              <img
                alt="Smart food & culture picks"
                loading="lazy"
                width="330"
                height="330"
                decoding="async"
                className="mx-auto rounded-2xl border border-black/5 shadow-sm"
                src={dinein}
              />
            </div>
          </div>

          {/* Feature 6 */}
          <div className="flex flex-col-reverse flex-wrap sm:flex-row">
            <div className="w-full p-6 sm:w-1/2 self-center">
              <img
                alt="On-the-go access"
                loading="lazy"
                width="230"
                height="200"
                decoding="async"
                className="mx-auto rounded-2xl border border-black/5 shadow-sm"
                src={drinks}
              />
            </div>
            <div className="mt-8 w-full p-6 sm:w-1/2">
              <h3 className="mb-3 text-2xl md:text-3xl font-semibold text-gray-900">
                On-the-go access
              </h3>
              <p className="text-gray-700">
                Your full itinerary stays synced across devices, even offline.
                Need to check your dinner reservation while hiking? Want to
                change your hotel while sitting in a café? Everything you need
                is in your pocket, ready when you are.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default TripPlannerFeaturesSection;
