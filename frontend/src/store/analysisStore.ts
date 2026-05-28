/**
 * Global State Management (Zustand).
 * Tracks UI tracking matrices, asynchronous jobs progress states, and final diagnostic reports data stores.
 */
import { create } from 'zustand';
import { GroupReport, AnalysisStatus } from '../types';

interface AnalysisStore {
  sessionId: string | null;
  status: AnalysisStatus;
  progress: number;
  error: string | null;
  report: GroupReport | null;
  selectedUserId: string | null;
  setSessionId: (id: string) => void;
  setStatus: (status: AnalysisStatus) => void;
  setProgress: (pct: number) => void;
  setError: (msg: string) => void;
  setReport: (report: GroupReport) => void;
  selectUser: (userId: string | null) => void;
  reset: () => void;
}

export const useAnalysisStore = create<AnalysisStore>((set) => ({
  sessionId: null,
  status: 'idle',
  progress: 0,
  error: null,
  report: null,
  selectedUserId: null,
  setSessionId: (id) => set({ sessionId: id }),
  setStatus: (status) => set({ status }),
  setProgress: (progress) => set({ progress }),
  setError: (error) => set({ error, status: 'error' }),
  setReport: (report) => set({ report, status: 'completed' }),
  selectUser: (selectedUserId) => set({ selectedUserId }),
  reset: () => set({ sessionId: null, status: 'idle', progress: 0, error: null, report: null }),
}));
