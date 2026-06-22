import React, { useState, useEffect } from 'react'
import { slotsAPI } from '../api'

function SlotsPage() {
  const [slots, setSlots] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchAvailableSlots()
  }, [])

  const fetchAvailableSlots = async () => {
    try {
      setLoading(true)
      const response = await slotsAPI.getAvailable()
      setSlots(response.data)
      setError(null)
    } catch (err) {
      setError('Failed to load training slots')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleString()
  }

  if (loading) return <div className="loading">Loading available slots...</div>
  if (error) return <div className="error">{error}</div>

  return (
    <div className="page">
      <h2>Available Training Slots</h2>
      {slots.length === 0 ? (
        <div className="card">
          <p>No available training slots at the moment.</p>
        </div>
      ) : (
        <div className="grid">
          {slots.map(slot => (
            <div key={slot.id} className="card">
              <div className="trainer-name">
                {slot.trainer?.name || 'Trainer'}
              </div>
              <div className="slot-info">
                <div>Specialization: {slot.trainer?.specialization}</div>
                <div>Date: {formatDate(slot.training_date)}</div>
              </div>
              <div>
                {slot.is_available ? (
                  <span className="available-badge">Available</span>
                ) : (
                  <span className="unavailable-badge">Booked</span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default SlotsPage

