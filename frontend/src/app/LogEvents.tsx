'use client';

import { useStatsigClient } from './my-statsig';

export default function LogEvents() {
  const { client } = useStatsigClient();

  const handleClick = () => {
    if (client) {
      client.logEvent("button_click", { page: "dashboard", timestamp: Date.now().toString() });
    }
  };

  return (
    <button
      onClick={handleClick}
      className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
    >
      Log Event
    </button>
  );
}
