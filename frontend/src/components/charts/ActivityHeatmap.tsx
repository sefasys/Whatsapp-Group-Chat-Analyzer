export default function ActivityHeatmap({ heatmap }: { heatmap: number[][] }) {
  const days = ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'];
  const hours = Array.from({ length: 24 }, (_, i) => i);

  // Find max for color scaling
  let max = 1;
  if (heatmap && heatmap.length > 0) {
    for (const row of heatmap) {
      for (const v of row) {
        if (v > max) max = v;
      }
    }
  }

  const cellColor = (val: number) => {
    if (!val) return 'var(--content-bg)';
    const ratio = val / max;
    // Light blue to accent blue gradient via opacity
    const alpha = Math.max(0.12, ratio);
    return `rgba(59, 130, 246, ${alpha})`;
  };

  return (
    <div className="card">
      <div className="card-header">
        <h3>Aktivite Isı Haritası</h3>
        <span className="text-xs text-muted">Gün × Saat</span>
      </div>
      <div className="card-body">
        <div className="heatmap-grid">
          {days.map((day, di) => (
            <div className="heatmap-row" key={di}>
              <div className="heatmap-label">{day}</div>
              {hours.map(h => {
                const val = heatmap?.[di]?.[h] ?? 0;
                return (
                  <div
                    key={h}
                    className="heatmap-cell"
                    style={{ background: cellColor(val) }}
                  >
                    <div className="heatmap-tooltip">
                      {day} {String(h).padStart(2, '0')}:00 — {val} mesaj
                    </div>
                  </div>
                );
              })}
            </div>
          ))}
        </div>
        <div className="heatmap-hours">
          {hours.map(h => (
            <span key={h}>{h % 3 === 0 ? h : ''}</span>
          ))}
        </div>
      </div>
    </div>
  );
}
