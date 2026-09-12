import React, { useMemo, useState } from 'react';
import ReactFlow, { 
  Background, 
  MiniMap, 
  Handle, 
  Position, 
  EdgeLabelRenderer, 
  getSmoothStepPath,
  Panel
} from 'reactflow';
import 'reactflow/dist/style.css';
import { AlertTriangle, Building } from 'lucide-react';

const handleStyle = {
  width: '6px',
  height: '6px',
  background: '#38bdf8',
  border: 'none',
  boxShadow: '0 0 8px rgba(56, 189, 248, 0.8)',
};

// Tooltip Component
const NodeTooltip = ({ role, statusColor, address, depth, volume }) => (
  <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-4 w-64 bg-slate-950/95 border border-slate-700 shadow-2xl p-2.5 rounded-lg text-xs z-50 pointer-events-none transition-opacity duration-200">
    <div className="flex items-center gap-2 mb-2 pb-2 border-b border-slate-800">
      <div className={`w-2 h-2 rounded-full ${statusColor}`} />
      <span className="font-semibold text-slate-200">{role}</span>
    </div>
    <div className="mb-2">
      <div className="text-[10px] text-slate-500 mb-0.5 uppercase tracking-wider">Complete Address</div>
      <div className="text-[11px] text-slate-300 font-mono break-all select-all leading-tight">
        {address}
      </div>
    </div>
    <div className="grid grid-cols-2 gap-2 mt-2 pt-2 border-t border-slate-800">
      <div>
        <div className="text-[9px] text-slate-500 uppercase tracking-wider">Depth</div>
        <div className="text-[11px] font-mono text-slate-300">{depth}</div>
      </div>
      <div>
        <div className="text-[9px] text-slate-500 uppercase tracking-wider">Volume</div>
        <div className="text-[11px] font-mono text-slate-300">{volume}</div>
      </div>
    </div>
  </div>
);

// 1. Suspect Node
const SuspectNode = ({ data }) => {
  const [hovered, setHovered] = useState(false);
  return (
    <div 
      className="relative rounded-xl bg-slate-950/90 border border-red-500/50 p-3.5 shadow-[0_0_20px_rgba(239,68,68,0.2)] backdrop-blur-md min-w-[200px]"
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      {hovered && (
        <NodeTooltip role="Origin Suspect" statusColor="bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.8)]" address={data.fullAddress} depth={data.depth} volume={data.volume} />
      )}
      <div className="bg-red-500/10 text-red-400 text-[10px] font-semibold px-2 py-0.5 rounded-full border border-red-500/30 inline-flex items-center gap-1.5 mb-2">
        <AlertTriangle size={12} />
        SUSPECT WALLET
      </div>
      <div className="text-xs font-mono text-slate-200 font-bold tracking-wider">{data.address}</div>
      <Handle type="source" position={Position.Right} style={handleStyle} />
    </div>
  );
};

// 2. Hop Node
const HopNode = ({ data }) => {
  const [hovered, setHovered] = useState(false);
  return (
    <div 
      className="relative rounded-xl bg-slate-900/90 border border-slate-700/60 p-3 shadow-lg backdrop-blur-md min-w-[180px]"
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      {hovered && (
        <NodeTooltip role="Intermediary Hop" statusColor="bg-slate-500 shadow-[0_0_8px_rgba(100,116,139,0.8)]" address={data.fullAddress} depth={data.depth} volume={data.volume} />
      )}
      <Handle type="target" position={Position.Left} style={handleStyle} />
      <div className="bg-slate-800 text-slate-400 text-[10px] px-2 py-0.5 rounded-full border border-slate-700 inline-flex items-center gap-1 mb-1.5">
        HOP #{data.hopIndex || 'X'} (INTERMEDIARY)
      </div>
      <div className="text-xs font-mono text-slate-300">{data.address}</div>
      <Handle type="source" position={Position.Right} style={handleStyle} />
    </div>
  );
};

// 3. VASP Node
const VaspNode = ({ data }) => {
  const [hovered, setHovered] = useState(false);
  return (
    <div 
      className="relative rounded-xl bg-slate-950/90 border border-emerald-500/50 p-3.5 shadow-[0_0_20px_rgba(16,185,129,0.2)] backdrop-blur-md min-w-[210px]"
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      {hovered && (
        <NodeTooltip role="Identified Exchange" statusColor="bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)]" address={data.fullAddress} depth={data.depth} volume={data.volume} />
      )}
      <Handle type="target" position={Position.Left} style={handleStyle} />
      <div className="bg-emerald-500/10 text-emerald-400 text-[10px] font-semibold px-2 py-0.5 rounded-full border border-emerald-500/30 inline-flex items-center gap-1.5 mb-2">
        <Building size={12} />
        IDENTIFIED VASP
      </div>
      <div className="text-sm font-bold text-white mb-1">{data.vaspName}</div>
      <div className="text-xs font-mono text-slate-300">{data.address}</div>
    </div>
  );
};

