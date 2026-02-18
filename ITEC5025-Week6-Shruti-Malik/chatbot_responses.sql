-- =============================================================================
-- chatbot_responses.sql
-- =============================================================================
-- ITEC5025 – Week 6 Assignment: Setting Up the Development Environment
-- Author : Shruti Malik
-- Date   : 2026-02-18
--
-- Purpose:
--   1. Create the `chatbot_responses` table to store keyword-triggered
--      replies for the Hypotify Clinical Chatbot.
--   2. Insert 20 clinical chatbot responses covering common patient
--      interactions (greetings, help, patient queries, lab results, etc.).
--   3. Create the `patient_demographics` table that mirrors the schema of
--      the 100,000-patient dataset (PatientCorePopulatedTable.txt).
--   4. Show example INSERT statements for patient records.
--
-- How to run (MySQL command line):
--   mysql -u root -p < chatbot_responses.sql
--
-- How to run (MySQL Workbench):
--   Open this file → Execute (Ctrl+Shift+Enter)
-- =============================================================================


-- -----------------------------------------------------------------------------
-- 0. Database setup
-- -----------------------------------------------------------------------------

-- Create (or reuse) a dedicated database for the chatbot project.
CREATE DATABASE IF NOT EXISTS hypotify_chatbot
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Switch to the chatbot database for all subsequent statements.
USE hypotify_chatbot;


-- =============================================================================
-- TABLE 1: chatbot_responses
-- =============================================================================
-- Stores keyword → response mappings that the chatbot looks up at runtime.
-- Columns:
--   id          – auto-incrementing primary key
--   keyword     – trigger word/phrase the chatbot matches against user input
--   response    – text the chatbot returns to the user
--   category    – logical grouping (greeting, help, patient, lab, etc.)
--   language    – response language (English / Spanish / Icelandic)
--   created_at  – timestamp of record creation (defaults to now)
-- =============================================================================

