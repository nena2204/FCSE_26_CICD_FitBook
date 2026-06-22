import React, { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import HomePage from './pages/HomePage'
import TrainersPage from './pages/TrainersPage'
import SlotsPage from './pages/SlotsPage'
import BookingPage from './pages/BookingPage'
import BookingsPage from './pages/BookingsPage'

function App() {
  const [activeLink, setActiveLink] = useState('home')
  return (
    <Router>
      <div className="app">
        <nav>
          <h1>FitBook</h1>
          <div className="nav-links">
            <Link to="/" onClick={() => setActiveLink('home')} className={activeLink === 'home' ? 'active' : ''}>Home</Link>
            <Link to="/trainers" onClick={() => setActiveLink('trainers')} className={activeLink === 'trainers' ? 'active' : ''}>Trainers</Link>
            <Link to="/slots" onClick={() => setActiveLink('slots')} className={activeLink === 'slots' ? 'active' : ''}>Slots</Link>
            <Link to="/book" onClick={() => setActiveLink('book')} className={activeLink === 'book' ? 'active' : ''}>Book</Link>
            <Link to="/bookings" onClick={() => setActiveLink('bookings')} className={activeLink === 'bookings' ? 'active' : ''}>Bookings</Link>
          </div>
        </nav>
        <main>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/trainers" element={<TrainersPage />} />
            <Route path="/slots" element={<SlotsPage />} />
            <Route path="/book" element={<BookingPage />} />
            <Route path="/bookings" element={<BookingsPage />} />
          </Routes>
        </main>
        <footer>
          <p>&copy; 2024 FitBook</p>
        </footer>
      </div>
    </Router>
  )
}

export default App
