import React, { useState, useEffect } from 'react'
import { trainersAPI } from '../api'

function TrainersPage() {
  const [trainers, setTrainers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchTrainers()
  }, [])

  const fetchTrainers = async () => {
    try {
      setLoading(true)
      const response = await trainersAPI.getAll()
      setTrainers(response.data)
      setError(null)
    } catch (err) {
      setError('Failed to load trainers')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div className="loading">Loading trainers...</div>
  if (error) return <div className="error">{error}</div>

  return (
    <div className="page">
      <h2>Our Trainers</h2>
      {trainers.length === 0 ? (
        <div className="card">
          <p>No trainers available yet.</p>
        </div>
      ) : (
        <div className="grid">
          {trainers.map(trainer => (
            <div key={trainer.id} className="card">
              <div className="trainer-name">{trainer.name}</div>
              <div className="slot-info">
                Specialization: {trainer.specialization}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default TrainersPage

