import { useNavigate } from 'react-router-dom';
import { useAnalysisStore } from '../store/analysisStore';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function DashboardPage() {
  const { report } = useAnalysisStore();
  const navigate = useNavigate();

  if (!report) {
    return (
      <>
        <div className="topbar">
          <span className="topbar-title">Genel Bakış</span>
        </div>
        <div className="page-content" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)' }}>
          Henüz analiz yapılmadı. Önce bir dosya yükleyin.
        </div>
      </>
    );
  }

  const { activeUsers, groupStats, groupDynamicsSummary } = report;
  const totalMessages = groupStats?.totalMessages ?? activeUsers.reduce((s, u) => s + u.activity.totalMessages, 0);

  return (
    <>
      <div className="topbar">
        <span className="topbar-title">Genel Bakış</span>
        <div className="topbar-right">
          <span>{activeUsers.length} kullanıcı</span>
          <span>•</span>
          <span>{totalMessages.toLocaleString()} mesaj</span>
        </div>
      </div>

      <div className="page-content">
        {/* KPI Cards */}
        <div className="grid grid-4 mb-6">
          <div className="stat-card">
            <div className="stat-label">Toplam Mesaj</div>
            <div className="stat-value">{totalMessages.toLocaleString()}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Aktif Kullanıcı</div>
            <div className="stat-value">{activeUsers.length}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Sessiz Kullanıcı</div>
            <div className="stat-value">{report.silentUsers?.length ?? 0}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Ort. Mesaj/Kullanıcı</div>
            <div className="stat-value">
              {activeUsers.length > 0 ? Math.round(totalMessages / activeUsers.length).toLocaleString() : 0}
            </div>
          </div>
        </div>

        {/* Activity Chart */}
        {groupStats?.dailyActivity && groupStats.dailyActivity.length > 0 && (
          <div className="card mb-6">
            <div className="card-header">
              <h3>Günlük Aktivite</h3>
            </div>
            <div className="card-body" style={{ height: 280 }}>
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={groupStats.dailyActivity} margin={{ top: 8, right: 8, left: -16, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
                  <XAxis
                    dataKey="date"
                    tick={{ fontSize: 11, fill: 'var(--text-muted)' }}
                    tickLine={false}
                    axisLine={false}
                    minTickGap={40}
                  />
                  <YAxis
                    tick={{ fontSize: 11, fill: 'var(--text-muted)' }}
                    tickLine={false}
                    axisLine={false}
                  />
                  <Tooltip
                    contentStyle={{
                      background: '#fff',
                      border: '1px solid var(--border)',
                      borderRadius: 4,
                      fontSize: 12,
                    }}
                  />
                  <Area
                    type="monotone"
                    dataKey="count"
                    stroke="var(--accent)"
                    fill="var(--accent-light)"
                    strokeWidth={2}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {/* Group Dynamics */}
        {groupDynamicsSummary && (
          <div className="card mb-6">
            <div className="card-header">
              <h3>Grup Dinamiği (AI Özeti)</h3>
            </div>
            <div className="card-body">
              <div className="narrative-block">{groupDynamicsSummary}</div>
            </div>
          </div>
        )}

        {/* Users Table */}
        <div className="card">
          <div className="card-header">
            <h3>Kullanıcılar</h3>
            <span className="text-xs text-muted">{activeUsers.length} kişi</span>
          </div>
          <div className="card-body" style={{ padding: 0 }}>
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Kullanıcı</th>
                    <th>Mesaj</th>
                    <th>Kelime</th>
                    <th>Medya</th>
                    <th>Rol</th>
                    <th>Ort. Mesaj Uzunluğu</th>
                  </tr>
                </thead>
                <tbody>
                  {activeUsers
                    .slice()
                    .sort((a, b) => b.activity.totalMessages - a.activity.totalMessages)
                    .map(user => (
                      <tr key={user.userId} onClick={() => navigate(`/user/${user.userId}`)}>
                        <td>
                          <div className="flex items-center gap-4" style={{ gap: 10 }}>
                            <div className="avatar">
                              {user.displayName.substring(0, 2).toUpperCase()}
                            </div>
                            <span style={{ fontWeight: 500 }}>{user.displayName}</span>
                          </div>
                        </td>
                        <td className="font-mono">{user.activity.totalMessages.toLocaleString()}</td>
                        <td className="font-mono">{user.activity.totalWords.toLocaleString()}</td>
                        <td className="font-mono">{user.activity.mediaCount}</td>
                        <td>
                          {user.socialRole?.primaryRole && (
                            <span className="badge badge-blue">{user.socialRole.primaryRole}</span>
                          )}
                        </td>
                        <td className="font-mono">{user.activity.avgMessageLength?.toFixed(1) ?? '—'}</td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