// Custom Edge with Label
const TransferEdge = ({ id, sourceX, sourceY, targetX, targetY, sourcePosition, targetPosition, data, animated, style, markerEnd }) => {
  const [edgePath, labelX, labelY] = getSmoothStepPath({ sourceX, sourceY, sourcePosition, targetX, targetY, targetPosition, borderRadius: 16 });
  return (
    <>
      <path id={id} className={`react-flow__edge-path ${animated ? 'animated' : ''}`} d={edgePath} style={{ ...style, stroke: '#60a5fa', strokeWidth: 2, strokeDasharray: '5,5' }} markerEnd={markerEnd} />
      {data?.amount && (
        <EdgeLabelRenderer>
          <div style={{ position: 'absolute', transform: `translate(-50%, -50%) translate(${labelX}px, ${labelY}px)`, pointerEvents: 'all' }} className="nodrag nopan">
            <div className="text-[10px] bg-slate-900/90 text-blue-400 border border-blue-500/30 px-2 py-0.5 rounded-full shadow-md font-mono">
              {data.amount}
            </div>
          </div>
        </EdgeLabelRenderer>
      )}
    </>
  );
};

const initialNodes = [
  { id: 'suspect', type: 'suspectNode', position: { x: 60, y: 200 }, data: { address: '0x742d...4f4e', fullAddress: '0x742d35Cc6634C0532925a3b844Bc454e4438f44e', depth: '0 Hops', volume: '62.5 ETH' } },
  { id: 'hop1', type: 'hopNode', position: { x: 440, y: 70 }, data: { address: '0x8f3c...1a2b', fullAddress: '0x8f3c9a6634C0532925a3b844Bc454e44381a2b', hopIndex: 1, depth: '1 Hop', volume: '50.5 ETH' } },
  { id: 'hop2', type: 'hopNode', position: { x: 440, y: 330 }, data: { address: '0x9a4d...2b3c', fullAddress: '0x9a4d2b6634C0532925a3b844Bc454e44382b3c', hopIndex: 2, depth: '1 Hop', volume: '12.0 ETH' } },
  { id: 'vasp', type: 'vaspNode', position: { x: 820, y: 200 }, data: { address: '0x10b2...9f31', fullAddress: '0x10b29f6634C0532925a3b844Bc454e44389f31', vaspName: 'Demo VASP / Binance', depth: '2 Hops', volume: '62.5 ETH' } }
];

const initialEdges = [
  { id: 'e1', source: 'suspect', target: 'hop1', type: 'transferEdge', animated: true, data: { amount: '50.5 ETH' } },
  { id: 'e2', source: 'suspect', target: 'hop2', type: 'transferEdge', animated: true, data: { amount: '12.0 ETH' } },
  { id: 'e3', source: 'hop1', target: 'vasp', type: 'transferEdge', animated: true, data: { amount: '50.5 ETH' } },
  { id: 'e4', source: 'hop2', target: 'vasp', type: 'transferEdge', animated: true, data: { amount: '12.0 ETH' } }
];

export default function TransactionGraph() {
  const nodeTypes = useMemo(() => ({ suspectNode: SuspectNode, hopNode: HopNode, vaspNode: VaspNode }), []);
  const edgeTypes = useMemo(() => ({ transferEdge: TransferEdge }), []);

  return (
    <div className="w-full h-full relative">
      <style>{`
        .react-flow__minimap { background-color: #020617 !important; border-radius: 0 0 0.5rem 0.5rem; }
        .react-flow__attribution { display: none !important; }
      `}</style>
      <ReactFlow
        nodes={initialNodes}
        edges={initialEdges}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        fitView
        className="bg-slate-900"
        proOptions={{ hideAttribution: true }}
      >
        <Background color="#334155" gap={20} size={1} variant="dots" />
        
        {/* Canvas Status Telemetry Bar */}
        <Panel position="top-left" className="m-4">
          <div className="bg-slate-950/90 border border-slate-800 backdrop-blur px-3 py-1.5 rounded-md flex items-center gap-2 shadow-lg">
            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse shadow-[0_0_8px_rgba(16,185,129,0.6)]" />
            <div className="text-[11px] font-mono text-slate-400">
              SYS // ACTIVE GRAPH: 4 NODES · 4 EDGES · MAX DEPTH: 3 HOPS · STATUS: RESOLVED
            </div>
          </div>
        </Panel>

        {/* Native MiniMap (NOT wrapped in a Panel) */}
        <MiniMap 
          position="bottom-right"
          className="!bg-slate-950 !border !border-slate-800 !rounded-lg !shadow-2xl overflow-hidden !m-6"
          style={{ width: 180, height: 120 }}
          pannable={true}
          zoomable={true}
          maskColor="rgba(15, 23, 42, 0.85)"
          maskStrokeColor="#3b82f6"
          maskStrokeWidth={2}
          nodeStrokeWidth={1}
          nodeColor={(n) => { 
            if (n.type === 'suspectNode') return '#ef4444'; 
            if (n.type === 'vaspNode') return '#10b981'; 
            return '#64748b'; 
          }}
        />
      </ReactFlow>
    </div>
  );
}
