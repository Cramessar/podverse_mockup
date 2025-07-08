import React from "react";
import { PieChart, Pie, Cell, Legend, ResponsiveContainer } from "recharts";

interface FeedStatsChartProps {
  healthy: number;
  flagged: number;
}

const COLORS = ["#22c55e", "#f87171"];

export default function FeedStatsChart({ healthy, flagged }: FeedStatsChartProps) {
  const data = [
    { name: "Healthy", value: healthy },
    { name: "Flagged", value: flagged },
  ];
  return (
    <div className="w-full h-64">
      <ResponsiveContainer>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={80}
            label
          >
            {data.map((entry, idx) => (
              <Cell key={`cell-${idx}`} fill={COLORS[idx % COLORS.length]} />
            ))}
          </Pie>
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
