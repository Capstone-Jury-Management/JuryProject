# Jury Management System

## Backend Routes

### Search
  Fetches a list of jury participants associated with the given data
  parameters. At least one data paramater is required.

* **URL:**
    /api/search
* **Method:**
    `POST`
* **Data Params:**\
    `first_name=[string]`\
    `last_name=[string]`\
    `birth_date=[string]`\
    `ssn=[string]`\
    `mvc_id=[string]`

### Participant
  Fetches participant details associated with the given participant_id.

* **URL:**
    /api/participant
* **Method:**
    `POST`
* **Data Params:**\
    `participant_id=[integer]`
