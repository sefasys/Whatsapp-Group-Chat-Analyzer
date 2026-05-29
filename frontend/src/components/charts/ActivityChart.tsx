import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface Props {
  dailyActivity: { date: string; count: number }[];
}

export default function ActivityChart({ dailyActivity }: Props) {
  return (
    <div className="card">
      <div className="card-header">
        <h3>Günlük Mesaj Dağılımı</h3>
      </div>
      <div className="card-body" style={{ height: 240 }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={dailyActivity} margin={{ top: 4, right: 4, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
            <XAxis
              dataKey="date"
              tick={{ fontSize: 10, fill: 'var(--text-muted)' }}
              tickLine={false}
              axisLine={false}
              minTickGap={40}
            />
            <YAxis
              tick={{ fontSize: 10, fill: 'var(--text-muted)' }}
              tickLine={false}
              axisLine={false}
            />
            <Tooltip
              contentStyle={{
                background: '#fff',
                border: '1px solid var(--border)',
                borderRadius: 4,
                fontSize: 12,
              }}
            />
            <Bar dataKey="count" fill="var(--accent)" radius={[2, 2, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