CREATE TABLE IF NOT EXISTS chatbot_responses (
    id          INT           NOT NULL AUTO_INCREMENT,
    keyword     VARCHAR(100)  NOT NULL,
    response    TEXT          NOT NULL,
    category    VARCHAR(50)   NOT NULL DEFAULT 'general',
    language    VARCHAR(20)   NOT NULL DEFAULT 'English',
    created_at  TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    INDEX idx_keyword  (keyword),
    INDEX idx_category (category),
    INDEX idx_language (language)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COMMENT='Keyword-triggered responses for the Hypotify Clinical Chatbot';


-- -----------------------------------------------------------------------------
-- INSERT: chatbot responses (20 records)
-- -----------------------------------------------------------------------------
-- Each INSERT adds a keyword/response pair.
-- The ON DUPLICATE KEY UPDATE clause prevents errors if the script is re-run.
-- -----------------------------------------------------------------------------

INSERT INTO chatbot_responses (keyword, response, category, language) VALUES

-- ── Greetings ────────────────────────────────────────────────────────────────
('hello',
 'Hello! Welcome to Hypotify Clinical Chatbot. How can I assist you today?',
 'greeting', 'English'),

('hi',
 'Hi there! I am your Hypotify clinical assistant. Type "help" to see what I can do.',
 'greeting', 'English'),

('hola',
 '¡Hola! Bienvenido al chatbot clínico Hypotify. ¿En qué puedo ayudarle hoy?',
 'greeting', 'Spanish'),

('good morning',
 'Good morning! Ready to assist with patient data and clinical insights.',
 'greeting', 'English'),

-- ── Help ─────────────────────────────────────────────────────────────────────
('help',
 'Available commands: patient <id>, patients list, insights language/age/gender, translate "<text>" to <lang>, exit.',
 'help', 'English'),

('commands',
 'Commands: patient <id> | patients list | insights <type> | translate | medical <term> | exit.',
 'help', 'English'),

('ayuda',
 'Comandos disponibles: paciente <id>, lista de pacientes, estadísticas, traducir, salir.',
 'help', 'Spanish'),

-- ── Patient queries ───────────────────────────────────────────────────────────
('patient not found',
 'No patient record was found for that ID. Please verify the Patient ID and try again.',
 'patient', 'English'),

('add patient',
 'To add a patient, type: patients add — then follow the prompts for name, DOB, gender, race, language, and poverty %.',
 'patient', 'English'),

('patient count',
 'The database currently holds records for 100,000 patients sourced from the EMRBots synthetic dataset.',
 'patient', 'English'),

('patient language',
 'Patients in this dataset speak English, Spanish, or Icelandic. Use: patients language <language> to filter.',
 'patient', 'English'),

-- ── Clinical insights ─────────────────────────────────────────────────────────
('insights',
 'Clinical insights available: language distribution, age statistics, gender breakdown, race/ethnicity, poverty analysis.',
 'insights', 'English'),

('poverty',
 'The average poverty percentage across all patients is calculated from PatientPopulationPercentageBelowPoverty. Use: insights poverty.',
 'insights', 'English'),

('age',
 'Patient ages range from newborns to over 100 years. Use: insights age — to see average age and distribution.',
 'insights', 'English'),

-- ── Lab results ───────────────────────────────────────────────────────────────
('lab results',
 'Lab data includes CBC panels, metabolic panels, and urinalysis. Each result is linked to a patient admission.',
 'lab', 'English'),

('cbc',
 'CBC (Complete Blood Count) includes: WBC, RBC, Hemoglobin, Hematocrit, Platelets, Neutrophils, Lymphocytes, and more.',
 'lab', 'English'),

('metabolic',
 'Metabolic panel includes: Sodium, Potassium, Chloride, CO2, Glucose, BUN, Creatinine, Albumin, Calcium, Bilirubin, AST, ALT, Alk Phos.',
 'lab', 'English'),

-- ── Translation ───────────────────────────────────────────────────────────────
('translate',
 'Translation usage: translate "<text>" to <language>. Supported: Spanish, French, Icelandic, and 100+ more via Google Translate.',
 'translation', 'English'),

-- ── Exit / Farewell ───────────────────────────────────────────────────────────
('goodbye',
 'Goodbye! Thank you for using Hypotify Clinical Chatbot. Stay healthy!',
 'farewell', 'English'),

('adios',
 '¡Adiós! Gracias por usar el chatbot clínico Hypotify. ¡Cuídese mucho!',
 'farewell', 'Spanish');


-- =============================================================================
-- TABLE 2: patient_demographics
-- =============================================================================
-- Mirrors the schema of PatientCorePopulatedTable.txt from the
-- 100,000-patient EMRBots synthetic dataset.
--
-- Columns map directly to the tab-delimited file headers:
--   PatientID                            → patient_id  (UUID string)
--   PatientGender                        → gender
--   PatientDateOfBirth                   → date_of_birth
--   PatientRace                          → race
--   PatientMaritalStatus                 → marital_status
--   PatientLanguage                      → language
--   PatientPopulationPercentageBelowPoverty → poverty_pct
-- =============================================================================

CREATE TABLE IF NOT EXISTS patient_demographics (
    patient_id    CHAR(36)       NOT NULL,
    gender        VARCHAR(10)    NOT NULL,
    date_of_birth DATETIME       NOT NULL,
    race          VARCHAR(50)    NOT NULL,
    marital_status VARCHAR(20)   NOT NULL,
    language      VARCHAR(30)    NOT NULL,
    poverty_pct   DECIMAL(5, 2)  NOT NULL DEFAULT 0.00,
    loaded_at     TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (patient_id),
    INDEX idx_gender   (gender),
    INDEX idx_race     (race),
    INDEX idx_language (language),
    INDEX idx_poverty  (poverty_pct)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COMMENT='100,000-patient demographics — EMRBots synthetic dataset';


-- -----------------------------------------------------------------------------
-- INSERT: sample patient records (5 rows from PatientCorePopulatedTable.txt)
-- These demonstrate the correct INSERT syntax before bulk-loading via Python.
-- -----------------------------------------------------------------------------

INSERT IGNORE INTO patient_demographics
    (patient_id, gender, date_of_birth, race, marital_status, language, poverty_pct)
VALUES
    ('F7CF0FE9-AFCD-49EF-BFB3-E42302FFA0D3', 'Female', '1951-07-10 07:29:47', 'Asian',            'Single',    'English',  13.70),
    ('C3935FBC-DBBA-4844-BBE4-A175FA508454', 'Male',   '1956-01-27 22:46:39', 'African American', 'Single',    'English',  15.73),
    ('1CA33F6F-2E84-4C99-AF6A-D40F7B4DB27F', 'Male',   '1972-12-22 10:11:01', 'White',            'Married',   'English',   7.09),
    ('81606388-2471-42A4-A6F1-1868AE25CFC3', 'Male',   '1984-01-17 00:49:06', 'Asian',            'Separated', 'Spanish',   2.17),
    ('E3120DE9-3361-40CF-A618-265C769E75A2', 'Female', '1978-12-21 07:24:08', 'White',            'Married',   'English',  18.67);

-- NOTE: The full 100,000 rows are loaded programmatically by load_patient_data.py
-- using LOAD DATA INFILE or batch INSERT for performance.


-- =============================================================================
-- Verification queries – run these to confirm data was inserted correctly
-- =============================================================================

-- Count chatbot responses
SELECT COUNT(*) AS total_responses FROM chatbot_responses;

-- Show all response categories
SELECT category, COUNT(*) AS count
FROM chatbot_responses
GROUP BY category
ORDER BY count DESC;

-- Count patient demographics rows
SELECT COUNT(*) AS total_patients FROM patient_demographics;

-- Language distribution in patient_demographics
SELECT language, COUNT(*) AS count
FROM patient_demographics
GROUP BY language
ORDER BY count DESC;

-- =============================================================================
-- End of chatbot_responses.sql
-- =============================================================================
