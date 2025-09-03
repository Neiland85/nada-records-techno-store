'use client';

import { useStatsigClient } from "@statsig/react-bindings";

export default function LogEvents() {
  const { client } = useStatsigClient();

  return (
    <button
      onClick={() => client.logEvent("my_custom_event")}
      className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
    >
      Click Me
    </button>
  );
}
