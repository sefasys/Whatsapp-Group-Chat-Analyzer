import React from 'react';
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, ResponsiveContainer } from 'recharts';
import { OceanScores } from '../../types';

interface Props { scores: OceanScores; }
export default function OceanRadar({ scores }: Props) {
  const data = [
    { label: 'Openness', value: scores.openness * 100 },
    { label: 'Conscientiousness', value: scores.conscientiousness * 100 },
    { label: 'Extraversion', value: scores.extraversion * 100 },
    { label: 'Agreeableness', value: scores.agreeableness * 100 },
    { label: 'Neuroticism', value: scores.neuroticism * 100 },
  ];

  return (
    <ResponsiveContainer width="100%" height={300}>
      <RadarChart data={data}>
        <PolarGrid />
        <PolarAngleAxis dataKey="label" />
        <Radar dataKey="value" fill="#8884d8" fillOpacity={0.5} />
      </RadarChart>
    </ResponsiveContainer>
  );
}
