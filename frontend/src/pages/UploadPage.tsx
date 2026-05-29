import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { useNavigate } from 'react-router-dom';
import { useAnalysis } from '../hooks/useAnalysis';
import { useAnalysisStore } from '../store/analysisStore';

export default function UploadPage() {
  const { runAnalysis } = useAnalysis();
  const { status, progress, error } = useAnalysisStore();
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);
  const [provider, setProvider] = useState<string>('gemini');

  const onDrop = useCallback((accepted: File[]) => {
    if (accepted.length > 0) setFile(accepted[0]);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'text/plain': ['.txt'], 'application/zip': ['.zip'] },
    maxFiles: 1,
    disabled: status === 'uploading' || status === 'parsing' || status === 'analyzing',
  });

  const handleStart = async () => {
    if (!file) return;
    try {
      await runAnalysis(file, provider);
      navigate('/dashboard');
    } catch {
      // Error is already set in the store by useAnalysis
    }
  };

  const isWorking = status === 'uploading' || status === 'parsing' || status === 'analyzing';

  const statusLabel = () => {
    switch (status) {
      case 'uploading': return 'Dosya yükleniyor...';
      case 'parsing': return 'Mesajlar ayrıştırılıyor...';
      case 'analyzing':
        if (progress < 30) return 'Veriler işleniyor...';
        if (progress < 60) return 'İstatistikler hesaplanıyor...';
        if (progress < 80) return 'Ağ grafikleri çıkarılıyor...';
        return 'Yapay zeka analizi yapılıyor...';
      default: return '';
    }
  };

  return (
    <div className="page-center">
      <div className="upload-box">
        <h1>WhatsApp Grup Analizi</h1>
        <p>Bir WhatsApp sohbet dışa aktarım dosyası yükleyin. Yapay zeka destekli analiz ile grubunuzun istatistiklerini, etkileşim ağını ve kişilik profillerini keşfedin.</p>

        <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
          <input {...getInputProps()} />
          <svg className="dropzone-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="17 8 12 3 7 8" />
            <line x1="12" y1="3" x2="12" y2="15" />
          </svg>

          {file ? (
            <>
              <div className="dropzone-title">{file.name}</div>
              <div className="dropzone-sub">{(file.size / 1024).toFixed(1)} KB</div>
            </>
          ) : (
            <>
              <div className="dropzone-title">
                {isDragActive ? 'Dosyayı bırakın' : 'Dosya seçin veya sürükleyin'}
              </div>
              <div className="dropzone-sub">Sohbet dışa aktarımını yükleyin</div>
              <div className="dropzone-formats">
                <span>.txt</span>
                <span>.zip</span>
              </div>
            </>
          )}
        </div>

        {/* Progress */}
        {isWorking && (
          <div style={{ marginTop: 16 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
              <span className="text-sm text-secondary">{statusLabel()}</span>
              <span className="text-sm font-mono">{progress}%</span>
            </div>
            <div className="progress-track">
              <div className="progress-fill" style={{ width: `${progress}%` }} />
            </div>
          </div>
        )}

        {/* Error */}
        {status === 'error' && error && (
          <div style={{ marginTop: 16, padding: '10px 14px', background: '#FEF2F2', border: '1px solid #FECACA', borderRadius: 'var(--radius)', color: '#DC2626', fontSize: 13 }}>
            {error}
          </div>
        )}

        {/* Model Selection */}
        <div style={{ marginTop: 20 }}>
          <label style={{ display: 'block', fontSize: 13, fontWeight: 500, marginBottom: 6, color: 'var(--text-secondary)' }}>
            Yapay Zeka Modeli
          </label>
          <select 
            value={provider} 
            onChange={(e) => setProvider(e.target.value)}
            disabled={isWorking}
            style={{ 
              width: '100%', 
              padding: '8px 12px', 
              borderRadius: 'var(--radius)', 
              border: '1px solid var(--border)', 
              background: 'var(--card-bg)',
              color: 'var(--text-primary)',
              fontSize: 13,
              outline: 'none',
              cursor: isWorking ? 'not-allowed' : 'pointer'
            }}
          >
            <option value="gemini">Gemini 1.5/2.5 Flash (Hızlı & Ücretsiz)</option>
            <option value="claude">Claude 3.5 Sonnet (En Zeki)</option>
            <option value="groq">Groq / Llama 3 (Ultra Hızlı)</option>
          </select>
        </div>

        {/* Action */}
        <div style={{ marginTop: 20 }}>
          <button
            className="btn btn-primary"
            onClick={handleStart}
            disabled={!file || isWorking}
            style={{ width: '100%' }}
          >
            {isWorking ? 'Analiz ediliyor...' : 'Analizi Başlat'}
          </button>
        </div>
      </div>
    </div>
  );
}
