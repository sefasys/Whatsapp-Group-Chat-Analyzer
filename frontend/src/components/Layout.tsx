import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';

export default function Layout({ topbarTitle }: { topbarTitle?: string }) {
  return (
    <div className="app-layout">
      <Sidebar />
      <div className="main-content">
        <Outlet />
      </div>
    </div>
  );
}
