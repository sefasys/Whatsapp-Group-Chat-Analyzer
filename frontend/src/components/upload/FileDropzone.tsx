import React from 'react';
import { useDropzone } from 'react-dropzone';

interface Props {
  onFile: (file: File) => void;
}

export default function FileDropzone({ onFile }: Props) {
  const { getRootProps, getInputProps } = useDropzone({
    accept: { 'text/plain': ['.txt'], 'application/zip': ['.zip'] },
    maxFiles: 1,
    onDrop: (accepted) => { if (accepted[0]) onFile(accepted[0]); },
  });

  return (
    <div { ...getRootProps() }>
      <input { ...getInputProps() } />
    </div>
  );
}
