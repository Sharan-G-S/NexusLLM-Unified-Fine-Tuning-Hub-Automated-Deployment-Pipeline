import React, { useState, useEffect, useRef } from 'react';
import { 
  LayoutDashboard, 
  Activity, 
  Settings, 
  MessageSquare, 
  Play, 
  Square, 
  Terminal, 
  Cpu, 
  Database, 
  CheckCircle2,
  AlertCircle,
  Download,
  Search,
  BookOpen
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { getStatus, startTraining, stopTraining, listConfigs, WS_LOGS_URL } from './lib/api';

const Sidebar = ({ activeTab, setActiveTab }) => {
  const tabs = [
    { id: 'overview', icon: LayoutDashboard, label: 'Overview' },
    { id: 'training', icon: Activity, label: 'Training' },
    { id: 'configs', icon: Settings, label: 'Configurations' },
    { id: 'playground', icon: MessageSquare, label: 'Playground' },
  ];

  return (
    <div className="w-64 h-screen glass-card rounded-none border-y-0 border-l-0 p-6 flex flex-col gap-8">
      <div className="flex items-center gap-3 px-2">
        <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center font-bold text-lg">N</div>
        <h1 className="text-xl font-bold tracking-tight">NexusLLM</h1>
      </div>
      <nav className="flex flex-col gap-2">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`nav-link ${activeTab === tab.id ? 'active' : ''}`}
          >
            <tab.icon size={20} />
            {tab.label}
          </button>
        ))}
      </nav>
    </div>
  );
};

