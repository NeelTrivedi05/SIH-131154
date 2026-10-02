/**
 * useSSE — Custom hook for Server-Sent Events with auto-reconnect
 * Subscribes to the PolarGrid backend stream and returns latest payload.
 */

import { useState, useEffect, useRef } from 'react';

// Use relative URL by default (works in dev with Vite proxy & in production when served by FastAPI)
// Or override with VITE_API_URL if frontend and backend are hosted on separate domains
const API_BASE = import.meta.env.VITE_API_URL || '';
const RECONNECT_DELAY = 3000;

export function useSSE() {
  const [data, setData] = useState(null);
  const [status, setStatus] = useState('connecting'); // 'connecting' | 'live' | 'error'
  const esRef = useRef(null);

  useEffect(() => {
    let cancelled = false;
    let timeout = null;

    function connect() {
      if (cancelled) return;
      setStatus('connecting');

      const es = new EventSource(`${API_BASE}/api/stream`);
      esRef.current = es;

      es.onopen = () => {
        if (!cancelled) setStatus('live');
      };

      es.onmessage = (event) => {
        if (cancelled) return;
        try {
          const payload = JSON.parse(event.data);
          setData(payload);
          setStatus('live');
        } catch {
          /* ignore malformed frames */
        }
      };

      es.onerror = () => {
        es.close();
        if (!cancelled) {
          setStatus('error');
          timeout = setTimeout(connect, RECONNECT_DELAY);
        }
      };
    }

    connect();

    return () => {
      cancelled = true;
      clearTimeout(timeout);
      esRef.current?.close();
    };
  }, []);

  return { data, status };
}
