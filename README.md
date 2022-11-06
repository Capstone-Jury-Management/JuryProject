# Juror Search - Backend

## Backend Routes

### Search
  Fetches a list of jury participants associated with the given data
  parameters. At least one data paramater is required.

* **URL:**
    /search
* **Method:**
    `POST`
* **Data Params:**\
    `first_name=[string]`\
    `last_name=[string]`\
    `birth_date=[string]`\
    `ssn=[string]`\
    `mvc_id=[string]`\

### Participant
  Fetches juror details associated with the given participant_id.

* **URL:**
    /participant
* **Method:**
    `POST`
* **Data Params:**\
    `participant_id=[integer]`\
