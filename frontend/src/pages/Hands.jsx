import { useState } from 'react'
import { useData } from '../context/DataContext'

function Hands() {
    const { hands, loading } = useData()
    const [filter, setFilter] = useState({ position: '', action: '' })
    const filtered = hands.filter(hand => {
        if (filter.position && hand.hero_position !== filter.position) return false
        if (filter.action && hand.hero_preflop_action !== filter.action) return false
        return true
    })
    const [page, setPage] = useState(0)
    const PER_PAGE = 50

  if (loading) return <p className="loading">Chargement...</p>

  return (
    <div className="hands-page">
      <div className="hands-page__header">
        <h1 className="hands-page__title">Mes mains</h1>
        <p className="hands-page__sub">{filtered.length} mains</p>
      </div>

      <div className="hands-filters">
        <select
          className="hands-filter"
          value={filter.position}
          onChange={e => setFilter(f => ({ ...f, position: e.target.value }))}
        >
          <option value="">Toutes positions</option>
          <option value="BTN">BTN</option>
          <option value="SB">SB</option>
          <option value="BB">BB</option>
        </select>

        <select
          className="hands-filter"
          value={filter.action}
          onChange={e => setFilter(f => ({ ...f, action: e.target.value }))}
        >
          <option value="">Toutes actions</option>
          <option value="fold">Fold</option>
          <option value="raise">Raise</option>
          <option value="call">Call</option>
          <option value="allin">Allin</option>
          <option value="check">Check</option>
        </select>
      </div>

      <table className="hands-table">
        <thead>
          <tr>
            <th>Score</th>
            <th>Position</th>
            <th>Stack BB</th>
            <th>Cartes</th>
            <th>Action</th>
            <th>Résultat</th>
          </tr>
        </thead>
        <tbody>
          {filtered.slice(page * PER_PAGE, (page + 1) * PER_PAGE).map(hand => (
            <tr key={hand.hand_id}>
              <td>
                <span className="score-pending">—</span>
              </td>
              <td>{hand.hero_position}</td>
              <td>{hand.hero_stack_bb} BB</td>
              <td>{JSON.parse(hand.hero_cards).join(' ')}</td>
              <td>
                <span className={`action-badge action-badge--${hand.hero_preflop_action}`}>
                  {hand.hero_preflop_action}
                </span>
              </td>
              <td className={hand.hero_won ? 'won' : 'lost'}>
                {hand.hero_won ? `+${hand.hero_chips_won}` : '−'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
            <div className="pagination">
                    <button
                        className="pagination__btn"
                        onClick={() => setPage(p => p - 1)}
                        disabled={page === 0}
                    >
                        ←
                    </button>
                    <span className="pagination__info">
                        {page + 1} / {Math.ceil(filtered.length / PER_PAGE)}
                    </span>
                    <button
                        className="pagination__btn"
                        onClick={() => setPage(p => p + 1)}
                        disabled={(page + 1) * PER_PAGE >= filtered.length}
                    >
                        →
                    </button>
                    </div>
            </div>
  )
}

export default Hands