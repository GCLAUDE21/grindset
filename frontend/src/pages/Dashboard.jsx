import { useData } from '../context/DataContext'


function Dashboard() {
  const { hands, stats, loading } = useData()

  if (loading) return <p className="loading">Chargement...</p>

  return (
    <div className="dashboard">

        <div className="dashboard__header">
        <div className="status-card">
            <div className="status-card__left">
                <p className="status-card__label">IQ SCORE</p>
                <div className="status-card__score-row">
                <p className="status-card__value">742</p>
                <div className="status-card__sparkline">
                    <svg viewBox="0 0 80 30" fill="none">
                    <polyline
                        points="0,25 15,20 30,22 45,15 60,8 80,12"
                        stroke="#c9a84c"
                        strokeWidth="1.5"
                        fill="none"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    />
                    <circle cx="80" cy="12" r="2.5" fill="#c9a84c"/>
                    </svg>
                </div>
                </div>
                <p className="status-card__delta">+38 pts cette semaine</p>
            </div>
            <div className="status-card__right">
                <div className="status-card__light status-card__light--green">
                <span>Prêt à jouer</span>
                </div>
                <p className="status-card__sessions">127 sessions · 181 044 mains</p>
            </div>
            </div>
        </div>

        <div className="objectives">
            <h2 className="objectives__title">Objectifs du mois</h2>
            <div className="objectives__list">
                <div className="objective">
                <div className="objective__header">
                    <span className="objective__label">Volume</span>
                    <span className="objective__nums"><strong>312</strong> / 400 mains</span>
                </div>
                <div className="objective__bar">
                    <div className="objective__fill" style={{ width: '78%' }}></div>
                </div>
                </div>
                <div className="objective">
                <div className="objective__header">
                    <span className="objective__label">IQ Score cible</span>
                    <span className="objective__nums"><strong>742</strong> / 780 pts</span>
                </div>
                <div className="objective__bar">
                    <div className="objective__fill objective__fill--purple" style={{ width: '95%' }}></div>
                </div>
                </div>
                <div className="objective">
                <div className="objective__header">
                    <span className="objective__label">Drills complétés</span>
                    <span className="objective__nums"><strong>47</strong> / 60 drills</span>
                </div>
                <div className="objective__bar">
                    <div className="objective__fill objective__fill--gold" style={{ width: '78%' }}></div>
                </div>
                </div>
            </div>
            </div>

            <div className="pre-session">
                <h2 className="pre-session__title">Avant de jouer</h2>
                <div className="warmup-banner">
                    <div className="warmup-banner__left">
                    <i className="ti ti-flame"></i>
                    <div>
                        <p className="warmup-banner__title">Échauffement disponible</p>
                        <p className="warmup-banner__sub">3 spots ciblés sur ton leak principal : fold trop tight BTN 8-12BB</p>
                    </div>
                    </div>
                    <button className="warmup-banner__btn">Démarrer</button>
                </div>
                <div className="leaks-list">
                    <div className="leak">
                    <span className="leak__dot leak__dot--red"></span>
                    <span className="leak__text">Over-fold face à push BTN · 8-12BB</span>
                    <span className="leak__ev">-0.8 EV/main</span>
                    </div>
                    <div className="leak">
                    <span className="leak__dot leak__dot--orange"></span>
                    <span className="leak__text">Call trop large BB vs open CO</span>
                    <span className="leak__ev">-0.4 EV/main</span>
                    </div>
                    <div className="leak">
                    <span className="leak__dot leak__dot--orange"></span>
                    <span className="leak__text">Push trop tight Axs · 10BB SB</span>
                    <span className="leak__ev">-0.3 EV/main</span>
                    </div>
                </div>
                </div>

                <div className="last-session">
                    <h2 className="last-session__title">Dernière session</h2>
                    <div className="last-session__card">
                        <div className="last-session__meta">
                        <span className="last-session__date">28 juin 2026</span>
                        <span className="last-session__hands">21 mains</span>
                        <span className="last-session__result last-session__result--pos">+5022 chips</span>
                        </div>
                        <div className="last-session__errors">
                        <p className="last-session__error">
                            <i className="ti ti-alert-triangle"></i>
                            Fold A7o à 9BB en BTN face à push SB · -1.2 EV
                        </p>
                        <p className="last-session__error">
                            <i className="ti ti-alert-triangle"></i>
                            Fold A2s à 11BB en SB face à push BTN · -0.9 EV
                        </p>
                        </div>
                    </div>
                    </div>

    </div>
    )
}

export default Dashboard