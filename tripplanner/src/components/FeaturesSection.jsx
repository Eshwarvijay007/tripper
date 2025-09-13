import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'

const FeaturesSection = () => {
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
      className={`lazy-element ${isVisible ? 'visible' : ''}`}
    >
      <section className="bg-background mb-12 mt-5 py-8 md:mt-10" id="product">
        <div className="container m-8 mx-auto max-w-5xl">
          <h2 className="px-6 text-center text-3xl font-bold md:text-4xl lg:px-12 xl:text-5xl">
            What Makes Our <span className="text-primary-purple">AI Trip Planner</span> Different
          </h2>
          <p className="mt-10 px-3 text-center text-gray-600">
            Planning a trip can feel overwhelming. <strong className="text-black">Too many tabs, hours of research, no clear starting point.</strong> That's where Tripplanner.ai comes in, our AI understands your travel needs, using live data and smart itineraries to match your style, budget, and timing. From flights to hotels to activities, we handle the whole process so you can focus on the journey, not the research.
          </p>
          <div className="mb-4 w-full">
            <div className="mx-auto h-1 bg-primary w-64 my-0 mb-10 rounded-t py-0 opacity-25"></div>
          </div>

          {/* Feature Cards */}
          <div className="flex flex-wrap">
            <div className="w-full p-6 sm:w-1/2 md:mt-8">
              <h3 className="mb-3 w-fit bg-primary-green/70 text-2xl font-bold leading-none text-black md:text-3xl">
                Instant itineraries
              </h3>
              <p className="text-gray-600">
                Enter your travel dates and destinations, and get a full plan while saving you hours, complete with flights, hotels, and activities. <br />
                <strong className="italic text-black">Example:</strong>
                <span className="italic"> Planning a week in <Link to="/layla" className="text-blue-600 underline">Rome</Link>? Trip Planner AI suggests a 7-day itinerary that balances classics like the Colosseum and Vatican with hidden gems like Trastevere and local trattorias. You'll see timing, routes, and budget estimates all in one view.</span>
              </p>
            </div>
            <div className="w-full p-6 sm:w-1/2">
              <img 
                alt="Instant itineraries" 
                loading="lazy" 
                width="250" 
                height="250" 
                className="mx-auto" 
                src="https://tripplanner.ai/_next/image?url=%2Fillustrations%2Fdestinations2.webp&w=640&q=75&dpl=dpl_3qP7RFTTn9SpXVLfWPH7mXJQkG1s"
              />
            </div>
          </div>

          <div className="flex flex-col-reverse flex-wrap sm:flex-row">
            <div className="w-full p-6 sm:w-1/2">
              <img 
                alt="Trips for everyone" 
                loading="lazy" 
                width="200" 
                height="200" 
                className="mx-auto" 
                src="https://tripplanner.ai/_next/image?url=%2Fillustrations%2Fmap.webp&w=640&q=75&dpl=dpl_3qP7RFTTn9SpXVLfWPH7mXJQkG1s"
              />
            </div>
            <div className="mt-8 w-full p-6 sm:w-1/2">
              <div className="align-middle">
                <h3 className="mb-3 w-fit bg-primary-green/70 text-2xl font-bold leading-none text-black md:text-3xl">
                  Trips for everyone
                </h3>
                <p className="text-gray-600">
                  Every traveler is different, and your trip should reflect that. We adapts to your style, whether you're planning a <Link to="/layla" className="text-blue-600 underline">family vacation</Link> with downtime built in, a <Link to="/layla" className="text-blue-600 underline">couples getaway</Link> filled with romantic moments or a <Link to="/layla" className="text-blue-600 underline">Pacific Coast Highway road trip</Link> our AI designs journeys that match your pace and preferences.
                </p>
              </div>
            </div>
          </div>

          <div className="flex flex-wrap">
            <div className="w-full p-6 sm:w-1/2 md:mt-8">
              <h3 className="mb-3 w-fit bg-primary-green/70 text-2xl font-bold leading-none text-black md:text-3xl">
                Live Prices & Easy Booking
              </h3>
              <p className="text-gray-600">
                Compare real-time prices for flights and hotels, then book directly with trusted platforms like Skyscanner, Booking.com, and GetYourGuide. Whether you're searching for a boutique hotel in Rome or the cheapest flight to Paris, our AI finds the best options so you save money, time, and stress.<br />
                <strong className="italic text-black">Example:</strong> 
                <span className="italic">"Help me find the best flights from Paris to Rome on October 19, 2025, and a hotel with a view of the Colosseum." and watch the magic happen on Layla.ai</span>
              </p>
            </div>
            <div className="w-full p-6 sm:w-1/2">
              <img 
                alt="Live Prices & Easy Booking" 
                loading="lazy" 
                width="250" 
                height="250" 
                className="mx-auto" 
                src="https://tripplanner.ai/_next/image?url=%2Fillustrations%2Fdestinations2.webp&w=640&q=75&dpl=dpl_3qP7RFTTn9SpXVLfWPH7mXJQkG1s"
              />
            </div>
          </div>

          <div className="flex flex-col-reverse flex-wrap sm:flex-row">
            <div className="w-full p-6 sm:w-1/2">
              <img 
                alt="Flexible editing" 
                loading="lazy" 
                width="200" 
                height="200" 
                className="mx-auto" 
                src="https://tripplanner.ai/_next/image?url=%2Fillustrations%2Fmap.webp&w=640&q=75&dpl=dpl_3qP7RFTTn9SpXVLfWPH7mXJQkG1s"
              />
            </div>
            <div className="mt-8 w-full p-6 sm:w-1/2">
              <div className="align-middle">
                <h3 className="mb-3 w-fit bg-primary-green/70 text-2xl font-bold leading-none text-black md:text-3xl">
                  Flexible editing
                </h3>
                <p className="mb-8 text-gray-600">
                  Swap activities, adjust transport, or upgrade your hotel with one click, your itinerary updates instantly.<br />
                  <strong className="italic text-black">Example:</strong> 
                  <span className="italic">If you decide to skip a museum visit for a food tour in Tokyo, your plan automatically recalculates travel times, new costs, and nearby suggestions so nothing feels broken.</span>
                </p>
              </div>
            </div>
          </div>

          <article className="">
            <address className="author">Written by <a rel="author" className="pointer-events-none" href="/">Ana Rodriguez</a></address>
            Family & Group Travel Blogger
          </article>
        </div>
      </section>
    </div>
  )
}

export default FeaturesSection