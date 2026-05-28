/**
 * Main dashboard landing root. File ingest dropping field.
 */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import FileDropzone from '../components/upload/FileDropzone';
import { useAnalysis } from '../hooks/useAnalysis';
import { useAnalysisStore } from '../store/analysisStore';

export default function UploadPage() {
  const { runAnalysis } = useAnalysis();
  const navigate = useNavigate();

  const handleFile = async (file: File) => {
    await runAnalysis(file);
    navigate('/dashboard');
  };

  return (
    <div>
      {/* FileDropzone component mounts here */}
    </div>
  );
}
