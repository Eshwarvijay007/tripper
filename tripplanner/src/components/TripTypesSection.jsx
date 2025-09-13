import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'

const TripTypesSection = () => {
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

  const tripTypes = [
    {
      title: 'Family Trip Planner: Create Balanced Itineraries for All Ages',
      description: 'Traveling with family means balancing sightseeing with downtime. A family trip planner needs to account for different energy levels, child-friendly activities, and convenient accommodations. Trip Planner AI ensures you don\'t overpack the schedule while still hitting the highlights.',
      example: 'A 5-day Barcelona itinerary may include mornings at Gaudí landmarks, afternoons at the beach, and evenings with flexible dining options that work for kids and adults alike, plus suggested day trips to nearby gems like Montserrat or Sitges.',
      link: '/layla?type=family'
    },
    {
      title: 'Couples Trip Planner: Romantic Getaways Without the Stress',
      description: 'Couples want moments, not stress. Trip Planner AI designs couples getaways with the right mix of iconic experiences and hidden gems. Think candlelit dinners, scenic walks, and flexible pacing so you can relax, not rush.',
      example: 'A weekend in Paris might feature an Eiffel Tower evening view, a private Seine cruise, and a curated list of boutique hotels with romantic charm.',
      link: '/layla?type=couples'
    },
    {
      title: 'Road Trip Planner: Scenic Routes Optimized with AI',
      description: 'Road trips are about the journey as much as the destination. With the support of an AI itinerary builder for road trips, travelers save time while enjoying curated routes and must-see stops. Trip Planner AI maps optimized stopovers, scenic viewpoints, and overnight stays so you\'re never driving too long in one stretch.',
      example: 'Driving the Pacific Coast Highway? Our AI suggests overnight stops in Santa Barbara, Big Sur, and Monterey, with side trips to national parks and coastal hikes.',
      link: '/layla?type=roadtrip'
    },
    {
      title: 'Multi-City Trip Planner: Europe, Asia & Beyond',
      description: 'Multi-city trips can be complex, multiple flights, trains, transfers, and hotels. Using an AI trip planner for multi-city travel, you\'ll see optimized connections, transfers, and overnight stays in seconds.',
      example: 'A 10-day Europe trip could start in Rome, connect to Florence by train, then fly to Paris, all optimized for cost and convenience. Our AI ensures you know when to fly, when to drive, and when to take the train.',
      link: '/layla?type=multicity'
    }
  ]

  return (
    <div 
      ref={sectionRef}
      className={`lazy-element ${isVisible ? 'visible' : ''}`}
      id="trip-types-section"
    >
      <div className="bg-background py-12" id="features">
        <div className="mx-auto mb-32 px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="px-6 text-center text-3xl font-bold md:text-4xl lg:px-12 xl:text-5xl">
              <span className="text-primary-purple">Trip Planner </span> Built for Every Trip Type
            </h2>
          </div>
          <div className="mx-auto mt-10 flex h-full max-w-6xl grid-cols-1 flex-col flex-wrap items-start gap-5 md:mt-20 md:grid-cols-2 md:gap-8 lg:grid-cols-3">
            {tripTypes.map((tripType, index) => (
              <div 
                key={index}
                className="w-full flex-1 rounded-xl border border-solid border-gray-200 p-6 trip-card last:md:col-span-2 last:lg:col-span-1"
              >
                <div className="flex items-center gap-3">
                  <h4 className="leading-2 text-lg text-gray-900 md:text-xl lg:text-2xl">
                    <strong>{tripType.title.split(':')[0]}: </strong>
                    {tripType.title.split(':')[1]}
                  </h4>
                </div>
                <p className="mt-2 text-base text-gray-500 md:text-lg">
                  {tripType.description}<br />
                  <span className="italic">Example: {tripType.example}</span> <br />
                  <Link className="text-blue-600 underline" to={tripType.link}>
                    Plan your {tripType.title.split(':')[0].toLowerCase()} →
                  </Link>
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default TripTypesSection