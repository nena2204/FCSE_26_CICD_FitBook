import React, { useState, useEffect } from 'react'
import { slotsAPI, bookingsAPI } from '../api'

function BookingPage() {
  const [slots, setSlots] = useState([])
  const [clientName, setClientName] = useState('')
  const [selectedSlot, setSelectedSlot] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)

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
      setError('Failed to load available slots')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!clientName.trim()) {
      setError('Please enter your name')
      return
    }
    if (!selectedSlot) {
      setError('Please select a training slot')
      return
    }

    try {
      await bookingsAPI.create(clientName, parseInt(selectedSlot))
      setSuccess('Booking created successfully!')
      setClientName('')
      setSelectedSlot('')
      setTimeout(() => setSuccess(null), 3000)
    } catch (err) {
      setError('Failed to create booking: ' + (err.response?.data?.detail || err.message))
      console.error(err)
    }
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleString()
  }

  if (loading) return <div className="loading">Loading available slots...</div>

  return (
    <div className="page">
      <h2>Book a Training Session</h2>
      {success && <div className="success">{success}</div>}
      {error && <div className="error">{error}</div>}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Your Name</label>
          <input
            id="name"
            type="text"
            value={clientName}
            onChange={(e) => setClientName(e.target.value)}
            placeholder="Enter your name"
          />
        </div>

        <div className="form-group">
          <label htmlFor="slot">Select Training Slot</label>
          <select
            id="slot"
            value={selectedSlot}
            onChange={(e) => setSelectedSlot(e.target.value)}
          >
            <option value="">-- Choose a slot --</option>
            {slots.map(slot => (
              <option key={slot.id} value={slot.id}>
                {slot.trainer?.name} ({slot.trainer?.specialization}) - {formatDate(slot.training_date)}
              </option>
            ))}
          </select>
        </div>

        <button type="submit">Book Training</button>
      </form>
    </div>
  )
}

export default BookingPage

