import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import UploadPage from './pages/UploadPage';
import DashboardPage from './pages/DashboardPage';
import UserProfilePage from './pages/UserProfilePage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Upload page — full screen, no sidebar */}
        <Route path="/" element={<UploadPage />} />

        {/* Dashboard layout — sidebar visible */}
        <Route element={<Layout />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/user/:userId" element={<UserProfilePage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
