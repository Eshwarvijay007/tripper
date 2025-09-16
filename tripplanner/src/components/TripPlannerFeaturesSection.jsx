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
      <section className={`${transparent ? 'bg-transparent' : 'bg-background'} mb-12 mt-5 py-8 md:mt-10`} id="product">
        <div className="container m-8 mx-auto max-w-5xl rounded-3xl bg-white/70 backdrop-blur-sm border border-black/5 shadow-sm px-6 md:px-10 py-8 md:py-12">
          <h2 className="px-0 text-center text-3xl md:text-4xl xl:text-5xl font-semibold leading-tight tracking-tight">
            <span className="text-gray-900">every journey has a storyteller.</span>
            <br className="hidden md:block" />
            <span className="script-accent">yours is Naomi</span>
          </h2>
          <p className="mt-6 md:mt-8 text-center text-gray-700">
            Planning a trip can feel overwhelming. <strong className="text-gray-900">Too many tabs, hours of research, no clear starting point.</strong> Our AI understands your travel needs, using live data and smart itineraries to match your style, budget, and timing. From flights to hotels to activities, we handle the whole process so you can focus on the journey.
          </p>

          <div className="mb-6 md:mb-8 w-full">
            <div className="mx-auto h-0.5 bg-black/10 w-40 md:w-56 rounded-full"></div>
          </div>

          {/* Feature 1 */}
          <div className="flex flex-wrap">
            <div className="w-full p-6 sm:w-1/2 md:mt-8">
              <h3 className="mb-3 text-2xl md:text-3xl font-semibold text-gray-900">Instant itineraries</h3>
              <p className="text-gray-700">
                Just enter your travel dates and destination—our planner instantly creates a detailed itinerary tailored to your needs. From iconic landmarks to hidden gems, your schedule includes timing, routes, and estimated costs so you always know what’s next. It's like having a personal guide, without the guesswork.
              </p>
            </div>
            <div className="w-full p-6 sm:w-1/2 self-center">
              <img alt="Instant itineraries" loading="lazy" decoding="async" className="mx-auto rounded-2xl border border-black/5 shadow-sm w-48 h-48 md:w-64 md:h-64" src={surfImg} />
            </div>
          </div>

          {/* Feature 2 */}
          <div className="flex flex-col-reverse flex-wrap sm:flex-row">
            <div className="w-full p-6 sm:w-1/2 self-center">
              <img alt="Trips for everyone" loading="lazy" decoding="async" className="mx-auto rounded-2xl border border-black/5 shadow-sm w-48 h-48 md:w-64 md:h-64" src={yogaImg} />
            </div>
            <div className="mt-8 w-full p-6 sm:w-1/2">
              <h3 className="mb-3 text-2xl md:text-3xl font-semibold text-gray-900">Trips for everyone</h3>
              <p className="text-gray-700">
                Whether you're traveling solo, with a partner, or in a group, your experience is uniquely yours. Our planner adapts to different travel styles—relaxed or fast-paced, luxurious or budget-friendly—ensuring your itinerary reflects your vibe, your preferences, and your pace.
              </p>
            </div>
          </div>

          {/* Feature 3 */}
          <div className="flex flex-wrap">
            <div className="w-full p-6 sm:w-1/2 md:mt-8">
              <h3 className="mb-3 text-2xl md:text-3xl font-semibold text-gray-900">Live prices & easy booking</h3>
              <p className="text-gray-700">
                No more switching between tabs or apps. See real-time prices for flights, hotels, and activities—all in one place. You get transparent comparisons and smooth booking options, so you're never left wondering if you missed a better deal. Everything is updated as you plan.
              </p>
            </div>
            <div className="w-full p-6 sm:w-1/2 self-center">
              <img alt="Live Prices & Easy Booking" loading="lazy" decoding="async" className="mx-auto rounded-2xl border border-black/5 shadow-sm w-48 h-48 md:w-64 md:h-64" src={boatImg} />
            </div>
          </div>

          {/* Feature 4 */}
          <div className="flex flex-col-reverse flex-wrap sm:flex-row">
            <div className="w-full p-6 sm:w-1/2 self-center">
              <img alt="Flexible editing" loading="lazy" width="200" height="200" decoding="async" className="mx-auto rounded-2xl border border-black/5 shadow-sm" src={uncle} />
            </div>
            <div className="mt-8 w-full p-6 sm:w-1/2">
              <h3 className="mb-3 text-2xl md:text-3xl font-semibold text-gray-900">Flexible editing</h3>
              <p className="text-gray-700">
                Plans change—and that’s okay. Easily remove, swap, or add new activities to your schedule. The AI recalculates travel time, updates pricing, and reshuffles nearby options so your day flows naturally. Every tweak feels seamless.
              </p>
            </div>
          </div>

          {/* Feature 5 */}
          <div className="flex flex-wrap">
            <div className="w-full p-6 sm:w-1/2 md:mt-8">
              <h3 className="mb-3 text-2xl md:text-3xl font-semibold text-gray-900">Smart food & culture picks</h3>
              <p className="text-gray-700">
                Beyond tourist traps, discover authentic places to eat, drink, and unwind. Our AI learns what you love—be it rooftop cocktails, cozy cafes, or night markets—and finds cultural hotspots that match. Each suggestion adds flavor to your journey, both literally and figuratively.
              </p>
            </div>
            <div className="w-full p-6 sm:w-1/2 self-center">
              <img alt="Smart food & culture picks" loading="lazy" width="330" height="330" decoding="async" className="mx-auto rounded-2xl border border-black/5 shadow-sm" src={dinein} />
            </div>
          </div>

          {/* Feature 6 */}
          <div className="flex flex-col-reverse flex-wrap sm:flex-row">
            <div className="w-full p-6 sm:w-1/2 self-center">
              <img alt="On-the-go access" loading="lazy" width="230" height="200" decoding="async" className="mx-auto rounded-2xl border border-black/5 shadow-sm" src={drinks} />
            </div>
            <div className="mt-8 w-full p-6 sm:w-1/2">
              <h3 className="mb-3 text-2xl md:text-3xl font-semibold text-gray-900">On-the-go access</h3>
              <p className="text-gray-700">
                Your full itinerary stays synced across devices, even offline. Need to check your dinner reservation while hiking? Want to change your hotel while sitting in a café? Everything you need is in your pocket, ready when you are.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default TripPlannerFeaturesSection;
