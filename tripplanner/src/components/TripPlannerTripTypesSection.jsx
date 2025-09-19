
import React from 'react';

const TripPlannerTripTypesSection = () => {
  return (
    <div className="lazy-div" style={{ opacity: 1, transform: "none" }}>
      <div className="bg-background py-12" id="features">
        <div className="mx-auto mb-32 px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="px-6 text-center text-3xl font-bold md:text-4xl lg:px-12 xl:text-5xl">
              <span className="text-primary-purple">Trip Planner </span> Built
              for Every Trip Type
            </h2>
          </div>
          <div className="mx-auto mt-10 flex h-full max-w-6xl grid-cols-1 flex-col flex-wrap items-start gap-5 md:mt-20 md:grid-cols-2 md:gap-8 lg:grid-cols-3">
            <div className="undefined w-full flex-1 rounded-xl border border-solid border-gray-200 p-6 last:md:col-span-2 last:lg:col-span-1">
              <div className="flex items-center gap-3">
                <h4 className="leading-2 text-lg text-gray-900 md:text-xl lg:text-2xl">
                  <strong>Family Trip Planner: </strong>Create Balanced
                  Itineraries for All Ages
                </h4>
              </div>
              <p className="mt-2 text-base text-gray-500 md:text-lg">
                Traveling with family means balancing sightseeing with downtime.
                A family trip planner needs to account for different energy
                levels, child-friendly activities, and convenient
                accommodations. Trip Planner AI ensures you don’t overpack the
                schedule while still hitting the highlights.
                <br />{" "}
                <span className="italic">
                  Example: A 5-day Barcelona itinerary may include mornings at
                  Gaudí landmarks, afternoons at the beach, and evenings with
                  flexible dining options that work for kids and adults alike,
                  plus suggested day trips to nearby gems like Montserrat or
                  Sitges.
                </span>{" "}
                <br /> Explore a full{" "}
                <a
                  className="text-blue-600 underline"
                  href="https://naomi.ai/plan/family-vacation-trip-planner?utm_medium=tripplanner"
                >
                  Family Vacation Trip Planner
                </a>
              </p>
            </div>
            <div className="undefined w-full flex-1 rounded-xl border border-solid border-gray-200 p-6 last:md:col-span-2 last:lg:col-span-1">
              <div className="flex items-center gap-3">
                <h4 className="leading-2 text-lg text-gray-900 md:text-xl lg:text-2xl">
                  <strong>Couples Trip Planner: </strong>Romantic Getaways
                  Without the Stress
                </h4>
              </div>
              <p className="mt-2 text-base text-gray-500 md:text-lg">
                Couples want moments, not stress. Trip Planner AI designs{" "}
                <strong>couples getaways</strong> with the right mix of iconic
                experiences and hidden gems. Think candlelit dinners, scenic
                walks, and flexible pacing so you can relax, not rush.
                <br />{" "}
                <span className="italic">
                  Example: A weekend in <strong>Paris</strong> might feature an
                  Eiffel Tower evening view, a private Seine cruise, and a
                  curated list of boutique hotels with romantic charm.
                </span>{" "}
                <br />
                Plan your escape with the{" "}
                <a
                  className="text-blue-600 underline"
                  href="https://naomi.ai/plan/couple-trip-planner?utm_medium=tripplanner"
                >
                  Couples Trip Planner
                </a>{" "}
                on Naomi.ai.
              </p>
            </div>
            <div className="undefined w-full flex-1 rounded-xl border border-solid border-gray-200 p-6 last:md:col-span-2 last:lg:col-span-1">
              <div className="flex items-center gap-3">
                <h4 className="leading-2 text-lg text-gray-900 md:text-xl lg:text-2xl">
                  <strong>Road Trip Planner: </strong>Scenic Routes Optimized
                  with AI
                </h4>
              </div>
              <p className="mt-2 text-base text-gray-500 md:text-lg">
                Road trips are about the journey as much as the destination.
                With the support of an{" "}
                <strong> AI itinerary builder for road trips,</strong> travelers
                save time while enjoying curated routes and must-see stops. Trip
                Planner AI maps optimized stopovers, scenic viewpoints, and
                overnight stays so you’re never driving too long in one stretch.
                <br />{" "}
                <span className="italic">
                  Example: Driving the <strong>Pacific Coast Highway</strong> ?
                  Our AI suggests overnight stops in Santa Barbara, Big Sur, and
                  Monterey, with side trips to national parks and coastal hikes.
                </span>{" "}
                <br />
                Customize your California route at{" "}
                <a className="text-blue-600 underline" href="/naomi">
                  California Road Trip
                </a>{" "}
                or just create your own!
              </p>
            </div>
            <div className="undefined w-full flex-1 rounded-xl border border-solid border-gray-200 p-6 last:md:col-span-2 last:lg:col-span-1">
              <div className="flex items-center gap-3">
                <h4 className="leading-2 text-lg text-gray-900 md:text-xl lg:text-2xl">
                  <strong>Multi-City Trip Planner: </strong>Europe, Asia &amp;
                  Beyond
                </h4>
              </div>
              <p className="mt-2 text-base text-gray-500 md:text-lg">
                Multi-city trips can be complex, multiple flights, trains,
                transfers, and hotels.{" "}
                <strong>Using an AI trip planner for multi-city travel,</strong>{" "}
                you’ll see optimized connections, transfers, and overnight stays
                in seconds.
                <br />{" "}
                <span className="italic">
                  Example: A 10-day <strong>Europe</strong> trip could start in
                  Rome, connect to Florence by train, then fly to Paris, all
                  optimized for cost and convenience. Our AI ensures you know
                  when to fly, when to drive, and when to take the train.
                </span>{" "}
                <br />
                Simply type and design your multi-city adventures with Naomi{" "}
                <a className="text-blue-600 underline" href="/naomi">
                  Multi-City Trip Planner.
                </a>{" "}
                on Naomi.ai.
              </p>
            </div>
          </div>
        </div>
        <div className="mx-auto flex flex-col px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="px-6 text-center text-3xl font-bold md:text-4xl lg:px-12 xl:text-5xl">
              Planning the Perfect Itinerary with AI
            </h2>
          </div>
          <div className="mx-auto mt-10 flex h-full max-w-6xl grid-cols-1 flex-col flex-wrap items-start gap-2 md:mt-20 md:grid-cols-2 md:gap-3 lg:grid-cols-3">
            <p className="mt-2 text-base text-gray-500 md:text-lg">
              The best trips aren’t just checklists of landmarks, they’re{" "}
              <strong> balanced itineraries</strong> that flow naturally, leave
              space for surprises, and reflect your personal travel style.
              That’s where <strong> Tripplanner.ai</strong> steps in: helping
              you explore destinations, compare options, and visualize
              possibilities.
            </p>
            <p className="mt-2 text-base text-gray-500 md:text-lg">
              When you’re ready to make it real, you’re connected directly to{" "}
              <a className="font-bold text-blue-600 underline" href="/naomi">
                Naomi.ai, your personal AI travel agent.
              </a>{" "}
              Unlike static booking sites, Naomi.ai works like a collaborative
              journey planner: you share your ideas, it suggests smarter
              options, and together you refine every detail until your itinerary
              feels effortless and truly yours
            </p>
            <h4 className="leading-2 text-lg font-bold text-gray-900 md:text-xl lg:text-2xl">
              From Idea to Itinerary that saves your hours
            </h4>
            <p className="mt-2 text-base text-gray-500 md:text-lg">
              Trip planning begins in seconds with Naomi.ai Travel Agent: input
              your dates, destinations, and what you love, and the AI designs a
              full itinerary from flights and hotels to transfers and
              experiences.
              <br />{" "}
              <span className="italic">
                Example: Ask for a “Plan me a 7-day cultural trip to Rome with
                my wife starting October 2nd” and Naomi.ai builds a plan that
                covers the Colosseum, Vatican Museums, and Piazza Navona, find
                hotels that match your taste and books flights that fit your
                timeline with time set aside for hidden trattorias and lazy
                piazza evenings.
              </span>{" "}
            </p>
            <h4 className="leading-2 text-lg font-bold text-gray-900 md:text-xl lg:text-2xl">
              Plan Together
            </h4>
            <p className="mt-2 text-base text-gray-500 md:text-lg">
              Planning doesn’t end with the first draft. Naomi.ai allows you to{" "}
              <strong>chat directly with the AI</strong> , asking for
              adjustments:
            </p>
            <ul className="mt-2 list-disc text-base text-gray-500 md:text-lg">
              <li>Swap museums for a guided food tours</li>
              <li>Shorten a train transfer</li>
              <li>Add a day trip to Florence or Capri</li>
              <li>Upgrade hotels to 5-star stays with sea views</li>
            </ul>
            <p className="mt-2 text-base text-gray-500 md:text-lg">
              The AI updates your itinerary instantly, recalculating costs,
              travel times, and alternatives, so you see how each change fits
              into the bigger picture.
            </p>
            <h4 className="leading-2 text-lg font-bold text-gray-900 md:text-xl lg:text-2xl">
              Flexible Itineraries
            </h4>
            <p className="mt-2 text-base text-gray-500 md:text-lg">
              The real power of an <strong>AI trip planner</strong> is combining
              structure with freedom. With <strong>Naomi.ai</strong>, every
              itinerary is designed to keep your trip organized while leaving
              room for spontaneity:
            </p>
            <ul className="mt-2 list-disc text-base text-gray-500 md:text-lg">
              <li>
                <strong>Daily plans:</strong> 1–2 must-see highlights to give
                each day purpose.
              </li>
              <li>
                <strong>Flexibility built in:</strong> optional activities and
                downtime when you need it.
              </li>
              <li>
                <strong>Smart routing:</strong> avoid backtracking and wasted
                travel time.
              </li>
              <li>
                <strong>Real-time updates:</strong> instant re-planning if
                weather shifts or your mood changes.
              </li>
            </ul>
            <p className="mt-2 text-base text-gray-500 md:text-lg">
              <span className="italic">
                Example: In <strong>Tokyo</strong>, if rain cancels an outdoor
                day trip , Naomi.ai instantly replaces it with an indoor food
                tour or museum visit , recalculating your schedule so nothing
                feels lost..
              </span>{" "}
            </p>
            <p className="mt-2 text-base text-gray-500">
              Start a chat with{" "}
              <a className="font-bold text-blue-600 underline" href="/naomi">
                Naomi.ai Travel Agent
              </a>{" "}
              and start your trip planning!
            </p>
            <article className="mt-4">
              <address className="author">
                Written by{" "}
                <a
                  rel="author"
                  className="pointer-events-none"
                  href="https://tripplanner.ai/"
                >
                  David Chen
                </a>
              </address>
              Data Scientist &amp; AI in Travel
            </article>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TripPlannerTripTypesSection;
