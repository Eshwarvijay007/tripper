import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'

const AIItinerarySection = () => {
  const [isVisible, setIsVisible] = useState(false)
  const sectionRef = useRef(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true)
        }
      },
      { threshold: 0.1, rootMargin: '50px' }
    )

    if (sectionRef.current) {
      observer.observe(sectionRef.current)
    }

    return () => observer.disconnect()
  }, [])

  return (
    <div
      ref={sectionRef}
      className={`lazy-element ${isVisible ? "visible" : ""}`}
      id="ai-itinerary-section"
    >
      <section className="bg-white py-12">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="px-6 text-center text-3xl font-bold md:text-4xl lg:px-12 xl:text-5xl">
              Planning the Perfect Itinerary with{" "}
              <span className="text-primary-purple">AI</span>
            </h2>
            <p className="mt-6 text-lg text-gray-600 max-w-4xl mx-auto">
              The best trips aren't just checklists of landmarks, they're{" "}
              <strong>balanced itineraries</strong> that flow naturally, leave
              space for surprises, and reflect your personal travel style.
              That's where <strong>Tripplanner.ai</strong> steps in: helping you
              explore destinations, compare options, and visualize
              possibilities.
            </p>
            <p className="mt-4 text-lg text-gray-600 max-w-4xl mx-auto">
              When you're ready to make it real, you're connected directly to{" "}
              <Link to="/naomi" className="text-blue-600 underline">
                Naomi.ai, your personal AI travel agent.
              </Link>{" "}
              Unlike static booking sites, Naomi.ai works like a collaborative
              journey planner: you share your ideas, it suggests smarter
              options, and together you refine every detail until your itinerary
              feels effortless and truly yours.
            </p>
          </div>

          <div className="mt-16 grid gap-8 md:grid-cols-3">
            <div className="text-center feature-card">
              <h4 className="text-xl font-bold text-gray-900 mb-4">
                From Idea to Itinerary that saves your hours
              </h4>
              <p className="text-gray-600">
                Trip planning begins in seconds with Naomi.ai Travel Agent:
                input your dates, destinations, and what you love, and the AI
                designs a full itinerary from flights and hotels to transfers
                and experiences.
              </p>
            </div>
            <div className="text-center feature-card">
              <h4 className="text-xl font-bold text-gray-900 mb-4">
                Plan Together
              </h4>
              <p className="text-gray-600">
                Planning doesn't end with the first draft. Naomi.ai allows you
                to <strong>chat directly with the AI</strong>, asking for
                adjustments like swapping museums for food tours or upgrading
                hotels.
              </p>
            </div>
            <div className="text-center feature-card">
              <h4 className="text-xl font-bold text-gray-900 mb-4">
                Flexible Itineraries
              </h4>
              <p className="text-gray-600">
                Every itinerary combines structure with freedom: 1–2 must-see
                highlights per day, flexibility built in, smart routing, and
                real-time updates.
              </p>
            </div>
          </div>

          <div className="mt-12 text-center">
            <Link
              to="/naomi"
              className="inline-flex items-center gap-2 rounded-full bg-accent-green px-8 py-4 text-lg text-white ring-2 ring-accent-green ring-offset-2 transition-colors hover:bg-accent-green-2 btn-hover"
            >
              Start a chat with Naomi.ai Travel Agent
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}

export default AIItinerarySection