import { NavLink } from 'react-router-dom';
import { useAnalysisStore } from '../store/analysisStore';

export default function Sidebar() {
  const { report } = useAnalysisStore();
  const users = report?.activeUsers ?? [];

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <h2>WA Analyzer</h2>
        <span>Grup Sohbet Analizi</span>
      </div>

      <ul className="sidebar-nav">
        <li>
          <NavLink to="/" className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
            Dosya Yükle
          </NavLink>
        </li>
        <li>
          <NavLink to="/dashboard" className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
            Genel Bakış
          </NavLink>
        </li>

        {users.length > 0 && (
          <>
            <li className="sidebar-section-title">Kullanıcılar</li>
            {users.map(u => (
              <li key={u.userId}>
                <NavLink
                  to={`/user/${u.userId}`}
                  className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                  {u.displayName}
                </NavLink>
              </li>
            ))}
          </>
        )}
      </ul>
    </aside>
  );
}
