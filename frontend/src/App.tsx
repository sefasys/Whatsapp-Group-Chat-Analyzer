import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import UploadPage from './pages/UploadPage';
import DashboardPage from './pages/DashboardPage';
import UserProfilePage from './pages/UserProfilePage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={ <UploadPage /> } />
        <Route path="/dashboard" element={ <DashboardPage /> } />
        <Route path="/user/:userId" element={ <UserProfilePage /> } />
      </Routes>
    </BrowserRouter>
  );
}
