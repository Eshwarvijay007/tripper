import React, { useEffect, useMemo, useState, useContext } from 'react';
import { useLocation } from 'react-router-dom';
import TripPageHeader from '../components/TripPageHeader';
// Removed static title and itinerary in favor of dynamic cards
import ChatPanel from '../components/ChatPanel';
import Map from '../components/Map';
import HotelsList from '../components/HotelsList';
import AirportsList from '../components/AirportsList';
import DestinationsList from '../components/DestinationsList';
import AttractionsList from '../components/AttractionsList';
import HotelHeroCard from '../components/HotelHeroCard';
import ItineraryCards from '../components/ItineraryCards';
import { postChatMessage, streamChat, getConversationState } from '../lib/api';
import { ChatContext } from '../context/ChatContext';
import { ensureConversationId } from '../lib/conversation';

const FinalTripPlannerPage = () => {
  const tripData = {
    title: '---',
    legs: [
      { city: 'Seville', days: 'Day 1-3', itineraries: [] },
      { city: 'Granada', days: 'Day 3-5', itineraries: [] },
      { city: 'Malaga', days: 'Day 5-6', itineraries: [] },
    ],
    itinerary: [
      {
        day: 1,
        title: 'Historic Seville and Iconic Monuments',
        date: '22 May, 2025',
        description: `Start your Seville adventure with a guided tour of the city\'s most famous landmarks. Join the Seville: Cathedral, Giralda, and Royal Alcázar Guided Tour to explore the majestic Royal Alcázar of Seville, the stunning Seville Cathedral, and climb the iconic Giralda tower. This 3-hour tour offers skip-the-line access and rich historical insights. After the tour, take a leisurely stroll through the charming Barrio Santa Cruz, the old Jewish quarter with narrow streets and picturesque squares. For lunch, enjoy traditional Andalusian cuisine at El Rinconcillo, one of Seville\'s oldest tapas bars, known for its authentic atmosphere and delicious dishes. In the afternoon, visit the Plaza de España and relax in the adjacent Maria Luisa Park, perfect for a peaceful walk and photo opportunities. End your day with a refreshing drink at La Terraza de EME, a rooftop bar with views of the cathedral.`,
      },
      {
        day: 2,
        title: 'Cultural Gems and Flamenco Experience',
        date: '23 May, 2025',
        description: `Begin your day exploring the vibrant neighborhood of Triana, known for its ceramic workshops and lively atmosphere. Walk across the historic Triana Bridge (Puente de Isabel II) to reach the city center. Visit the Seville Bullring (Plaza de Toros de la Maestranza de Cabellería de Sevilla), one of Spain\'s most famous bullrings, and learn about its history. For lunch, savor modern Andalusian cuisine at Egaña-Oriza, a Michelin-starred restaurant offering exquisite dishes. In the afternoon, visit the Hospital de los Venerables, a beautiful baroque building with art exhibitions. In the evening, immerse yourself in authentic flamenco at Baraka Sala Flamenca, where passionate performances bring the spirit of Andalusia alive. Alternatively, you can join the Seville: Spanish Cooking Class with Dinner to learn how to prepare classic Spanish dishes and enjoy your own dinner.`,
      },
      {
        day: 3,
        title: 'Last Morning and Departure to Granada',
        date: '24 May, 2025',
        description: `On your final morning, take a relaxed walk through the Historic Center of Seville to soak in the city\'s atmosphere one last time. Visit the Torre del Oro, a historic watchtower by the Guadalquivir River, offering panoramic views. Enjoy a leisurely brunch at La Cacharrería, a cozy café known for its fresh juices and creative breakfast options. After brunch, check out from Eurostars Sevilla Boutique and prepare for your 2-hour drive to Granada.`,
      },
    ],
  };

  const [cards, setCards] = useState([]);
  const [mapMarkers, setMapMarkers] = useState([]);
  const location = useLocation();
  const {
    addMessage,
    conversationId,
    setConversationId,
    itineraryData,
    isItineraryDone,
    updateItineraryData,
    startAssistantTyping,
    stopAssistantTyping,
    setLastAssistantMessage,
  } = useContext(ChatContext);

  // Maintain agent state across turns for follow-up Q&A
  const [agentState, setAgentState] = useState({});
  const [pendingQuestions, setPendingQuestions] = useState([]);

  const defaultDates = useMemo(() => {
    const start = new Date();
    const end = new Date(start.getTime() + 24*3600*1000);
    const pad = (n) => String(n).padStart(2, '0');
    const toIsoDate = (d) => `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`;
    return { start: toIsoDate(start), end: toIsoDate(end) };
  }, []);

  const handleShowHotels = async () => {
    const city = tripData.legs?.[0]?.city || 'Seville';
    await processUserText(`Show me good hotel options in ${city} for my trip.`);
  };

  const handleShowAirports = async () => {
    const query = tripData.legs?.[0]?.city || 'Seville';
    await processUserText(`What are the best airports and flight options around ${query}?`);
  };

  const handleShowDestinations = async () => {
    const query = tripData.legs?.[0]?.city || 'Hubli';
    await processUserText(`Suggest great destinations and places to visit around ${query}.`);
  };

  // Function to check for itinerary data
  const checkForItineraryData = async (convId) => {
    try {
      const stateData = await getConversationState(convId);
      const state = stateData.state || {};
      
      if (state.itinerary_done && state.trip_plan) {
        updateItineraryData(state.trip_plan, true);
        
        // Update map markers with all locations from the trip plan
        const allLocations = [];
        if (state.trip_plan.trip_plan) {
          state.trip_plan.trip_plan.forEach(day => {
            if (day.locations) {
              day.locations.forEach(location => {
                if (location.lat && location.lng) {
                  allLocations.push({
                    lat: location.lat,
                    lon: location.lng,
                    title: location.name
                  });
                }
              });
            }
          });
        }
        setMapMarkers(allLocations);
      }
    } catch (error) {
      console.error('Error checking itinerary data:', error);
    }
  };

  // Shared function to process a free-form user text via chatbot
  const processUserText = async (text) => {
    const convId = conversationId || ensureConversationId();
    if (convId && convId !== conversationId) {
      setConversationId(convId);
    }
    startAssistantTyping();
    let firstAssistantChunk = true;
    try {
      const { streamUrl } = await postChatMessage({ content: text, conversationId: convId });
      await streamChat({
        streamUrl,
        onEvent: (evt) => {
          if (evt.event === 'message' && evt.role === 'assistant') {
            const content = evt.content || '';
            if (!content) return;
            if (firstAssistantChunk) {
              addMessage({ text: content, sender: 'assistant' });
              firstAssistantChunk = false;
            } else {
              setLastAssistantMessage(content);
            }
          }
          if (evt.event === 'done') {
            // Check for itinerary data after the stream is done
            checkForItineraryData(convId);
          }
        },
      });
    } catch (e) {
      const fallback = e.message || 'Sorry, something went wrong.';
      if (firstAssistantChunk) {
        addMessage({ text: fallback, sender: 'assistant' });
      } else {
        setLastAssistantMessage(fallback);
      }
    } finally {
      stopAssistantTyping();
    }
  };

  // Handler for location clicks
  const handleLocationClick = (location) => {
    if (location.lat && location.lng) {
      setMapMarkers([{
        lat: location.lat,
        lon: location.lng,
        title: location.name
      }]);
    }
  };

  // If navigated with initialQuery from Layla page, auto-process it once
  useEffect(() => {
    const navConversationId = location?.state?.conversationId;
    const resolvedConversationId = navConversationId || ensureConversationId();
    if (resolvedConversationId && resolvedConversationId !== conversationId) {
      setConversationId(resolvedConversationId);
    }
    const q = location?.state?.initialQuery;
    if (q && typeof q === 'string' && q.trim()) {
      processUserText(q);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Check for existing itinerary data on mount
  useEffect(() => {
    if (conversationId && !isItineraryDone) {
      checkForItineraryData(conversationId);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [conversationId]);

  return (
    <div className="min-h-screen flex flex-col bg-white">
      {/* Fixed top header, 48px height */}
      <header className="fixed top-0 left-0 right-0 h-14 flex items-center px-3 z-20 bg-[var(--brand-color)] text-gray-900">
        <TripPageHeader />
      </header>
      {/* Main content: left chat (fixed) + right trip panel (fixed) */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-[30%_70%] min-h-0 pt-12">
        {/* Center/Left: Chat panel */}
        <div className="min-h-0">
          <div className="sticky top-14 h-[calc(100vh-3.5rem)] border-r bg-[var(--brand-color)]">
            <ChatPanel onQuickAction={(label) => {
              const lower = label.toLowerCase();
              if (lower.includes('hotel')) {
                handleShowHotels();
              } else if (lower.includes('flight')) {
                processUserText('Suggest good flight options based on my trip.');
              } else if (lower.includes('destination') || lower.includes('place')) {
                handleShowDestinations();
              }
            }} onUserMessage={async (text) => { await processUserText(text); }} />
          </div>
        </div>
        {/* Right: Trip panel */}
        <aside className="min-h-0">
          <div className="sticky top-14 h-[calc(100vh-3.5rem)] border-l bg-gray-50 flex flex-col">
            {/* Split full height: itinerary scrollable (left), map full height (right) */}
            <div className="flex-1 grid grid-cols-1 lg:grid-cols-2 gap-4 p-4 min-h-0">
              <div className="min-h-0 overflow-y-auto space-y-4">
                {/* Permanent intro card */}
                <div className="bg-white/90 border rounded-3xl p-6 md:p-7 shadow-md backdrop-blur-sm overflow-hidden min-h-28 md:min-h-36">
                  <div className="flex items-start gap-4">
                    <div className="h-10 w-1.5 rounded-full bg-gradient-to-b from-emerald-500 to-lime-400" />
                    <div className="flex-1">
                      <h3 className="text-lg md:text-xl font-semibold tracking-tight text-gray-900">Your Itinerary Plan</h3>
                      <p className="mt-2 text-sm md:text-base text-gray-600 leading-relaxed">
                        Here i am just for you.
                      </p>
                      <p className="mt-1 text-sm text-gray-600 leading-relaxed">
                        A neat day-by-day schedule, hotels, and sights — all in one place.
                      </p>
                      <p className="mt-1 text-sm text-gray-600 leading-relaxed">
                        Want changes? Ask on the left and we’ll refine instantly.
                      </p>
                    </div>
                  </div>
                </div>
                {/* Itinerary Cards - Show when itinerary is done */}
                {isItineraryDone && itineraryData && (
                  <ItineraryCards 
                    tripPlan={itineraryData} 
                    onLocationClick={handleLocationClick}
                  />
                )}

                {/* Dynamic cards area */}
                {cards.map((card) => (
                  <div key={card.id} className="bg-white border rounded-md p-4">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="font-semibold text-sm">{card.title}</h3>
                      {card.type === 'hotels' && (
                        <button className="text-xs text-blue-600" onClick={handleShowHotels}>Refresh</button>
                      )}
                    </div>
                    {card.type === 'itinerary' && (
                      <div className="space-y-3">
                        {(card.itinerary?.days || []).map((d) => (
                          <div key={d.index} className="border rounded p-2">
                            <div className="font-medium text-sm">Day {d.index + 1}: {d.summary || 'Plan'}</div>
                            <ul className="mt-1 list-disc list-inside text-sm text-gray-700">
                              {(d.activities || []).map((a) => (
                                <li key={a.id}>{a.name}{a.category ? ` · ${a.category}` : ''}</li>
                              ))}
                            </ul>
                          </div>
                        ))}
                      </div>
                    )}
                    {card.type === 'hotels' && <HotelsList items={card.items} />}
                    {card.type === 'hotel_single' && <HotelHeroCard hotel={card.item} />}
                    {card.type === 'airports' && <AirportsList items={card.items} />}
                    {card.type === 'destinations' && (
                      <DestinationsList
                        items={card.items}
                        onShowOnMap={(ds) => {
                          const markers = (ds || []).filter(d => typeof d.lat === 'number' && typeof d.lon === 'number').map(d => ({
                            lat: d.lat,
                            lon: d.lon,
                            title: d.name,
                          }));
                          setMapMarkers(markers);
                        }}
                        onShowAttractions={async (d) => {
                          await processUserText(`Suggest popular attractions near ${d.name}.`);
                        }}
                      />
                    )}
                    {card.type === 'attractions' && (
                      <AttractionsList
                        items={card.items}
                        onShowOnMap={(items) => {
                          const markers = (items || []).filter(x => typeof x.lat === 'number' && typeof x.lon === 'number').map(x => ({ lat: x.lat, lon: x.lon, title: x.name }));
                          setMapMarkers(markers);
                        }}
                      />
                    )}
                    {card.type === 'error' && <div className="text-sm text-red-600">{card.error}</div>}
                  </div>
                ))}
              </div>
              <div className="min-h-0 h-full relative -mt-2 -mr-1 -mb-3 md:-mt-3 md:-mr-1 md:-mb-4">
                <Map fullHeight markers={mapMarkers} />
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
};

export default FinalTripPlannerPage;
