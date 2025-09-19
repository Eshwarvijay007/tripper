# Naomi.ai

## 🚀 Features

### Complete React Implementation
- **Modern React 18**: Built with the latest React features including hooks and functional components
- **Vite Build Tool**: Lightning-fast development and optimized production builds
- **React Router**: Client-side routing for seamless navigation
- **Tailwind CSS**: Utility-first CSS framework for rapid styling
- **Framer Motion**: Smooth animations and transitions (ready to implement)

### Naomi.ai Features
- **Exact Visual Recreation**: Pixel-perfect clone of the original Naomi.ai website
- **Responsive Design**: Fully responsive layout that works on all devices
- **Modern Animations**: Smooth scroll animations, hover effects, and lazy loading
- **Performance Optimized**: Fast loading with React optimization techniques
- **Accessibility**: Built with accessibility best practices in mind
- **Interactive Elements**: Functional carousel, smooth scrolling, and hover effects

### Naomi.ai Chat Interface
- **Complete Chat Interface**: Full recreation of Naomi's conversational AI interface
- **Interactive Trip Planning**: Simulated AI responses and trip generation
- **Real-time Chat**: Dynamic message handling with typing indicators
- **Voice Input Support**: Ready for Web Speech API integration
- **Trip Planning Process**: Animated step-by-step trip creation workflow
- **Booking Simulation**: Mock booking interface with interactive buttons

## 🛠 Technologies Used

- **React 18**: Modern React with hooks and functional components
- **Vite**: Next-generation frontend tooling for fast development
- **React Router DOM**: Declarative routing for React applications
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Beautiful & consistent icon toolkit
- **Framer Motion**: Production-ready motion library for React
- **PostCSS & Autoprefixer**: CSS processing and vendor prefixing


## 🚀 Getting Started

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure backend API base (optional):**
   - Copy `.env.example` to `.env`
   - Set `VITE_API_BASE` to your FastAPI URL (default `http://localhost:8000`)

3. **Start development server:**
   ```bash
   npm run dev
   ```

3. **Open your browser:**
   Navigate to `http://localhost:3000`

### Build for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## 🎨 Key Components

### HomePage
- Complete landing page with all sections
- Lazy loading animations
- Responsive design
- Interactive elements

### NaomiPage
- Full AI chat interface
- Message handling
- Typing indicators
- Trip planning simulation
- Booking options

### Reusable Components
- **Header**: Fixed navigation with scroll effects
- **HeroSection**: Main call-to-action area
- **FeaturesSection**: Feature showcase with animations
- **PartnerCarousel**: Infinite scrolling partner logos
- **TripTypesSection**: Interactive trip type cards
- **AIItinerarySection**: AI planning explanation
- **MobileCreateButton**: Floating mobile CTA

## ✨ Animations & Effects

- **Intersection Observer**: Lazy loading animations as elements come into view
- **CSS Transitions**: Smooth hover effects and state changes
- **Tailwind Animations**: Built-in animation utilities
- **Custom Keyframes**: Partner carousel and loading animations
- **Responsive Interactions**: Touch-friendly mobile interactions

## 🎯 Performance Features

- **Vite Optimization**: Fast development and optimized builds
- **Code Splitting**: Automatic route-based code splitting with React Router
- **Lazy Loading**: Components and images load as needed
- **Efficient Re-renders**: Optimized React component structure
- **Modern JavaScript**: ES6+ features for better performance

## 🔧 Customization

### Tailwind Configuration
The project uses custom Tailwind configuration with brand colors:

```javascript
colors: {
  'primary': '#6366f1',
  'primary-purple': '#8b5cf6',
  'primary-green': '#10b981',
  'accent-green': '#059669',
  // ... more colors
}
```

### Adding New Components
1. Create component in `src/components/`
2. Import and use in pages
3. Add routing in `App.jsx` if needed

### Styling
- Use Tailwind utility classes
- Custom CSS in `src/index.css`
- Component-specific styles with CSS modules if needed

## 🌐 Deployment

This React app can be deployed to any static hosting service:

- **Vercel**: `npm run build` then deploy `dist/` folder
- **Netlify**: Connect GitHub repo for automatic deployments
- **GitHub Pages**: Use `gh-pages` package
- **AWS S3**: Upload `dist/` folder to S3 bucket
- **Any CDN**: Deploy the built `dist/` folder

## 📱 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🤝 Contributing

This project demonstrates modern React development practices including:

- Functional components with hooks
- Component composition patterns
- State management with useState
- Effect handling with useEffect
- Event handling and user interactions
- Responsive design principles
- Performance optimization techniques

## 📄 License

This project is for educational and demonstration purposes only. All design rights belong to the original Naomi.ai team.

## Backend Integration (FastAPI)

- From repo root, run the backend:
  ```bash
  pip install -r requirements.txt
  uvicorn app.main:app --reload
  ```
- Health: `GET http://localhost:8000/api/healthz`
- The Naomi prompt section calls:
  - `POST {VITE_API_BASE}/api/chat/messages`
  - Streams NDJSON from `GET {VITE_API_BASE}/api/chat/stream/{conversation_id}`
- With the current stub backend, you will see streaming placeholder tokens in the chat UI.

---

Built with ❤️ using React 18, Vite, and modern web technologies
