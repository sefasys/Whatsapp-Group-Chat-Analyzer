/**
 * Execution pipeline hook manager.
 * Orchestrates sequencing flows: Upload → Engine Parsing → Async Processing Engine Poll
 */
import { useCallback } from 'react';
import { useAnalysisStore } from '../store/analysisStore';
import { uploadChat, startAnalysis, pollReport } from '../utils/api';

export function useAnalysis() {
  const { setSessionId, setStatus, setProgress, setError, setReport } = useAnalysisStore();

  const runAnalysis = useCallback(async (file: File, provider: string = 'gemini') => {
    try {
      setStatus('uploading');
      const { sessionId } = await uploadChat(file);
      setSessionId(sessionId);
      setStatus('parsing');
      
      await startAnalysis(sessionId, provider);
      setStatus('analyzing');
      
      const report = await pollReport(sessionId, (pct) => setProgress(pct));
      setReport(report);
    } catch (err: any) {
      setError(err.message ?? 'An unknown system exception occurred.');
    }
  }, [setSessionId, setStatus, setProgress, setError, setReport]);

  return { runAnalysis };
}
