/**
 * Core HTTP Client API interactions layer.
 */
import axios from 'axios';
import { GroupReport } from '../types';

const BASE = 'http://localhost:8000/api';

export async function uploadChat(file: File): Promise<{ sessionId: string }> {
  const form = new FormData();
  form.append('file', file);
  const res = await axios.post(`${BASE}/upload`, form);
  return res.data;
}

export async function startAnalysis(sessionId: string): Promise<void> {
  await axios.post(`${BASE}/analyze/${sessionId}`);
}

export async function pollReport(
  sessionId: string,
  onProgress: (pct: number) => void): Promise<GroupReport> {
  return new Promise((resolve, reject) => {
    const interval = setInterval(async () => {
      try {
        const res = await axios.get(`${BASE}/report/${sessionId}`);
        const { status, progress, report } = res.data;
        onProgress(progress);
        if (status === 'completed') {
          clearInterval(interval);
          resolve(report);
        } else if (status === 'failed') {
          clearInterval(interval);
          reject(new Error(res.data.error));
        }
      } catch (e) {
        clearInterval(interval);
        reject(e);
      }
    }, 2000);
  });
}

export async function getUserProfile(sessionId: string, userId: string) {
  const res = await axios.get(`${BASE}/user/${sessionId}/${userId}`);
  return res.data;
}
