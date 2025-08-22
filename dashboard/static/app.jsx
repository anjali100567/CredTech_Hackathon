// file: frontend/src/App.jsx
import React, { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function App() {
  const [score, setScore] = useState(null);
  const [prices, setPrices] = useState([]);
  const [events, setEvents] = useState([]);

  const ticker = "AAPL"; // demo ticker

  useEffect(() => {
    fetch(`/score/${ticker}`).then(r => r.json()).then(setScore);
    fetch(`/prices/${ticker}`).then(r => r.json()).then(setPrices);
    fetch(`/events/${ticker}`).then(r => r.json()).then(setEvents);
  }, []);

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold mb-4">Explainable Credit Intelligence Dashboard</h1>

      {/* Score */}
      <div className="bg-white shadow rounded-xl p-4 mb-6">
        <h2 className="text-xl">Latest Credit Score ({ticker})</h2>
        <p className="text-4xl font-bold text-blue-600">{score ? score.score : "Loading..."}</p>
        {score && <p className="text-gray-500 text-sm">Method: {score.method}, Updated: {new Date(score.time).toLocaleString()}</p>}
      </div>

      {/* Charts + Events */}
      <div className="grid grid-cols-2 gap-6">
        {/* Price Trend */}
        <div className="bg-white shadow rounded-xl p-4">
          <h2 className="text-lg mb-2">📊 Price Trend</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={prices}>
              <XAxis dataKey="ts" hide />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="close" stroke="#2563eb" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Events */}
        <div className="bg-white shadow rounded-xl p-4">
          <h2 className="text-lg mb-2">📰 Recent Events</h2>
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left border-b">
                <th>Time</th><th>Headline</th><th>Event</th><th>Impact</th>
              </tr>
            </thead>
            <tbody>
              {events.map((e, i) => (
                <tr key={i} className="border-b">
                  <td>{new Date(e.ts).toLocaleDateString()}</td>
                  <td>{e.headline}</td>
                  <td>{e.event_type}</td>
                  <td className={e.impact >= 0 ? "text-green-600" : "text-red-600"}>{e.impact}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
