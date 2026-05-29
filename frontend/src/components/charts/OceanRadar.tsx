import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from 'recharts';
import { OceanScores } from '../../types';

export default function OceanRadar({ scores }: { scores: OceanScores }) {
  const data = [
    { trait: 'Açıklık', value: scores.openness ?? 50 },
    { trait: 'Sorumluluk', value: scores.conscientiousness ?? 50 },
    { trait: 'Dışadönüklük', value: scores.extraversion ?? 50 },
    { trait: 'Uyumluluk', value: scores.agreeableness ?? 50 },
    { trait: 'Nevrotiklik', value: scores.neuroticism ?? 50 },
  ];

  return (
    <div className="card">
      <div className="card-header">
        <h3>OCEAN Kişilik Profili</h3>
      </div>
      <div className="card-body" style={{ height: 300 }}>
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart data={data} cx="50%" cy="50%" outerRadius="72%">
            <PolarGrid stroke="var(--border)" />
            <PolarAngleAxis dataKey="trait" tick={{ fontSize: 11, fill: 'var(--text-secondary)' }} />
            <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
            <Tooltip
              contentStyle={{
                background: '#fff',
                border: '1px solid var(--border)',
                borderRadius: 4,
                fontSize: 12,
              }}
            />
            <Radar
              name="Skor"
              dataKey="value"
              stroke="var(--accent)"
              fill="var(--accent)"
              fillOpacity={0.2}
              strokeWidth={2}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
