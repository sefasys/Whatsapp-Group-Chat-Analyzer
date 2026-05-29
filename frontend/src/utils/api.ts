/**
 * Core HTTP Client — Backend API iletişim katmanı.
 */
import axios from 'axios';
import { GroupReport } from '../types';

const BASE = 'http://localhost:8000/api';

export async function uploadChat(file: File): Promise<{ sessionId: string }> {
  const form = new FormData();
  form.append('file', file);
  const res = await axios.post(`${BASE}/upload`, form);
  // Backend snake_case döndürüyor → camelCase'e çevir
  return { sessionId: res.data.session_id };
}

export async function startAnalysis(sessionId: string, provider: string = 'gemini'): Promise<void> {
  await axios.post(`${BASE}/analyze/${sessionId}?provider=${provider}`);
}

export async function pollReport(
  sessionId: string,
  onProgress: (pct: number) => void
): Promise<GroupReport> {
  return new Promise((resolve, reject) => {
    const interval = setInterval(async () => {
      try {
        const res = await axios.get(`${BASE}/report/${sessionId}`);
        const data = res.data;

        onProgress(data.progress ?? 0);

        if (data.status === 'completed') {
          clearInterval(interval);
          // Backend "result" alanında tutuyor
          resolve(data.result as GroupReport);
        } else if (data.status === 'failed') {
          clearInterval(interval);
          const errMsg = data.result?.error ?? data.error ?? 'Analiz başarısız oldu.';
          reject(new Error(errMsg));
        }
      } catch (e) {
        clearInterval(interval);
        reject(e);
      }
    }, 2000);
  });
}
