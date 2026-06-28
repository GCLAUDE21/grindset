import { createContext, useContext, useState, useEffect } from 'react'
import axios from 'axios'
import API from '../config/api'

const DataContext = createContext()

export function DataProvider({ children }) {
  const [hands, setHands] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      axios.get(`${API}/hands/?limit=181044`),
      axios.get(`${API}/stats/`)
    ]).then(([handsRes, statsRes]) => {
      setHands(handsRes.data.hands)
      setStats(statsRes.data)
      setLoading(false)
    }).catch(err => {
      console.error(err)
      setLoading(false)
    })
  }, [])

  return (
    <DataContext.Provider value={{ hands, stats, loading }}>
      {children}
    </DataContext.Provider>
  )
}

export function useData() {
  return useContext(DataContext)
}