const TrainingMonitor = () => {
  const [logs, setLogs] = useState([]);
  const [status, setStatus] = useState('idle');
  const [configs, setConfigs] = useState([]);
  const [selectedConfig, setSelectedConfig] = useState('');
  const [useDeepspeed, setUseDeepspeed] = useState(false);
  const logEndRef = useRef(null);

  useEffect(() => {
    fetchConfigs();
    fetchStatus();
    const interval = setInterval(fetchStatus, 3000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    let ws;
    if (status === 'active') {
      ws = new WebSocket(WS_LOGS_URL);
      ws.onmessage = (event) => {
        setLogs((prev) => [...prev.slice(-100), event.data]);
        logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
      };
    }
    return () => ws?.close();
  }, [status]);

  const fetchConfigs = async () => {
    const res = await listConfigs();
    setConfigs(res.data);
    if (res.data.length > 0) setSelectedConfig(res.data[0]);
  };

  const fetchStatus = async () => {
    const res = await getStatus();
    setStatus(res.data.training);
  };

  const handleStart = async () => {
    await startTraining(selectedConfig, useDeepspeed);
    setStatus('active');
  };

  return (
    <div className="p-8 flex flex-col gap-6 h-full overflow-y-auto">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold">Training Hub</h2>
          <p className="text-white/50">Manage and monitor your fine-tuning jobs.</p>
        </div>
        <div className="flex gap-4">
          {status === 'active' ? (
            <button onClick={stopTraining} className="btn-secondary flex items-center gap-2">
              <Square size={18} /> Stop training
            </button>
          ) : (
            <button onClick={handleStart} className="btn-primary flex items-center gap-2">
              <Play size={18} /> Start training
            </button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6">
        <div className="glass-card p-6 flex flex-col gap-4">
          <h3 className="text-lg font-semibold flex items-center gap-2"><Settings size={18} /> Setup</h3>
          <div className="flex flex-col gap-2">
            <label className="text-sm text-white/60">Select YAML Configuration</label>
            <select 
              value={selectedConfig}
              onChange={(e) => setSelectedConfig(e.target.value)}
              className="bg-white/5 border border-white/10 rounded-lg p-2 outline-none"
            >
              {configs.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
          <div className="flex items-center gap-3 mt-4">
            <input 
              type="checkbox" 
              checked={useDeepspeed} 
              onChange={(e) => setUseDeepspeed(e.target.checked)}
              className="w-4 h-4 rounded bg-primary"
            />
            <label className="text-sm">Use DeepSpeed ZeRO-3</label>
          </div>
        </div>
        
        <div className="col-span-2 glass-card p-6 flex flex-col gap-4">
          <h3 className="text-lg font-semibold flex items-center gap-2"><Terminal size={18} /> Training Logs</h3>
          <div className="bg-black/40 rounded-xl p-4 font-mono text-sm h-64 overflow-y-auto border border-white/5">
            {logs.length === 0 ? (
              <div className="text-white/20 italic">Logs will appear here...</div>
            ) : (
              logs.map((log, i) => <div key={i} className="text-green-400/80">{log}</div>)
            )}
            <div ref={logEndRef} />
          </div>
        </div>
      </div>
    </div>
  );
};

const Layout = ({ children, activeTab, setActiveTab }) => (
  <div className="flex h-screen bg-background bg-gradient-mesh overflow-hidden">
    <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
    <main className="flex-1 h-screen overflow-hidden">
      <AnimatePresence mode="wait">
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.2 }}
          className="h-full"
        >
          {children}
        </motion.div>
      </AnimatePresence>
    </main>
  </div>
);

export default function App() {
  const [activeTab, setActiveTab] = useState('overview');

  return (
    <Layout activeTab={activeTab} setActiveTab={setActiveTab}>
      {activeTab === 'overview' && (
        <div className="p-8 grid grid-cols-2 gap-8">
          <div className="glass-card p-8 flex flex-col gap-4">
            <h2 className="text-2xl font-bold">System Status</h2>
            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 bg-white/5 rounded-2xl flex flex-col gap-1">
                <span className="text-white/40 text-xs">GPU Utilization</span>
                <span className="text-xl font-bold">84%</span>
                <div className="w-full h-1 bg-white/10 rounded-full overflow-hidden mt-2">
                  <div className="w-[84%] h-full bg-primary" />
                </div>
              </div>
              <div className="p-4 bg-white/5 rounded-2xl flex flex-col gap-1">
                <span className="text-white/40 text-xs">VRAM Usage</span>
                <span className="text-xl font-bold">12.4 GB</span>
                <div className="w-full h-1 bg-white/10 rounded-full overflow-hidden mt-2">
                  <div className="w-[60%] h-full bg-accent" />
                </div>
              </div>
            </div>
            <div className="flex flex-col gap-3 mt-4">
              <div className="flex items-center gap-3 text-sm text-green-400">
                <CheckCircle2 size={16} /> LLaMA-Factory Backend Online
              </div>
              <div className="flex items-center gap-3 text-sm text-primary">
                <Cpu size={16} /> DeepSpeed Cluster Identified (1 Node)
              </div>
            </div>
          </div>
          <div className="glass-card p-8 flex flex-col gap-4">
            <h2 className="text-2xl font-bold">Advanced Features</h2>
            <div className="grid grid-cols-1 gap-4">
              <div className="flex items-center gap-4 p-3 bg-white/5 rounded-xl border border-white/5 hover:border-primary/30 transition-all cursor-pointer group">
                <div className="p-2 bg-primary/10 rounded-lg group-hover:bg-primary/20 transition-all">
                  <Download size={20} className="text-primary" />
                </div>
                <div>
                  <div className="font-semibold text-sm">Model Export & Quantization</div>
                  <div className="text-xs text-white/40">GGUF/AWQ export for edge deployment</div>
                </div>
              </div>
              <div className="flex items-center gap-4 p-3 bg-white/5 rounded-xl border border-white/5 hover:border-secondary/30 transition-all cursor-pointer group">
                <div className="p-2 bg-secondary/10 rounded-lg group-hover:bg-secondary/20 transition-all">
                  <Search size={20} className="text-secondary" />
                </div>
                <div>
                  <div className="font-semibold text-sm">RAG Integration Framework</div>
                  <div className="text-xs text-white/40">FAISS-powered external knowledge retrieval</div>
                </div>
              </div>
              <div className="flex items-center gap-4 p-3 bg-white/5 rounded-xl border border-white/5 hover:border-accent/30 transition-all cursor-pointer group">
                <div className="p-2 bg-accent/10 rounded-lg group-hover:bg-accent/20 transition-all">
                  <BookOpen size={20} className="text-accent" />
                </div>
                <div>
                  <div className="font-semibold text-sm">Automated Notebook Generator</div>
                  <div className="text-xs text-white/40">One-click Colab/Jupyter compatibility</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
      {activeTab === 'training' && <TrainingMonitor />}
      {activeTab === 'playground' && (
        <div className="p-8 h-full flex flex-col gap-4">
          <h2 className="text-3xl font-bold">Model Playground</h2>
          <div className="flex-1 glass-card p-6 flex flex-col gap-4 relative">
            <div className="flex-1 flex flex-col gap-4 overflow-y-auto p-4 bg-black/20 rounded-2xl border border-white/5">
              <div className="flex gap-3 bg-white/5 p-4 rounded-2xl max-w-[80%]">
                <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center font-bold">N</div>
                <div className="flex-1 text-sm leading-relaxed">
                  Hello! I am your Nexus-trained Financial Analyst. How can I assist you with market data today?
                </div>
              </div>
            </div>
            <div className="mt-auto flex gap-3">
              <input 
                placeholder="Ask your model about market sentiment..."
                className="flex-1 bg-white/5 border border-white/10 rounded-2xl px-6 py-4 outline-none focus:border-primary/50 transition-all"
              />
              <button className="btn-primary px-8">Send</button>
            </div>
          </div>
        </div>
      )}
    </Layout>
  );
}
