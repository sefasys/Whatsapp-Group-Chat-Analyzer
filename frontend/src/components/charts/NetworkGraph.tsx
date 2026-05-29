import { useRef, useEffect, useState } from 'react';
import ForceGraph2D from 'react-force-graph-2d';

interface Props {
  graph: {
    nodes: { id: string; label: string; influenceScore?: number }[];
    edges: { source: string; target: string; weight: number }[];
  };
}

export default function NetworkGraph({ graph }: Props) {
  const ref = useRef<any>();
  const containerRef = useRef<HTMLDivElement>(null);
  const [dims, setDims] = useState({ w: 0, h: 0 });

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    const obs = new ResizeObserver(() => {
      setDims({ w: el.offsetWidth, h: el.offsetHeight });
    });
    obs.observe(el);
    setDims({ w: el.offsetWidth, h: el.offsetHeight });
    return () => obs.disconnect();
  }, []);

  useEffect(() => {
    if (ref.current && graph.nodes.length > 0) {
      setTimeout(() => ref.current?.zoomToFit(300, 40), 300);
    }
  }, [graph, dims]);

  const data = {
    nodes: graph.nodes.map(n => ({ ...n, val: (n.influenceScore ?? 0.5) * 10 + 2 })),
    links: graph.edges.map(e => ({
      source: e.source,
      target: e.target,
      width: Math.max(0.5, Math.min(e.weight * 0.4, 4)),
    })),
  };

  return (
    <div className="card">
      <div className="card-header">
        <h3>Etkileşim Ağı</h3>
      </div>
      <div className="card-body" ref={containerRef} style={{ height: 360, overflow: 'hidden' }}>
        {dims.w > 0 && (
          <ForceGraph2D
            ref={ref}
            width={dims.w}
            height={dims.h}
            graphData={data}
            nodeLabel="label"
            nodeColor={() => 'var(--accent)'}
            nodeRelSize={4}
            linkColor={() => '#CBD5E1'}
            linkWidth="width"
            backgroundColor="transparent"
          />
        )}
      </div>
    </div>
  );
}
