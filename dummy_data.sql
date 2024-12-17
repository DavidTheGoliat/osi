-- Create table to store banknote history
CREATE TABLE IF NOT EXISTS banknote_history (
    serial_number TEXT,
    location TEXT,
    timestamp TEXT
);

-- Insert dummy data (locations across Switzerland)
INSERT INTO banknote_history VALUES ('CH123001', '46.9481,7.4474, Bern, Switzerland', '2024-06-01 09:30:00');
INSERT INTO banknote_history VALUES ('CH123001', '47.3769,8.5417, Zürich, Switzerland', '2024-06-03 14:15:00');
INSERT INTO banknote_history VALUES ('CH123001', '46.2044,6.1432, Geneva, Switzerland', '2024-06-05 16:45:00');
INSERT INTO banknote_history VALUES ('CH987002', '46.5197,6.6323, Lausanne, Switzerland', '2024-06-02 11:00:00');
INSERT INTO banknote_history VALUES ('CH987002', '47.0502,8.3093, Lucerne, Switzerland', '2024-06-04 13:00:00');
INSERT INTO banknote_history VALUES ('CH456003', '46.0215,7.7479, Zermatt, Switzerland', '2024-06-06 17:30:00');
INSERT INTO banknote_history VALUES ('CH456003', '46.0132,8.9274, Lugano, Switzerland', '2024-06-08 10:15:00');
INSERT INTO banknote_history VALUES ('CH789004', '47.3690,8.5380, Zürich Old Town, Switzerland', '2024-06-09 09:00:00');
INSERT INTO banknote_history VALUES ('CH789004', '47.5596,7.5886, Basel, Switzerland', '2024-06-10 12:45:00');
INSERT INTO banknote_history VALUES ('CH345005', '46.1270,8.6180, Locarno, Switzerland', '2024-06-12 15:15:00');
INSERT INTO banknote_history VALUES ('CH345005', '47.4245,9.3767, St. Gallen, Switzerland', '2024-06-14 18:30:00');
INSERT INTO banknote_history VALUES ('CH678006', '46.2083,6.1460, Geneva Lake, Switzerland', '2024-06-15 11:45:00');
INSERT INTO banknote_history VALUES ('CH678006', '46.9481,7.4474, Bern, Switzerland', '2024-06-17 09:30:00');
INSERT INTO banknote_history VALUES ('CH567007', '46.8800,8.2096, Engelberg, Switzerland', '2024-06-18 13:00:00');
INSERT INTO banknote_history VALUES ('CH567007', '46.8182,8.2275, Andermatt, Switzerland', '2024-06-20 14:30:00');
INSERT INTO banknote_history VALUES ('CH234008', '47.4810,8.2115, Baden, Switzerland', '2024-06-21 16:45:00');
INSERT INTO banknote_history VALUES ('CH234008', '47.0502,8.3093, Lucerne, Switzerland', '2024-06-23 17:30:00');
INSERT INTO banknote_history VALUES ('CH345009', '46.4978,9.8390, St. Moritz, Switzerland', '2024-06-24 09:00:00');
INSERT INTO banknote_history VALUES ('CH345009', '46.0215,7.7479, Zermatt, Switzerland', '2024-06-26 10:30:00');
INSERT INTO banknote_history VALUES ('CH123010', '46.5197,6.6323, Lausanne, Switzerland', '2024-06-27 11:15:00');
INSERT INTO banknote_history VALUES ('CH123010', '47.3769,8.5417, Zürich, Switzerland', '2024-06-29 12:30:00');
INSERT INTO banknote_history VALUES ('CH789011', '46.2044,6.1432, Geneva, Switzerland', '2024-06-30 14:00:00');
INSERT INTO banknote_history VALUES ('CH789011', '47.5596,7.5886, Basel, Switzerland', '2024-07-01 16:45:00');
INSERT INTO banknote_history VALUES ('CH567012', '46.1270,8.6180, Locarno, Switzerland', '2024-07-02 18:00:00');
INSERT INTO banknote_history VALUES ('CH567012', '47.4245,9.3767, St. Gallen, Switzerland', '2024-07-04 20:30:00');
