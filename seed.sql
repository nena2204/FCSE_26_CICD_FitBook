-- Izbrisi gi starite podatoci i resetiraj gi ID vrednostite
TRUNCATE TABLE bookings, training_slots, trainers
RESTART IDENTITY CASCADE;


-- 1. Treneri
INSERT INTO trainers (name, specialization)
VALUES
    ('Marko Andonov', 'Strength Training'),
    ('Ana Nikolova', 'Yoga'),
    ('Stefan Iliev', 'CrossFit'),
    ('Elena Stojanova', 'Pilates'),
    ('Daniel Ristov', 'Cardio & Conditioning');


-- 2. Termini za narednite 7 dena
WITH days AS (
    SELECT generate_series(
        DATE '2026-07-02',
        DATE '2026-07-08',
        INTERVAL '1 day'
    )::date AS training_day
),
times AS (
    SELECT *
    FROM (
        VALUES
            (TIME '08:00'),
            (TIME '10:00'),
            (TIME '16:00'),
            (TIME '18:00')
    ) AS available_times(training_time)
)
INSERT INTO training_slots (
    trainer_id,
    training_date,
    is_available
)
SELECT
    trainers.id,
    days.training_day + times.training_time,
    TRUE
FROM trainers
CROSS JOIN days
CROSS JOIN times
WHERE EXTRACT(ISODOW FROM days.training_day) <> 7;

-- 3. Nekolku probni rezervacii
WITH selected_slots AS (
    SELECT
        id,
        ROW_NUMBER() OVER (ORDER BY training_date) AS row_number
    FROM training_slots
    WHERE is_available = TRUE
    ORDER BY training_date
    LIMIT 6
)
INSERT INTO bookings (
    client_name,
    training_slot_id,
    created_at
)
SELECT
    CASE row_number
        WHEN 1 THEN 'Nikola Trajkov'
        WHEN 2 THEN 'Marija Spasova'
        WHEN 3 THEN 'Petar Angelov'
        WHEN 4 THEN 'Sara Dimitrova'
        WHEN 5 THEN 'Filip Jovanov'
        WHEN 6 THEN 'Mila Kostova'
    END,
    id,
    NOW() - (row_number || ' hours')::interval
FROM selected_slots;


-- Rezerviranite termini povekje ne se dostapni
UPDATE training_slots
SET is_available = FALSE
WHERE id IN (
    SELECT training_slot_id
    FROM bookings
);


-- Prikaz na rezultatite
SELECT * FROM trainers;

SELECT
    COUNT(*) AS total_slots,
    COUNT(*) FILTER (WHERE is_available = TRUE) AS available_slots,
    COUNT(*) FILTER (WHERE is_available = FALSE) AS booked_slots
FROM training_slots;

SELECT * FROM bookings;