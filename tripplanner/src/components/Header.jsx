import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

const Header = () => {
  const [isScrolled, setIsScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50)
    }

    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <div className={`fixed top-0 flex w-full items-center justify-center z-50 transition-all ${
      isScrolled ? 'header-blur' : ''
    }`}>
      <div className="mx-5 flex h-14 w-full max-w-screen-xl items-center justify-between md:h-16">
        <div className="flex gap-10">
          <Link className="font-display flex items-center text-2xl" to="/">
            <img 
              alt="Trip Planner AI Logo" 
              loading="lazy" 
              width="29" 
              height="29" 
              className="mr-2 rounded-sm" 
              src="https://tripplanner.ai/_next/image?url=%2Flogo%2Flogo.webp&w=64&q=75&dpl=dpl_3qP7RFTTn9SpXVLfWPH7mXJQkG1s"
            />
            <div className="text-base/7 font-medium md:text-xl/8">Trip Planner AI</div>
          </Link>
          <div className="flex">
            <Link 
              className="cursor-pointer rounded-lg px-3 py-1.5 text-gray-700 transition-colors hover:bg-gray-100 hidden" 
              to="/public-trips"
            >
              Community Trips
            </Link>
          </div>
        </div>
        <ul className="ml-5 flex gap-2">
          <li className="cursor-pointer rounded-full px-4 py-1.5 hover:bg-gray-100 hidden md:block">
            <Link to="/public-trips">Community Trips</Link>
          </li>
        </ul>
      </div>
    </div>
  )
}

export default Header