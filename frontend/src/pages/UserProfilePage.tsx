import { useParams, useNavigate } from 'react-router-dom';
import { useAnalysisStore } from '../store/analysisStore';
import OceanRadar from '../components/charts/OceanRadar';
import ActivityHeatmap from '../components/charts/ActivityHeatmap';
import ActivityChart from '../components/charts/ActivityChart';
import NetworkGraph from '../components/charts/NetworkGraph';

export default function UserProfilePage() {
  const { userId } = useParams<{ userId: string }>();
  const { report } = useAnalysisStore();
  const navigate = useNavigate();

  const user = report?.activeUsers.find(u => u.userId === userId)
            ?? report?.silentUsers.find(u => u.userId === userId);

  if (!user) {
    return (
      <>
        <div className="topbar">
          <span className="topbar-title">Kullanıcı Profili</span>
        </div>
        <div className="page-content" style={{ color: 'var(--text-muted)' }}>
          Kullanıcı bulunamadı.{' '}
          <a href="#" onClick={(e) => { e.preventDefault(); navigate('/dashboard'); }}>Geri dön</a>
        </div>
      </>
    );
  }

  const { activity, ocean, socialRole, communication, ideology, llmNarrative } = user;

  return (
    <>
      <div className="topbar">
        <div className="flex items-center" style={{ gap: 12 }}>
          <button className="btn btn-outline" onClick={() => navigate('/dashboard')} style={{ padding: '4px 10px', fontSize: 12 }}>
            ← Geri
          </button>
          <span className="topbar-title">{user.displayName}</span>
          {socialRole?.primaryRole && <span className="badge badge-blue">{socialRole.primaryRole}</span>}
        </div>
        <div className="topbar-right">
          <span>{activity.totalMessages.toLocaleString()} mesaj</span>
        </div>
      </div>

      <div className="page-content">
        {/* Stats Row */}
        <div className="grid grid-4 mb-6">
          <div className="stat-card">
            <div className="stat-label">Toplam Mesaj</div>
            <div className="stat-value">{activity.totalMessages.toLocaleString()}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Toplam Kelime</div>
            <div className="stat-value">{activity.totalWords.toLocaleString()}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Medya</div>
            <div className="stat-value">{activity.mediaCount}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Günlük Ortalama</div>
            <div className="stat-value">{activity.messagesPerDay?.toFixed(1) ?? '—'}</div>
          </div>
        </div>

        {/* AI Narrative */}
        {llmNarrative && (
          <div className="card mb-6">
            <div className="card-header">
              <h3>Karakter Analizi (AI)</h3>
            </div>
            <div className="card-body">
              <div className="narrative-block">{llmNarrative}</div>
            </div>
          </div>
        )}

        {/* OCEAN + Details */}
        <div className="grid grid-2 mb-6">
          <OceanRadar scores={ocean} />

          <div className="card">
            <div className="card-header">
              <h3>İletişim & Profil</h3>
            </div>
            <div className="card-body">
              <table>
                <tbody>
                  <tr style={{ cursor: 'default' }}>
                    <td className="text-muted" style={{ width: 160 }}>En Aktif Saat</td>
                    <td className="font-mono">{activity.mostActiveHour != null ? `${String(activity.mostActiveHour).padStart(2, '0')}:00` : '—'}</td>
                  </tr>
                  <tr style={{ cursor: 'default' }}>
                    <td className="text-muted">En Aktif Gün</td>
                    <td>{activity.mostActiveDay ?? '—'}</td>
                  </tr>
                  <tr style={{ cursor: 'default' }}>
                    <td className="text-muted">Ort. Mesaj Uzunluğu</td>
                    <td className="font-mono">{activity.avgMessageLength?.toFixed(1) ?? '—'} kelime</td>
                  </tr>
                  {communication?.humorType && (
                    <tr style={{ cursor: 'default' }}>
                      <td className="text-muted">Mizah Tipi</td>
                      <td>{communication.humorType}</td>
                    </tr>
                  )}
                  {communication?.formalityLevel != null && (
                    <tr style={{ cursor: 'default' }}>
                      <td className="text-muted">Resmiyet Seviyesi</td>
                      <td>{communication.formalityLevel}/10</td>
                    </tr>
                  )}
                  {communication?.topEmojis && communication.topEmojis.length > 0 && (
                    <tr style={{ cursor: 'default' }}>
                      <td className="text-muted">Sık Kullanılan Emojiler</td>
                      <td style={{ fontSize: 18, letterSpacing: 4 }}>{communication.topEmojis.slice(0, 5).join(' ')}</td>
                    </tr>
                  )}
                  {socialRole?.influenceScore != null && (
                    <tr style={{ cursor: 'default' }}>
                      <td className="text-muted">Etki Skoru (PageRank)</td>
                      <td className="font-mono">{socialRole.influenceScore.toFixed(4)}</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Heatmap */}
        {report?.groupStats?.hourlyHeatmap && (
          <div className="mb-6">
            <ActivityHeatmap heatmap={report.groupStats.hourlyHeatmap} />
          </div>
        )}

        {/* Network */}
        {report?.networkGraph && (
          <div className="mb-6">
            <NetworkGraph graph={report.networkGraph} />
          </div>
        )}

        {/* Ideology */}
        {ideology && ideology.keyValues && ideology.keyValues.length > 0 && (
          <div className="card mb-6">
            <div className="card-header">
              <h3>Değerler & Temalar</h3>
            </div>
            <div className="card-body">
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                {ideology.keyValues.map((v, i) => (
                  <span key={i} className="badge badge-blue">{v}</span>
                ))}
                {ideology.recurringThemes?.map((t, i) => (
                  <span key={`t-${i}`} className="badge badge-amber">{t}</span>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  );
}
