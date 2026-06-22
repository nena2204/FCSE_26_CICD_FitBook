import React, { useState, useEffect } from 'react'
import { bookingsAPI } from '../api'

function BookingsPage() {
  const [bookings, setBookings] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)

  useEffect(() => {
    fetchBookings()
  }, [])

  const fetchBookings = async () => {
    try {
      setLoading(true)
      const response = await bookingsAPI.getAll()
      setBookings(response.data)
      setError(null)
    } catch (err) {
      setError('Failed to load bookings')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleCancel = async (bookingId) => {
    if (window.confirm('Are you sure you want to cancel this booking?')) {
      try {
        await bookingsAPI.delete(bookingId)
        setSuccess('Booking cancelled successfully!')
        fetchBookings()
        setTimeout(() => setSuccess(null), 3000)
      } catch (err) {
        setError('Failed to cancel booking: ' + err.message)
        console.error(err)
      }
    }
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleString()
  }

  if (loading) return <div className="loading">Loading bookings...</div>

  return (
    <div className="page">
      <h2>My Bookings</h2>
      {success && <div className="success">{success}</div>}
      {error && <div className="error">{error}</div>}

      {bookings.length === 0 ? (
        <div className="card">
          <p>You have no bookings yet.</p>
        </div>
      ) : (
        <div>
          {bookings.map(booking => (
            <div key={booking.id} className="card">
              <div className="trainer-name">
                {booking.training_slot?.trainer?.name || 'Training'}
              </div>
              <div className="slot-info">
                <div>Client: {booking.client_name}</div>
                <div>
                  Specialization: {booking.training_slot?.trainer?.specialization}
                </div>
                <div>
                  Date: {formatDate(booking.training_slot?.training_date)}
                </div>
                <div>Booked on: {formatDate(booking.created_at)}</div>
              </div>
              <div className="button-group">
                <button
                  className="secondary"
                  onClick={() => handleCancel(booking.id)}
                >
                  Cancel Booking
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default BookingsPage

