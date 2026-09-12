import React from 'react';
import { Search, ZoomIn, ZoomOut, Focus, Check, ShieldAlert } from 'lucide-react';
import TransactionGraph from './components/TransactionGraph';

function App() {
  return (
    <div className="h-screen w-full flex flex-col font-sans bg-slate-950 text-slate-200 overflow-hidden">
      
      {/* 1. Top Search Workspace (Header) */}
      <header className="flex-none flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-950/50 backdrop-blur-sm z-10">
        <div className="flex items-center space-x-6 w-full max-w-5xl">
          <div className="flex items-center space-x-2">
            <ShieldAlert className="w-6 h-6 text-blue-500" />
            <h1 className="text-lg font-semibold tracking-tight text-slate-100">Genesis Blockers</h1>
          </div>
          
          <div className="flex-1 flex items-center space-x-3 bg-slate-900/50 p-1.5 rounded-md border border-slate-800/50">
            <div className="flex-1 relative">
              <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
              <input 
                type="text" 
                placeholder="0x..." 
                className="w-full bg-slate-900 border border-slate-700 rounded-sm py-1.5 pl-9 pr-3 text-sm font-mono text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors"
                defaultValue="0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
              />
            </div>
            
            <select 
              disabled 
              className="bg-slate-900 border border-slate-700 rounded-sm py-1.5 px-3 text-sm text-slate-400 opacity-70 cursor-not-allowed appearance-none"
            >
              <option>Ethereum</option>
            </select>
            
            <div className="flex items-center space-x-2 px-2 border-l border-slate-800">
              <label className="text-xs text-slate-400 font-medium whitespace-nowrap">Max Hops</label>
              <input 
                type="number" 
                min="1" max="20" defaultValue="5"
                className="w-16 bg-slate-900 border border-slate-700 rounded-sm py-1 text-center text-sm text-slate-200 focus:outline-none focus:border-blue-500"
              />
            </div>
            
            <button className="bg-slate-800 border border-slate-700 text-slate-200 hover:bg-slate-700 px-4 py-1.5 rounded-sm text-sm font-medium transition-colors whitespace-nowrap">
              Run Investigation
            </button>
          </div>
        </div>
      </header>

      {/* Main Workspace */}
      <main className="flex-1 flex overflow-hidden">
        
        {/* 2. Main Workspace - Left Pane (Graph Canvas) */}
        <section className="relative w-[70%] h-full bg-slate-900 border-r border-slate-800 flex flex-col">
          <TransactionGraph />
          
          {/* Floating Control Overlay */}
          <div className="absolute bottom-6 left-6 z-20 flex flex-col bg-slate-950 border border-slate-800 rounded-md shadow-xl overflow-hidden">
            <button className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors border-b border-slate-800" title="Zoom In">
              <ZoomIn className="w-4 h-4" />
            </button>
            <button className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors border-b border-slate-800" title="Zoom Out">
              <ZoomOut className="w-4 h-4" />
            </button>
            <button className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors" title="Recenter">
              <Focus className="w-4 h-4" />
            </button>
          </div>
        </section>

        {/* 3. Main Workspace - Right Pane (Attribution Sidebar) */}
        <aside className="w-[30%] h-full bg-slate-950 p-5 overflow-y-auto custom-scrollbar flex flex-col space-y-6">
          
          {/* Investigation Summary Card */}
          <div className="flex flex-col space-y-1 pb-4 border-b border-slate-800/50">
            <div className="flex items-center justify-between">
              <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Investigation</h2>
              <span className="text-xs font-mono text-slate-500">INV-2026-0001</span>
            </div>
            <p className="text-sm text-slate-500 mt-2">
              <span className="text-slate-300 font-medium">25</span> Transactions Analyzed
            </p>
          </div>

          {/* VASP Match Card */}
          <div className="bg-slate-900/50 border border-slate-800 rounded-md p-4 flex flex-col space-y-4">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="text-sm font-medium text-slate-400">Nearest VASP Match</h3>
                <p className="text-2xl font-semibold text-slate-100 mt-1 tracking-tight">Demo VASP</p>
              </div>
              <div className="bg-red-500/10 border border-red-500/20 text-red-400 text-xs font-bold px-2 py-1 rounded shadow-sm">
                CRITICAL
              </div>
            </div>
            
            <div className="flex items-center space-x-4 pt-2">
              <div className="flex flex-col">
                <span className="text-xs text-slate-500">Confidence</span>
                <span className="text-lg font-mono text-emerald-400">91.0%</span>
              </div>
              <div className="w-px h-8 bg-slate-800"></div>
              <div className="flex flex-col">
                <span className="text-xs text-slate-500">Graph Distance</span>
                <span className="text-lg font-mono text-slate-200">3 Hops</span>
              </div>
            </div>
          </div>

          {/* Evidence List */}
          <div className="flex flex-col space-y-3 pt-2">
            <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Attribution Evidence</h4>
            
            <div className="space-y-2">
              {/* Evidence Item 1 */}
              <div className="bg-slate-900 border border-slate-800/80 rounded p-3 flex items-start space-x-3 hover:border-slate-700 transition-colors">
                <div className="mt-0.5 bg-emerald-500/20 p-1 rounded-full">
                  <Check className="w-3 h-3 text-emerald-400" />
                </div>
                <div className="flex-1">
                  <p className="text-sm text-slate-300 leading-snug">Direct transfer of 50.5 ETH to known deposit address.</p>
                </div>
                <div className="text-right">
                  <span className="text-xs font-mono text-slate-500">Str: 0.95</span>
                </div>
              </div>

              {/* Evidence Item 2 */}
              <div className="bg-slate-900 border border-slate-800/80 rounded p-3 flex items-start space-x-3 hover:border-slate-700 transition-colors">
                <div className="mt-0.5 bg-emerald-500/20 p-1 rounded-full">
                  <Check className="w-3 h-3 text-emerald-400" />
                </div>
                <div className="flex-1">
                  <p className="text-sm text-slate-300 leading-snug">Repeated interactions with nested mixer cluster.</p>
                </div>
                <div className="text-right">
                  <span className="text-xs font-mono text-slate-500">Str: 0.82</span>
                </div>
              </div>

              {/* Evidence Item 3 */}
              <div className="bg-slate-900 border border-slate-800/80 rounded p-3 flex items-start space-x-3 hover:border-slate-700 transition-colors">
                <div className="mt-0.5 bg-emerald-500/20 p-1 rounded-full">
                  <Check className="w-3 h-3 text-emerald-400" />
                </div>
                <div className="flex-1">
                  <p className="text-sm text-slate-300 leading-snug">Temporal correlation with known phishing campaign.</p>
                </div>
                <div className="text-right">
                  <span className="text-xs font-mono text-slate-500">Str: 0.74</span>
                </div>
              </div>
            </div>
          </div>
          
        </aside>
      </main>
    </div>
  );
}

export default App;
