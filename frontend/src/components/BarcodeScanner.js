import React from 'react';
import { useZxing } from 'react-zxing';

export const BarcodeScanner = ({ onResult, onError }) => {
  const { ref } = useZxing({
    onResult: (result) => {
      onResult(result.getText());
    },
    onError: (error) => {
      onError(error);
    },
  });

  return (
    <>
      <video ref={ref} />
      <p>
        <span>Last result:</span>
        <span></span>
      </p>
    </>
  );
};