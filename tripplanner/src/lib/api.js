export const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

export async function postChatMessage({ content, conversationId }) {
  const res = await fetch(`${API_BASE}/api/chat/messages`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content, conversation_id: conversationId || null }),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Chat API error ${res.status}: ${text}`);
  }
  const data = await res.json();
  // stream_url is relative from backend; make absolute
  const streamUrl = data.stream_url.startsWith('http')
    ? data.stream_url
    : `${API_BASE}${data.stream_url}`;
  return { conversationId: data.conversation_id, messageId: data.message_id, streamUrl };
}

export async function streamChat({ streamUrl, onEvent }) {
  const res = await fetch(streamUrl);
  if (!res.ok || !res.body) {
    throw new Error(`Stream error ${res.status}`);
  }
  const reader = res.body.getReader();
  const decoder = new TextDecoder('utf-8');
  let buf = '';
  for (;;) {
    const { value, done } = await reader.read();
    if (done) break;
    buf += decoder.decode(value, { stream: true });
    let idx;
    while ((idx = buf.indexOf('\n')) >= 0) {
      const line = buf.slice(0, idx).trim();
      buf = buf.slice(idx + 1);
      if (!line) continue;
      // Line is a Python-like dict string in our stub; try to coerce to JSON
      let evt = null;
      try {
        // convert single quotes to double quotes for JSON parse in stub environment
        const jsonish = line.replace(/'/g, '"');
        evt = JSON.parse(jsonish);
      } catch {
        // fallback no-op
      }
      if (evt && onEvent) onEvent(evt);
    }
  }
}

export async function searchFlights(payload) {
  const res = await fetch(`${API_BASE}/api/search/flights`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`Flight search failed ${res.status}`);
  return res.json();
}

export async function searchHotels(payload) {
  const res = await fetch(`${API_BASE}/api/search/hotels`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`Hotel search failed ${res.status}`);
  return res.json();
}

export async function createItinerary(payload) {
  const res = await fetch(`${API_BASE}/api/itineraries`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`Create itinerary failed ${res.status}`);
  return res.json();
}

export async function getItinerary(itineraryId) {
  const res = await fetch(`${API_BASE}/api/itineraries/${itineraryId}`);
  if (!res.ok) throw new Error(`Get itinerary failed ${res.status}`);
  return res.json();
}

export async function getFlightDestinations(query) {
  const url = `${API_BASE}/api/booking/flight-destinations?query=${encodeURIComponent(query)}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Flight destinations failed ${res.status}`);
  return res.json();
}

export async function getBookingDestinations(query) {
  const url = `${API_BASE}/api/booking/destinations?query=${encodeURIComponent(query)}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Destinations failed ${res.status}`);
  return res.json();
}

export async function getPlacesSuggestions(query) {
  const url = `${API_BASE}/api/places/suggest?query=${encodeURIComponent(query)}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Places suggest failed ${res.status}`);
  return res.json();
}

export async function getNearbyAttractions({ lat, lon }) {
  const res = await fetch(`${API_BASE}/api/search/poi`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ location: { lat, lon }, paging: { page: 1, page_size: 20 } }),
  });
  if (!res.ok) throw new Error(`POI search failed ${res.status}`);
  return res.json();
}

export async function agentPlan(payload, { signal } = {}) {
  const res = await fetch(`${API_BASE}/api/agent/plan`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
    body: JSON.stringify(payload),
    signal,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Agent plan failed ${res.status}: ${text}`);
  }
  return res.json();
}
