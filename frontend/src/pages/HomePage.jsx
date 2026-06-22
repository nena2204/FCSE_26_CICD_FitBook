import React from 'react'

function HomePage() {
  return (
    <div className="page">
      <h2>Welcome to FitBook</h2>
      <div className="card">
        <p>
          FitBook is your modern online training booking system. Browse available trainers,
          check training sessions, and book your next fitness class in just a few clicks.
        </p>
        <ul style={{ marginTop: '1rem' }}>
          <li>Browse talented trainers from various specializations</li>
          <li>View available training sessions</li>
          <li>Book training sessions easily</li>
          <li>Manage your bookings</li>
        </ul>
      </div>
      <div className="card">
        <h3>Get Started</h3>
        <p>Start by browsing our trainers or checking available training slots!</p>
      </div>
    </div>
  )
}

export default HomePage

